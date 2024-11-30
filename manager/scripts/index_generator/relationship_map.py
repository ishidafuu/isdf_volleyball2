from pathlib import Path
from typing import Dict, List, Any
from character_manager.scripts.index_generator.base import BaseIndexGenerator


class RelationshipMapGenerator(BaseIndexGenerator):
    def generate(self) -> None:
        """関係性マップの生成"""
        characters = self.read_character_data()
        relationships = self.read_relationship_data()

        content = self.create_header("キャラクター関係性マップ")

        # 1. チーム内関係
        content.extend(["## チーム内関係", ""])
        for team in self.get_teams():
            content.extend([
                f"### {team}",
                "```mermaid",
                "graph TD"
            ])
            team_chars = self.get_team_characters(team)
            for rel in self.filter_team_relationships(team_chars):
                content.append(
                    f"    {rel['from_id']}[{rel['from_name']}] "
                    f"--{rel['type']}--> "
                    f"{rel['to_id']}[{rel['to_name']}]"
                )
            content.extend(["```", ""])

        # 2. チーム間ライバル関係
        content.extend(["## チーム間ライバル関係", "```mermaid", "graph LR"])
        for rel in self.get_rival_relationships():
            content.append(
                f"    {rel['from_id']}[{rel['from_name']}] "
                f"--ライバル--> "
                f"{rel['to_id']}[{rel['to_name']}]"
            )
        content.extend(["```", ""])

        # 3. 特別な関係性
        content.extend(["## 特別な関係性", ""])
        special_rels = {
            "兄弟関係": self.get_sibling_relationships(),
            "幼なじみ": self.get_childhood_friend_relationships(),
            "師弟関係": self.get_mentor_relationships()
        }
        for rel_type, rels in special_rels.items():
            content.extend([f"### {rel_type}", ""])
            for rel in rels:
                content.append(f"- {rel['description']}")
            content.append("")

        self.save_index(content, "relationship-map.md")