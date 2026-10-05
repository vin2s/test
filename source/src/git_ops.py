import subprocess
import os
from src.config import GITHUBMIRROR_DIR, README_PATH, GIT_ROOT
from src.logger import log, offset

# -------------------- GIT --------------------

def git_commit_and_push(dry_run: bool = False):
    """Добавляет изменённые файлы в индекс, делает коммит и пушит."""
    try:
        paths_to_add = [
            os.path.relpath(os.path.join(GITHUBMIRROR_DIR, "26.txt"), GIT_ROOT),
            "26.txt",
        ]
        if os.path.exists(README_PATH):
            paths_to_add.append(os.path.relpath(README_PATH, GIT_ROOT))

        subprocess.run(
            ["git", "add", *paths_to_add],
            check=True,
            cwd=GIT_ROOT,
        )

        diff = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=GIT_ROOT,
        )
        if diff.returncode == 0:
            log("ℹ️ Нет изменений для коммита")
            return

        subprocess.run(
            ["git", "commit", "-m", f"🚀 Автообновление репозитория: {offset}"],
            check=True,
            cwd=GIT_ROOT,
        )
        log("✅ Коммит создан")

        if dry_run:
            log("ℹ️ Dry-run: push пропущен")
            return

        subprocess.run(["git", "push"], check=True, cwd=GIT_ROOT)
        log("✅ Изменения запушены в репозиторий")

    except subprocess.CalledProcessError as e:
        log(f"❌ Ошибка git: {e}")
