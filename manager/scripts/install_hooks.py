from pathlib import Path
import subprocess
import logging


def install_git_hooks(base_path: Path):
    """Git hooksのインストール"""
    logger = logging.getLogger(__name__)
    hooks_dir = base_path / ".git" / "hooks"

    logger.info(f"Current working directory: {Path.cwd()}")
    logger.info(f"Base path: {base_path}")
    logger.info(f"Hooks directory path: {hooks_dir}")

    # .gitディレクトリの存在確認
    git_dir = base_path / ".git"
    if not git_dir.exists():
        logger.error(f"Git directory not found at {git_dir}")
        return False

    # hooksディレクトリの作成（存在しない場合）
    hooks_dir.mkdir(exist_ok=True)

    if not hooks_dir.exists():
        logger.error(f"Failed to create hooks directory at {hooks_dir}")
        return False

    # post-commit hookの作成/更新
    post_commit = hooks_dir / "post-commit"
    post_commit_content = """#!/bin/sh
# Run repomix
npx repomix

# Check if repomix-output.txt exists and has changes
if [ -f repomix-output.txt ]; then
    # 差分がない場合は終了
    if git diff --quiet repomix-output.txt; then
        exit 0
    fi

    # ヘッダー部分（最初の5行）以降に実質的な差分があるかチェック
    DIFF_COUNT=$(git diff repomix-output.txt | 
        awk '
            BEGIN { header_passed = 0; count = 0; }
            /^@@/ { if (!header_passed) header_passed = 1; next; }
            /^[+-]/ {
                if (header_passed && NR > 10) {
                    # ヘッダー部分を過ぎた行で、プラスかマイナスで始まる行をカウント
                    count++;
                }
            }
            END { print count; }
        ')

    if [ "$DIFF_COUNT" -eq 0 ]; then
        # 実質的な差分がない場合は変更を破棄
        git checkout -- repomix-output.txt
        exit 0
    fi

    # Stage and amend the commit with the updated file
    git add repomix-output.txt
    git commit --amend --no-edit
fi
"""
    post_commit.write_text(post_commit_content)
    post_commit.chmod(0o755)

    # pre-pushフックを削除（もし存在する場合）
    pre_push = hooks_dir / "pre-push"
    if pre_push.exists():
        pre_push.unlink()

    logger.info("Git hooks installed successfully")
    return True


def main():
    """メイン実行関数"""
    logging.basicConfig(level=logging.INFO)
    try:
        git_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'],
                                           universal_newlines=True).strip()
        base_path = Path(git_root)
        install_git_hooks(base_path)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to find Git repository root: {e}")


if __name__ == "__main__":
    main()