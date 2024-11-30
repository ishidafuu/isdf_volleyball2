from character_manager.scripts.index_generator.base import BaseIndexGenerator

class GrowthMapGenerator(BaseIndexGenerator):
    def generate(self) -> None:
        """キャラクターの成長過程マップの生成"""
        characters = self.read_character_data()
        episodes = self.read_episode_data()

        content = self.create_header("キャラクター成長過程マップ")

        # 1. チーム別成長マップ
        for team in self.get_teams():
            content.extend([
                f"## {team}の成長過程",
                "```mermaid",
                "graph TD"
            ])

            # 各キャラクターの成長イベントをノードとして配置
            for char in self.get_team_characters(team):
                events = self.get_character_growth_events(char['character_id'])
                for i, event in enumerate(events[:-1]):
                    content.append(
                        f"    {char['character_id']}_{i}[{event['title']}] "
                        f"--{event['growth_type']}--> "
                        f"{char['character_id']}_{i + 1}[{events[i + 1]['title']}]"
                    )
            content.extend(["```", ""])

        # 2. 技術習得ツリー
        content.extend(["## 技術習得ツリー", ""])
        for skill_type in self.get_skill_types():
            content.extend([
                f"### {skill_type}",
                "```mermaid",
                "graph LR"
            ])
            for skill in self.get_skills_by_type(skill_type):
                for prereq in skill['prerequisites']:
                    content.append(
                        f"    {prereq['id']}[{prereq['name']}] "
                        f"--> {skill['id']}[{skill['name']}]"
                    )
            content.extend(["```", ""])

        # 3. 影響関係マップ
        content.extend(["## 影響関係マップ", ""])
        influences = self.get_influence_relationships()
        for category, relations in influences.items():
            content.extend([
                f"### {category}",
                "| 影響元 | 影響先 | 内容 | 結果 |",
                "|--------|--------|------|------|"
            ])
            for inf in relations:
                content.append(
                    f"| {inf['from']} | "
                    f"{inf['to']} | "
                    f"{inf['content']} | "
                    f"{inf['result']} |"
                )
            content.append("")

        self.save_index(content, "growth-map.md")