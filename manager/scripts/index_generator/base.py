from pathlib import Path
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any
import frontmatter
from datetime import datetime

class BaseIndexGenerator(ABC):
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.indexes_dir = base_path / "_indexes"
        self.characters_dir = base_path / "individual-characters"
        self.relationships_dir = base_path / "relationships"
        self.episodes_dir = base_path / "episodes"
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

    def read_episode_data(self) -> List[Dict[str, Any]]:
        """全エピソードデータの読み込み"""
        episodes = []
        for episode_file in self.episodes_dir.glob("**/*.md"):
            try:
                post = frontmatter.load(episode_file)
                episode_data = post.metadata
                episode_data['content'] = post.content
                episode_data['file_path'] = str(episode_file.relative_to(self.base_path))
                episodes.append(episode_data)
            except Exception as e:
                self.logger.error(f"Error reading {episode_file}: {e}")
        return episodes

    def read_relationship_data(self) -> List[Dict[str, Any]]:
        """全関係性データの読み込み"""
        relationships = []
        for rel_file in self.relationships_dir.glob("**/*.md"):
            try:
                post = frontmatter.load(rel_file)
                rel_data = post.metadata
                rel_data['content'] = post.content
                rel_data['file_path'] = str(rel_file.relative_to(self.base_path))
                relationships.append(rel_data)
            except Exception as e:
                self.logger.error(f"Error reading {rel_file}: {e}")
        return relationships

    def get_teams(self) -> List[str]:
        """全チームの取得"""
        chars = self.read_character_data()
        return sorted(list(set(char.get('team', '') for char in chars if char.get('team'))))

    def get_team_characters(self, team: str) -> List[Dict[str, Any]]:
        """チームに所属するキャラクターの取得"""
        chars = self.read_character_data()
        return [char for char in chars if char.get('team') == team]

    def get_main_characters(self) -> List[Dict[str, Any]]:
        """主要キャラクターの取得"""
        chars = self.read_character_data()
        # タグや特定の条件で主要キャラクターを判断
        return [char for char in chars if 'main_character' in char.get('tags', [])]

    def get_character_episodes(self, character_id: str) -> List[Dict[str, Any]]:
        """キャラクターに関連するエピソードの取得"""
        episodes = self.read_episode_data()
        return [ep for ep in episodes if character_id in ep.get('characters', {}).get('primary', [])]

    def get_joint_events(self) -> List[Dict[str, Any]]:
        """合同イベントの取得"""
        episodes = self.read_episode_data()
        return [ep for ep in episodes if len(set(ep.get('teams', []))) > 1]

    def get_crossover_types(self) -> List[str]:
        """クロスオーバーイベントの種類取得"""
        episodes = self.read_episode_data()
        return sorted(list(set(ep.get('crossover_type', '') for ep in episodes if ep.get('crossover_type'))))

    def get_crossover_events(self, event_type: str) -> List[Dict[str, Any]]:
        """特定種類のクロスオーバーイベント取得"""
        episodes = self.read_episode_data()
        return [ep for ep in episodes if ep.get('crossover_type') == event_type]

    def get_time_periods(self) -> List[str]:
        """時系列区分の取得"""
        episodes = self.read_episode_data()
        return sorted(list(set(ep.get('period', '') for ep in episodes if ep.get('period'))))

    def get_episodes_by_period(self, period: str) -> List[Dict[str, Any]]:
        """特定期間のエピソード取得"""
        episodes = self.read_episode_data()
        return [ep for ep in episodes if ep.get('period') == period]

    def get_skill_types(self) -> List[str]:
        """技能タイプの取得"""
        return [
            "アタック系",
            "レシーブ系",
            "サーブ系",
            "ブロック系",
            "トス系",
            "基礎技能系"
        ]

    def get_skills_by_type(self, skill_type: str) -> List[Dict[str, Any]]:
        """特定タイプの技能リスト取得"""
        # この部分は実際のデータ構造に合わせて実装
        skill_data = {
            "アタック系": [
                {
                    "id": "attack_basic",
                    "name": "基本スパイク",
                    "prerequisites": []
                },
                {
                    "id": "attack_quick",
                    "name": "クイック",
                    "prerequisites": [
                        {"id": "attack_basic", "name": "基本スパイク"}
                    ]
                }
            ],
            "レシーブ系": [
                {
                    "id": "receive_basic",
                    "name": "基本レシーブ",
                    "prerequisites": []
                },
                {
                    "id": "receive_rolling",
                    "name": "ローリングレシーブ",
                    "prerequisites": [
                        {"id": "receive_basic", "name": "基本レシーブ"}
                    ]
                }
            ],
            # 他の技能タイプも同様に定義
        }
        return skill_data.get(skill_type, [])

    def get_character_growth_events(self, character_id: str) -> List[Dict[str, Any]]:
        """キャラクターの成長イベント取得"""
        episodes = self.read_episode_data()
        growth_events = []

        for ep in episodes:
            if character_id in ep.get('characters', {}).get('primary', []):
                if 'growth' in ep.get('tags', []):
                    growth_events.append({
                        'title': ep.get('title', '不明なイベント'),
                        'growth_type': ep.get('growth_type', '一般的な成長'),
                        'period': ep.get('period', '時期不明'),
                        'impact': ep.get('impact', ''),
                        'related_skills': ep.get('related_skills', [])
                    })

        return sorted(growth_events, key=lambda x: x['period'])

    def get_influence_relationships(self) -> Dict[str, List[Dict[str, Any]]]:
        """影響関係の取得"""
        relationships = self.read_relationship_data()
        influence_map = {
            "技術指導": [],
            "精神的影響": [],
            "ライバル関係": [],
            "チーム関係": []
        }

        for rel in relationships:
            if 'influence_type' in rel:
                influence_map[rel.get('influence_type', 'その他')].append({
                    'from': rel.get('from_character', ''),
                    'to': rel.get('to_character', ''),
                    'content': rel.get('influence_content', ''),
                    'result': rel.get('influence_result', '')
                })

        return influence_map

    def get_major_events(self) -> List[Dict[str, Any]]:
        """重要イベントの取得"""
        episodes = self.read_episode_data()
        major_events = []

        for ep in episodes:
            if 'major_event' in ep.get('tags', []):
                major_events.append({
                    'title': ep.get('title', '不明なイベント'),
                    'period': ep.get('period', '時期不明'),
                    'participants': self._get_participant_names(ep.get('characters', {}).get('primary', [])),
                    'impact': ep.get('impact', '影響不明')
                })

        return sorted(major_events, key=lambda x: x['period'])

    def _get_participant_names(self, character_ids: List[str]) -> List[str]:
        """キャラクターIDから名前のリストを取得"""
        characters = self.read_character_data()
        id_to_name = {
            char.get('character_id'): char.get('name', {}).get('full', 'Unknown')
            for char in characters
        }
        return [id_to_name.get(char_id, 'Unknown') for char_id in character_ids]

    def get_episodes_by_period(self, period: str) -> List[Dict[str, Any]]:
        """特定期間のエピソード取得"""
        episodes = self.read_episode_data()
        period_episodes = []

        for ep in episodes:
            if ep.get('period') == period:
                period_episodes.append({
                    'title': ep.get('title', '不明なエピソード'),
                    'participants': self._get_participant_names(ep.get('characters', {}).get('primary', [])),
                    'impact': ep.get('impact', ''),
                    'tags': ep.get('tags', [])
                })

        return period_episodes

    def get_rival_relationships(self) -> List[Dict[str, Any]]:
        """ライバル関係の取得"""
        relationships = self.read_relationship_data()
        rival_rels = []

        for rel in relationships:
            if rel.get('relationship_type') == 'rival':
                # 双方向の関係性を作成
                participants = rel.get('participants', [])
                if len(participants) >= 2:
                    rival_rels.append({
                        'from_id': participants[0].get('character_id'),
                        'from_name': self._get_character_name(participants[0].get('character_id')),
                        'to_id': participants[1].get('character_id'),
                        'to_name': self._get_character_name(participants[1].get('character_id')),
                        'type': rel.get('rivalry_type', 'ライバル')
                    })

        return rival_rels

    def get_sibling_relationships(self) -> List[Dict[str, Any]]:
        """兄弟関係の取得"""
        relationships = self.read_relationship_data()
        sibling_rels = []

        for rel in relationships:
            if rel.get('relationship_type') == 'sibling':
                participants = rel.get('participants', [])
                if len(participants) >= 2:
                    names = [
                        self._get_character_name(p.get('character_id'))
                        for p in participants
                    ]
                    sibling_rels.append({
                        'description': f"{' と '.join(names)}は兄弟",
                        'details': rel.get('details', '')
                    })

        return sibling_rels

    def get_childhood_friend_relationships(self) -> List[Dict[str, Any]]:
        """幼なじみ関係の取得"""
        relationships = self.read_relationship_data()
        childhood_rels = []

        for rel in relationships:
            if rel.get('relationship_type') == 'childhood_friend':
                participants = rel.get('participants', [])
                if len(participants) >= 2:
                    names = [
                        self._get_character_name(p.get('character_id'))
                        for p in participants
                    ]
                    childhood_rels.append({
                        'description': f"{' と '.join(names)}は幼なじみ",
                        'details': rel.get('details', '')
                    })

        return childhood_rels

    def get_mentor_relationships(self) -> List[Dict[str, Any]]:
        """師弟関係の取得"""
        relationships = self.read_relationship_data()
        mentor_rels = []

        for rel in relationships:
            if rel.get('relationship_type') == 'mentor':
                participants = rel.get('participants', [])
                if len(participants) >= 2:
                    mentor = self._get_character_name(participants[0].get('character_id'))
                    student = self._get_character_name(participants[1].get('character_id'))
                    mentor_rels.append({
                        'description': f"{mentor}は{student}の指導者",
                        'details': rel.get('details', '')
                    })

        return mentor_rels

    def filter_team_relationships(self, team_chars: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """チーム内の関係性を抽出"""
        relationships = self.read_relationship_data()
        team_rels = []
        team_char_ids = {char.get('character_id') for char in team_chars}

        for rel in relationships:
            participants = rel.get('participants', [])
            if len(participants) >= 2:
                char1_id = participants[0].get('character_id')
                char2_id = participants[1].get('character_id')

                if char1_id in team_char_ids and char2_id in team_char_ids:
                    team_rels.append({
                        'from_id': char1_id,
                        'from_name': self._get_character_name(char1_id),
                        'to_id': char2_id,
                        'to_name': self._get_character_name(char2_id),
                        'type': rel.get('relationship_type', '関係')
                    })

        return team_rels

    def _get_character_name(self, character_id: str) -> str:
        """キャラクターIDから名前を取得"""
        characters = self.read_character_data()
        for char in characters:
            if char.get('character_id') == character_id:
                return char.get('name', {}).get('full', 'Unknown')
        return 'Unknown'

    @abstractmethod
    def generate(self) -> None:
        """インデックス生成の実装（サブクラスで必須実装）"""
        pass

    def create_header(self, title: str) -> List[str]:
        """共通のヘッダー部分の生成"""
        return [
            "---",
            "version: 1.0.0",
            f"last_updated: {datetime.now().strftime('%Y-%m-%d')}",
            "status: generated",
            "---",
            "",
            f"# {title}",
            ""
        ]

    def save_index(self, content: List[str], filename: str) -> None:
        """インデックスファイルの保存"""
        output_path = self.indexes_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        self.logger.info(f"Generated index: {output_path}")