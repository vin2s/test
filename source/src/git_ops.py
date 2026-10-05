import subprocess
import os
from src.config import GITHUBMIRROR_DIR, README_PATH, GIT_ROOT
from src.logger import log, offset

# -------------------- GIT --------------------

def _git(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=check, cwd=GIT_ROOT)


def git_commit_and_push(dry_run: bool = False):
    """Принудительно добавляет 26.txt, делает коммит и пушит в GitHub."""
    try:
        mirror_26 = os.path.join(GITHUBMIRROR_DIR, "26.txt")
        root_26 = os.path.join(GIT_ROOT, "26.txt")
        paths_to_add: list[str] = []
        for path in (mirror_26, root_26):
            if os.path.exists(path):
                rel = os.path.relpath(path, GIT_ROOT).replace("\\", "/")
                paths_to_add.append(rel)
        if os.path.exists(README_PATH):
            paths_to_add.append(os.path.relpath(README_PATH, GIT_ROOT).replace("\\", "/"))

        if not paths_to_add:
            log("⚠️ Файлы 26.txt не найдены — коммит пропущен")
            return

        _git(["git", "add", "-f", *paths_to_add])

        diff = _git(["git", "diff", "--cached", "--quiet"], check=False)
        if diff.returncode == 0:
            log("ℹ️ Нет изменений для коммита")
            return

        _git(["git", "commit", "-m", f"🚀 Автообновление репозитория: {offset}"])
        log("✅ Коммит создан")

        if dry_run:
            log("ℹ️ Dry-run: push пропущен")
            return

        _git(["git", "push", "origin", "HEAD"])
        log("✅ Изменения запушены в репозиторий")

    except subprocess.CalledProcessError as e:
        log(f"❌ Ошибка git: {e}")
