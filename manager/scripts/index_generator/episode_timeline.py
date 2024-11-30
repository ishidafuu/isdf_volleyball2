from pathlib import Path
from typing import Dict, List, Any
from character_manager.scripts.index_generator.base import BaseIndexGenerator

class EpisodeTimelineGenerator(BaseIndexGenerator):
    def generate(self) -> None:
        """エピソードタイムラインの生成"""
        content = self.create_header("エピソードタイムライン")

        # 1. 時系列表示
        content.extend([
            "## 時系列展開",
            "```mermaid",
            "timeline"
        ])

        # 時系列ごとのエピソード表示
        for period in self.get_time_periods():
            content.append(f"    section {period}")
            for ep in self.get_episodes_by_period(period):
                participants_str = ", ".join(ep['participants'])
                content.append(
                    f"        {ep['title']} : "
                    f"{participants_str}"
                )
        content.extend(["```", ""])

        # 2. 重要イベント一覧
        content.extend(["## 重要イベント", ""])
        for event in self.get_major_events():
            content.extend([
                f"### {event['title']}",
                f"- 時期: {event['period']}",
                f"- 参加者: {', '.join(event['participants'])}",
                f"- 影響: {event['impact']}",
                ""
            ])

        # 3. キャラクター別重要エピソード
        content.extend(["## キャラクター別重要エピソード", ""])
        for char in self.get_main_characters():
            char_name = char.get('name', {}).get('full', 'Unknown')
            episodes = self.get_character_episodes(char.get('character_id', ''))

            if episodes:
                content.extend([
                    f"### {char_name}",
                    "| 時期 | エピソード | 影響 |",
                    "|------|------------|------|"
                ])

                for ep in episodes:
                    content.append(
                        f"| {ep.get('period', '時期不明')} | "
                        f"{ep.get('title', '不明')} | "
                        f"{ep.get('impact', '-')} |"
                    )
                content.append("")

        self.save_index(content, "episode-timeline.md")