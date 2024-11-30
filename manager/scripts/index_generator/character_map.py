from character_manager.scripts.index_generator.base import BaseIndexGenerator


class CharacterMapGenerator(BaseIndexGenerator):
    def generate(self) -> None:
        """キャラクター一覧の生成"""
        characters = self.read_character_data()

        # ヘッダー部分の作成
        content = self.create_header("キャラクター一覧")
        content.append("## チーム別キャラクター一覧")

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
        self.save_index(content, "character-list.md")