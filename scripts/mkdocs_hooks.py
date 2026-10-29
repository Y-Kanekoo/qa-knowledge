"""ローカルプレビュー中に元文書の変更を公開用入力へ反映する。"""

import subprocess
import sys
from pathlib import Path


def on_pre_build(config):
    """MkDocs の再ビルド前に、変更された文書だけを同期する。"""
    script = Path(__file__).resolve().with_name("prepare_site_docs.py")
    subprocess.run([sys.executable, str(script)], check=True)
