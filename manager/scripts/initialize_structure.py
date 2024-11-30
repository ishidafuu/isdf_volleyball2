from pathlib import Path
import logging
from typing import List, Dict


class DirectoryInitializer:
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.logger = self._setup_logger()

    @staticmethod
    def _setup_logger():
        """ロガーの設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)

    def get_directory_structure(self) -> Dict[str, List[str]]:
        """ディレクトリ構造の定義"""
        return {
            "_config": {
                "dirs": ["templates"],
                "files": ["constants.md", "tags.md"]
            },
            "_indexes": {
                "dirs": [],
                "files": ["character-list.md", "ability-ranking.md",
                          "height-chart.md", "position-matrix.md"]
            },
            "individual-characters": {
                "dirs": [],
                "files": []  # キャラクターファイルは後で追加
            },
            "teams": {
                "dirs": ["teio-high", "tsukiura-high", "seiwa-high",
                         "sousei-high", "hisui-high", "sakura-high"],
                "files": []
            },
            "relationships": {
                "dirs": ["rivals", "siblings", "middle-school",
                         "team-dynamics", "position-based",
                         "special-relationships"],
                "files": []
            },
            "episodes": {
                "dirs": ["_timeline", "tournaments", "development"],
                "files": []
            },
            "locations": {
                "dirs": ["schools", "districts", "landmarks"],
                "files": []
            },
            "meta": {
                "dirs": [],
                "files": ["timeline.md", "locations.md", "glossary.md"]
            },
            "_cross-references": {
                "dirs": ["skill-connections", "strategy-links",
                         "development-paths"],
                "files": []
            }
        }

    def create_directories(self):
        """ディレクトリ構造の作成"""
        self.logger.info(f"Creating directory structure in {self.base_path}")

        # ベースディレクトリの作成
        self.base_path.mkdir(exist_ok=True)

        # README.mdの作成
        readme_path = self.base_path / "README.md"
        if not readme_path.exists():
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write("# Character Management System\n\n")
                f.write("## Directory Structure\n\n")
                # ディレクトリ構造の説明を追加

        # 各ディレクトリとファイルの作成
        structure = self.get_directory_structure()
        for main_dir, contents in structure.items():
            main_path = self.base_path / main_dir
            main_path.mkdir(exist_ok=True)
            self.logger.info(f"Created directory: {main_path}")

            # サブディレクトリの作成
            for sub_dir in contents['dirs']:
                sub_path = main_path / sub_dir
                sub_path.mkdir(exist_ok=True)
                self.logger.info(f"Created sub-directory: {sub_path}")

            # 初期ファイルの作成
            for file_name in contents['files']:
                file_path = main_path / file_name
                if not file_path.exists():
                    file_path.touch()
                    self.logger.info(f"Created file: {file_path}")

    def verify_structure(self) -> bool:
        """ディレクトリ構造の検証"""
        structure = self.get_directory_structure()
        success = True

        for main_dir, contents in structure.items():
            main_path = self.base_path / main_dir
            if not main_path.exists():
                self.logger.error(f"Missing directory: {main_path}")
                success = False
                continue

            for sub_dir in contents['dirs']:
                sub_path = main_path / sub_dir
                if not sub_path.exists():
                    self.logger.error(f"Missing sub-directory: {sub_path}")
                    success = False

            for file_name in contents['files']:
                file_path = main_path / file_name
                if not file_path.exists():
                    self.logger.error(f"Missing file: {file_path}")
                    success = False

        return success


def main():
    """メイン実行関数"""
    base_path = Path("characters")  # プロジェクトのルートディレクトリ

    initializer = DirectoryInitializer(base_path)
    initializer.create_directories()

    if initializer.verify_structure():
        initializer.logger.info("Directory structure created successfully!")
    else:
        initializer.logger.error("Some elements are missing in the directory structure")


if __name__ == "__main__":
    main()