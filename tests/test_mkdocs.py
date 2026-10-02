"""Verify public source selection and the strict build used before deployment."""

import json
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import unquote, urlsplit

import pytest
import yaml
from bs4 import BeautifulSoup
from mkdocs.structure.files import File, Files

from scripts.mkdocs_hooks import _navigation_paths, on_files

ROOT = Path(__file__).resolve().parents[1]


def test_navigation_paths_only_select_local_markdown():
    assert _navigation_paths(
        [{"Home": "index.md"}, {"Guides": [{"Schema": "docs/schema.md"}]}]
        + [{"External": "https://example.com/guide.md"}, {"Section": "#section"}]
    ) == {"index.md", "docs/schema.md"}
    assert _navigation_paths([]) == set()


def test_source_selection_preserves_paths_and_theme_assets(tmp_path):
    root = tmp_path / "repo"
    public_paths = {"index.md", "indexes/by-company.md", "docs/schema.md", "entries/article.md"}
    private_paths = {
        "entries/_template.md", "docs/internal.md", "README.md", "scripts/internal.py",
        "tests/internal.py", ".github/workflows/ci.yml", ".env",
    }
    for path in public_paths | private_paths:
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# Test", encoding="utf-8")
    theme = tmp_path / "theme"
    theme.mkdir()
    (theme / "theme.css").write_text("body {}", encoding="utf-8")
    site = str(tmp_path / "site")
    config = SimpleNamespace(
        config_file_path=str(root / "mkdocs.yml"), docs_dir=str(root / "docs"),
        site_dir=site, use_directory_urls=True,
        nav=[{"Home": "index.md"}, {"Index": "indexes/by-company.md"}, {"Schema": "docs/schema.md"}],
    )
    files = Files([
        File("schema.md", str(root / "docs"), site, True),
        File("internal.md", str(root / "docs"), site, True),
        File("theme.css", str(theme), site, True),
    ])

    result = on_files(files, config=config)

    assert {file.src_uri for file in result} == public_paths | {"theme.css"}
    assert result.get_file_from_path("theme.css").abs_src_path == str(theme / "theme.css")
    for path in public_paths:
        file = result.get_file_from_path(path)
        assert file.abs_src_path == str(root / path)
        expected = "index.html" if path == "index.md" else path.removesuffix(".md") + "/index.html"
        assert file.dest_uri == expected


@pytest.fixture(scope="module")
def built_site(tmp_path_factory):
    """Build the real repository in isolation, including the CI index-generation step."""
    root = tmp_path_factory.mktemp("mkdocs") / "repo"
    shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", ".venv", "site", "__pycache__", ".pytest_cache"))
    for command in (["scripts/generate_index.py"], ["-m", "mkdocs", "build", "--strict"]):
        result = subprocess.run(
            [sys.executable, *command], cwd=root, capture_output=True, text=True, check=False,
        )
        assert result.returncode == 0, result.stdout + result.stderr
    return root, root / "site"


def test_strict_build_publishes_all_entries_and_only_selected_pages(built_site):
    root, site = built_site
    config = yaml.safe_load((root / "mkdocs.yml").read_text(encoding="utf-8"))
    entries = {path.relative_to(root).as_posix() for path in (root / "entries").glob("*.md")
               if path.name != "_template.md"}
    assert entries  # Do not permit a vacuous pass if entry discovery breaks.
    expected_sources = _navigation_paths(config["nav"]) | entries
    expected_html = {"index.html" if path == "index.md" else path.removesuffix(".md") + "/index.html"
                     for path in expected_sources}
    actual_html = {path.relative_to(site).as_posix() for path in site.rglob("*.html")}
    assert actual_html == expected_html | {"404.html"}
    assert not any(site.rglob("*.md"))
    assert not any(site.rglob("*.py"))
    assert not any(site.rglob("*.yml"))
    for private_path in (".github", ".claude", "scripts", "tests", "docs/review-report", "entries/_template"):
        assert not (site / private_path).exists()

    # Every entry is discoverable from the company index and the search index.
    company = BeautifulSoup((site / "indexes/by-company/index.html").read_text(encoding="utf-8"), "html.parser")
    entry_links = {node["href"] for node in company.select("article a[href]")}
    search = json.loads((site / "search/search_index.json").read_text(encoding="utf-8"))
    search_locations = {doc["location"].split("#")[0] for doc in search["docs"]}
    for entry in entries:
        url = entry.removesuffix(".md") + "/"
        assert "../../" + url in entry_links
        assert url in search_locations


def test_built_site_local_links_and_assets_resolve(built_site):
    _, site = built_site
    documents = {
        page.resolve(): BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        for page in site.rglob("*.html") if page.name != "404.html"
    }
    checked = 0
    for page, document in documents.items():
        for node in document.select("a[href], link[href], script[src], img[src]"):
            url = urlsplit(node.get("href", node.get("src", "")))
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            target = ((site / path.lstrip("/")) if path.startswith("/") else page.parent / path).resolve()
            if target.is_dir():
                target /= "index.html"
            assert target.is_relative_to(site.resolve()), (page, url)
            assert target.is_file(), (page, url, target)
            if url.fragment and target in documents:
                fragment = unquote(url.fragment)
                assert documents[target].find(id=fragment) or documents[target].find(attrs={"name": fragment}), (
                    page, url, target,
                )
            checked += 1
    assert checked > len(documents)


@pytest.mark.parametrize("broken_source", ["navigation", "entry_link"])
def test_strict_build_rejects_missing_pages_and_entry_links(tmp_path, broken_source):
    root = tmp_path / "repo"
    (root / "docs").mkdir(parents=True)
    (root / "scripts").mkdir()
    (root / "entries").mkdir()
    shutil.copy2(ROOT / "scripts/mkdocs_hooks.py", root / "scripts/mkdocs_hooks.py")
    config = {
        "site_name": "Strict regression test", "hooks": ["scripts/mkdocs_hooks.py"],
        "nav": [{"Home": "index.md"}],
    }
    if broken_source == "navigation":
        config["nav"].append({"Missing": "docs/missing.md"})
    (root / "mkdocs.yml").write_text(yaml.safe_dump(config), encoding="utf-8")
    (root / "index.md").write_text("# Home", encoding="utf-8")
    content = "# Entry\n\n[Broken related entry](missing.md)" if broken_source == "entry_link" else "# Entry"
    (root / "entries/article.md").write_text(content, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict"], cwd=root,
        capture_output=True, text=True, check=False,
    )

    assert result.returncode != 0
    assert "missing.md" in result.stdout + result.stderr
    assert "strict mode" in result.stdout + result.stderr
