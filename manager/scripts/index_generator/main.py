from pathlib import Path
from character_manager.scripts.index_generator.character_map import CharacterMapGenerator
from character_manager.scripts.index_generator.crossover_map import CrossoverMapGenerator
from character_manager.scripts.index_generator.episode_timeline import EpisodeTimelineGenerator
from character_manager.scripts.index_generator.growth_map import GrowthMapGenerator
from character_manager.scripts.index_generator.relationship_map import RelationshipMapGenerator

def main():
    base_path = Path("characters")

    # 各インデックス生成器のインスタンス化と実行
    generators = [
        CharacterMapGenerator(base_path),
        CrossoverMapGenerator(base_path),
        GrowthMapGenerator(base_path),
        EpisodeTimelineGenerator(base_path),
        RelationshipMapGenerator(base_path),
    ]

    # 全インデックスの生成
    for generator in generators:
        generator.generate()


if __name__ == "__main__":
    main()