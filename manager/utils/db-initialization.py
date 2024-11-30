import sqlite3
import os
from pathlib import Path

def initialize_database(db_path: str):
    """データベースの初期化とテーブル作成を行う"""
    
    # データベースディレクトリの確認と作成
    db_dir = os.path.dirname(db_path)
    if db_dir:
        Path(db_dir).mkdir(parents=True, exist_ok=True)

    # データベース接続
    with sqlite3.connect(db_path) as conn:
        # キャラクター基本情報テーブル
        conn.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id TEXT PRIMARY KEY,
                name_given TEXT,
                name_family TEXT,
                name_full TEXT,
                name_reading TEXT,
                year INTEGER,
                position TEXT,
                height INTEGER,
                team TEXT,
                previous_team TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # キャラクター能力値テーブル
        conn.execute("""
            CREATE TABLE IF NOT EXISTS abilities (
                character_id TEXT PRIMARY KEY,
                attack TEXT,
                receive TEXT,
                serve TEXT,
                block TEXT,
                stamina TEXT,
                technique TEXT,
                FOREIGN KEY(character_id) REFERENCES characters(id)
            )
        """)

        # エピソードテーブル
        conn.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                id TEXT PRIMARY KEY,
                title TEXT,
                episode_type TEXT,
                content_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # キャラクター・エピソード関連テーブル
        conn.execute("""
            CREATE TABLE IF NOT EXISTS character_episodes (
                character_id TEXT,
                episode_id TEXT,
                role TEXT,
                FOREIGN KEY(character_id) REFERENCES characters(id),
                FOREIGN KEY(episode_id) REFERENCES episodes(id),
                PRIMARY KEY(character_id, episode_id)
            )
        """)

        # キャラクター関係性テーブル
        conn.execute("""
            CREATE TABLE IF NOT EXISTS character_relationships (
                character_id1 TEXT,
                character_id2 TEXT,
                relationship_type TEXT,
                description TEXT,
                FOREIGN KEY(character_id1) REFERENCES characters(id),
                FOREIGN KEY(character_id2) REFERENCES characters(id),
                PRIMARY KEY(character_id1, character_id2)
            )
        """)

        # インデックスの作成
        conn.execute("CREATE INDEX IF NOT EXISTS idx_episodes_title ON episodes(title)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_characters_name ON characters(name_full)")

        print("Database initialized successfully!")

if __name__ == "__main__":
    # データベースパスの設定
    DB_PATH = "isdf_volleyball.db"
    
    # データベースの初期化
    initialize_database(DB_PATH)
