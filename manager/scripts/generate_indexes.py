from pathlib import Path
import logging
import yaml
import pandas as pd
from typing import Dict, List, Any
import frontmatter
from datetime import datetime


class IndexGenerator:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.indexes_dir = base_path / "_indexes"
        self.characters_dir = base_path / "individual-characters"
        self.logger = self._setup_logger()

    @staticmethod
    def _setup_logger():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)

    def read_character_data(self) -> List[Dict[str, Any]]:
        """全キャラクターデータの読み込み"""
        characters = []
        for char_dir in self.characters_dir.glob("**/"):
            profile_path = char_dir / "profile.md"
            if profile_path.is_file():
                try:
                    post = frontmatter.load(profile_path)
                    char_data = post.metadata
                    char_data['profile_path'] = str(profile_path.relative_to(self.base_path))
                    characters.append(char_data)
                except Exception as e:
                    self.logger.error(f"Error reading {profile_path}: {e}")
        return characters

    def generate_character_list(self) -> None:
        """キャラクター一覧の生成"""
        characters = self.read_character_data()

        # Markdown形式でのキャラクター一覧生成
        content = [
            "---",
            "version: 1.0.0",
            f"last_updated: {datetime.now().strftime('%Y-%m-%d')}",
            "status: generated",
            "---",
            "",
            "# キャラクター一覧",
            "",
            "## チーム別キャラクター一覧",
        ]

        # チームでグループ化
        chars_by_team = {}
        for char in characters:
            team = char.get('team', 'その他')
            if team not in chars_by_team:
                chars_by_team[team] = []
            chars_by_team[team].append(char)

        # チームごとにキャラクターを出力
        for team in sorted(chars_by_team.keys()):
            content.extend([
                f"### {team}",
                "",
                "| ID | 名前 | ポジション | 学年 | 身長 |",
                "|-----|------|------------|------|------|"
            ])

            for char in sorted(chars_by_team[team], key=lambda x: x.get('character_id', '')):
                name = char.get('name', {})
                full_name = name.get('full', 'N/A')
                content.append(
                    f"| {char.get('character_id', 'N/A')} | "
                    f"{full_name} | "
                    f"{char.get('position', 'N/A')} | "
                    f"{char.get('year', 'N/A')}年 | "
                    f"{char.get('height', 'N/A')}cm |"
                )
            content.append("")

        # ファイルに保存
        output_path = self.indexes_dir / "character-list.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        self.logger.info(f"Generated character list: {output_path}")

    def generate_ability_ranking(self) -> None:
        """能力値ランキングの生成"""
        characters = self.read_character_data()

        content = [
            "---",
            "version: 1.0.0",
            f"last_updated: {datetime.now().strftime('%Y-%m-%d')}",
            "status: generated",
            "---",
            "",
            "# 能力値ランキング",
            ""
        ]

        # 能力値カテゴリ
        ability_categories = [
            'attack', 'receive', 'serve', 'block',
            'stamina', 'technique'
        ]

        # 各能力値のランキングを生成
        for category in ability_categories:
            content.extend([
                f"## {category.capitalize()}ランキング",
                "",
                "| ランク | 名前 | チーム | 学年 |",
                "|--------|------|--------|------|"
            ])

            # キャラクターを能力値でソート
            sorted_chars = sorted(
                [c for c in characters if c.get('abilities', {}).get(category)],
                key=lambda x: x.get('abilities', {}).get(category, 'C'),
                reverse=True
            )

            for char in sorted_chars:
                name = char.get('name', {}).get('full', 'N/A')
                content.append(
                    f"| {char.get('abilities', {}).get(category, 'C')} | "
                    f"{name} | "
                    f"{char.get('team', 'N/A')} | "
                    f"{char.get('year', 'N/A')}年 |"
                )
            content.append("")

        # ファイルに保存
        output_path = self.indexes_dir / "ability-ranking.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        self.logger.info(f"Generated ability ranking: {output_path}")

    def generate_height_chart(self) -> None:
        """身長一覧の生成"""
        characters = self.read_character_data()

        content = [
            "---",
            "version: 1.0.0",
            f"last_updated: {datetime.now().strftime('%Y-%m-%d')}",
            "status: generated",
            "---",
            "",
            "# 身長一覧",
            "",
            "| 名前 | 身長 | チーム | ポジション | 学年 |",
            "|------|------|--------|------------|------|"
        ]

        # 身長でソート（降順）
        sorted_chars = sorted(
            characters,
            key=lambda x: x.get('height', 0),
            reverse=True
        )

        for char in sorted_chars:
            name = char.get('name', {}).get('full', 'N/A')
            content.append(
                f"| {name} | "
                f"{char.get('height', 'N/A')}cm | "
                f"{char.get('team', 'N/A')} | "
                f"{char.get('position', 'N/A')} | "
                f"{char.get('year', 'N/A')}年 |"
            )

        # ファイルに保存
        output_path = self.indexes_dir / "height-chart.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        self.logger.info(f"Generated height chart: {output_path}")

    def generate_position_matrix(self) -> None:
        """ポジション別選手マトリックスの生成"""
        characters = self.read_character_data()

        content = [
            "---",
            "version: 1.0.0",
            f"last_updated: {datetime.now().strftime('%Y-%m-%d')}",
            "status: generated",
            "---",
            "",
            "# ポジション別選手マトリックス",
            ""
        ]

        # ポジション定義
        positions = ['WSP', 'MB', 'S', 'L', 'OPP']

        # 各ポジションのマトリックスを生成
        for position in positions:
            content.extend([
                f"## {position}",
                "",
                "| チーム | 3年生 | 2年生 | 1年生 |",
                "|--------|--------|--------|--------|"
            ])

            # チームでグループ化
            chars_by_team = {}
            for char in characters:
                if char.get('position') == position:
                    team = char.get('team', 'その他')
                    if team not in chars_by_team:
                        chars_by_team[team] = {1: [], 2: [], 3: []}
                    year = char.get('year', 0)
                    if year in chars_by_team[team]:
                        chars_by_team[team][year].append(char)

            # チームごとに出力
            for team in sorted(chars_by_team.keys()):
                year_data = chars_by_team[team]
                content.append(
                    f"| {team} | "
                    f"{', '.join(c.get('name', {}).get('full', 'N/A') for c in year_data[3])} | "
                    f"{', '.join(c.get('name', {}).get('full', 'N/A') for c in year_data[2])} | "
                    f"{', '.join(c.get('name', {}).get('full', 'N/A') for c in year_data[1])} |"
                )
            content.append("")

        # ファイルに保存
        output_path = self.indexes_dir / "position-matrix.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        self.logger.info(f"Generated position matrix: {output_path}")

    def generate_all_indexes(self) -> None:
        """全インデックスの生成"""
        self.generate_character_list()
        self.generate_ability_ranking()
        self.generate_height_chart()
        self.generate_position_matrix()
        self.logger.info("All indexes generated successfully")


def main():
    """メイン実行関数"""
    base_path = Path("characters")
    generator = IndexGenerator(base_path)
    generator.generate_all_indexes()


if __name__ == "__main__":
    main()