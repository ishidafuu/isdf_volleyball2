from pathlib import Path
import time
import logging
import sys
import yaml
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Set, Optional
import git
from datetime import datetime


class UpdateManager:
    def __init__(self, character_path: Path, repo_path: Path):
        self.character_path = Path(character_path)
        self.characters_dir = self.character_path / "individual-characters"
        self.indexes_dir = self.character_path / "_indexes"
        self.logger = self._setup_logger()
        self.repo = self._get_git_repo(repo_path)
        self.changed_files: Set[Path] = set()
        self.last_update = datetime.now()

    @staticmethod
    def _setup_logger():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)

    def _get_git_repo(self, repo_path: Path) -> Optional[git.Repo]:
        """メインのGitリポジトリを取得"""
        try:
            repo = git.Repo(repo_path, search_parent_directories=True)
            self.logger.info(f"Found Git repository at: {repo.working_dir}")
            return repo
        except git.InvalidGitRepositoryError:
            self.logger.warning("Git repository not found")
            return None

    def _is_update_needed(self) -> bool:
        """更新が必要かどうかの判定"""
        # 最後の更新から5分以上経過し、かつファイル変更がある場合
        time_threshold = (datetime.now() - self.last_update).seconds > 300
        return bool(self.changed_files) and time_threshold

    def update_indexes(self):
        """インデックスの更新"""
        from character_manager.scripts.generate_indexes import IndexGenerator

        try:
            self.logger.info("Updating indexes...")
            generator = IndexGenerator(self.character_path)
            generator.generate_all_indexes()

            # Git commitの作成
            if self.repo:
                self._create_git_commit()

            self.changed_files.clear()
            self.last_update = datetime.now()
            self.logger.info("Indexes updated successfully")

        except Exception as e:
            self.logger.error(f"Error updating indexes: {e}")

    def _create_git_commit(self):
        """Git commitの作成"""
        try:
            # インデックスファイルの追加
            # 相対パスに変換
            index_files = [str(f.relative_to(Path(self.repo.working_dir)))
                           for f in self.indexes_dir.glob("*.md")]
            self.repo.index.add(index_files)

            # 変更されたキャラクターファイルの追加
            changed_files = [str(f.relative_to(Path(self.repo.working_dir)))
                             for f in self.changed_files]
            self.repo.index.add(changed_files)

            # コミットの作成
            commit_message = f"Auto-update: Indexes and character files\n\nUpdated files:\n" + \
                             "\n".join(changed_files)
            self.repo.index.commit(commit_message)

        except Exception as e:
            self.logger.error(f"Error creating git commit: {e}")


class CharacterFileHandler(FileSystemEventHandler):
    def __init__(self, update_manager: UpdateManager):
        self.update_manager = update_manager
        self.logger = update_manager.logger

    def on_modified(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        if file_path.suffix == '.md' and 'individual-characters' in str(file_path):
            self.logger.info(f"Detected change in: {file_path}")
            self.update_manager.changed_files.add(file_path)


def main():
    """メイン実行関数"""
    # charactersディレクトリとプロジェクトルートのパスを設定
    project_root = Path(__file__).resolve().parents[2]  # character_managerのルートディレクトリ
    characters_path = project_root / "characters"

    # UpdateManagerの初期化
    update_manager = UpdateManager(characters_path, project_root)

    # ファイル監視の設定
    event_handler = CharacterFileHandler(update_manager)
    observer = Observer()
    observer.schedule(event_handler, str(update_manager.characters_dir), recursive=True)
    observer.start()

    try:
        while True:
            if update_manager._is_update_needed():
                update_manager.update_indexes()
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
        update_manager.logger.info("Stopping file monitoring")

    observer.join()


if __name__ == "__main__":
    main()