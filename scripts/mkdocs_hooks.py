"""Publish the knowledge pages without copying the repository into the site."""

from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files


def _navigation_paths(nav: list | dict | str) -> set[str]:
    """Collect local Markdown pages explicitly selected for the public navigation."""
    if isinstance(nav, str):
        return {nav} if nav.endswith(".md") and "://" not in nav else set()
    children = nav.values() if isinstance(nav, dict) else nav
    return set().union(*(_navigation_paths(child) for child in children))


def on_files(files: Files, *, config: MkDocsConfig) -> Files:
    """Keep theme assets, then add only navigation pages and non-template entries.

    Sources retain their repository-relative paths, so links from the generated
    indexes and between entries work both on GitHub and in MkDocs. In particular,
    docs/ is not flattened, and scripts, tests and project metadata never become
    downloadable site assets.
    """
    root = Path(config.config_file_path).resolve().parent
    docs_dir = Path(config.docs_dir).resolve()
    for file in list(files):
        if file.abs_src_path and Path(file.abs_src_path).is_relative_to(docs_dir):
            files.remove(file)

    paths = _navigation_paths(config.nav)
    paths.update(
        path.relative_to(root).as_posix()
        for path in (root / "entries").glob("*.md")
        if path.name != "_template.md"
    )
    for path in sorted(paths):
        # Let MkDocs report missing nav targets through its strict validation.
        if (root / path).is_file():
            files.append(File(path, str(root), config.site_dir, config.use_directory_urls))
    return files
