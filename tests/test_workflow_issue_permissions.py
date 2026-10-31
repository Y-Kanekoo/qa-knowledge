"""失敗時の Issue 通知に必要な GitHub Actions 権限を確認する。"""

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize("name", ["validate.yml", "generate-index.yml"])
def test_failure_issue_notification_has_write_permission(name):
    workflow = yaml.safe_load((ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8"))
    jobs = workflow["jobs"].values()
    notifying_jobs = [job for job in jobs if any("gh issue create" in step.get("run", "") for step in job["steps"])]
    assert notifying_jobs
    for job in notifying_jobs:
        assert job.get("permissions", workflow.get("permissions", {}))["issues"] == "write"
