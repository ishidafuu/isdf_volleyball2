from character_manager.scripts.index_generator.base import BaseIndexGenerator

class CrossoverMapGenerator(BaseIndexGenerator):
    def generate(self) -> None:
        """クロスオーバーイベントマップの生成"""
        episodes = self.read_episode_data()
        relationships = self.read_relationship_data()

        content = self.create_header("クロスオーバーイベントマップ")

        # 1. 合同イベントマップ
        content.extend([
            "## 合同イベント",
            "```mermaid",
            "graph TD"
        ])

        # イベントとチーム/キャラクターの関係を可視化
        for event in self.get_joint_events():
            for participant in event['participants']:
                content.append(
                    f"    {event['id']}[{event['title']}] "
                    f"--{participant['role']}--> "
                    f"{participant['id']}[{participant['name']}]"
                )
        content.extend(["```", ""])

        # 2. クロスチーム関係性
        content.extend(["## クロスチーム関係性", ""])
        for event_type in self.get_crossover_types():
            content.extend([
                f"### {event_type}",
                "| イベント | 参加者 | 影響 | 派生関係 |",
                "|----------|--------|------|-----------|"
            ])
            for event in self.get_crossover_events(event_type):
                content.append(
                    f"| {event['title']} | "
                    f"{', '.join(event['participants'])} | "
                    f"{event['impact']} | "
                    f"{event['derived_relationships']} |"
                )
            content.append("")

        self.save_index(content, "crossover-map.md")