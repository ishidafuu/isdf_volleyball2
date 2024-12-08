# エピソード管理ワークフロー

## 0. 概要と目的

### 0.1 ワークフローの目的
このワークフローは以下の目的を達成するために設計されています：

1. 物語の整合性維持
   - 時系列の一貫性確保
   - キャラクターの成長過程の追跡
   - 学校/チームの発展の記録

2. データの関連性管理
   - キャラクター間の関係性の明確化
   - エピソード間の因果関係の把握
   - 影響関係の追跡可能性の確保

3. 分析基盤の確立
   - キャラクターの成長ポイントの記録
   - 学校/チームの特色の変遷の追跡
   - ストーリーラインの分析

### 0.2 システム要件
1. データの一貫性
   - キャラクター情報の統一的な管理
   - 時系列情報の正確な記録
   - 関連性情報の確実な維持

2. 拡張性
   - 新規エピソードの追加容易性
   - 関連情報の柔軟な拡張
   - 分析視点の追加可能性

3. 検索性
   - キャラクター視点での検索
   - 時系列での検索
   - テーマ/カテゴリでの検索

## 1. エピソード作成の基本フロー

### 1.1 前提確認
目的：新規エピソードの整合性確保と重複防止

1. 既存エピソードの確認
   - 目的：関連エピソードの把握と整合性チェック
   ```sql
   -- 関連エピソードの検索
   SELECT id, title, timeline, category 
   FROM episodes 
   WHERE timeline = '{timeline}' 
   OR category = '{category}';
   ```

2. 必要な参照情報の収集
   - 目的：登場キャラクターと関連情報の正確な紐付け
   ```sql
   -- キャラクター情報の確認
   SELECT * FROM characters 
   WHERE name = '{character_name}';
   ```

### 1.2 エピソードファイル作成
目的：一貫性のある形式でのエピソード保存と管理

1. 配置場所の決定
   - 目的：時系列とカテゴリに基づく整理された構造の維持
   ```
   episodes/
   ├── 3_years_ago/  # 3年前の出来事
   ├── 2_years_ago/  # 2年前の出来事
   ├── 1_year_ago/   # 1年前の出来事
   └── current/      # 現在の出来事
   ```

### 1.3 データベース登録
目的：検索可能な形でのエピソード情報の保存

1. episodesテーブルへの登録
   - 目的：エピソードの基本情報の記録
   ```sql
   INSERT INTO episodes (
     id, title, episode_type, content_path, 
     timeline, category, school_type, summary
   ) VALUES (...);
   ```

2. 関連テーブルの更新
   - 目的：キャラクターへの影響と関連性の記録
   ```sql
   -- キャラクターの役割と影響を記録
   INSERT INTO episode_characters (...) VALUES (...);
   ```

## 2. データ整合性の確認

### 2.1 キャラクター名の表記確認
目的：キャラクター情報の一貫性確保

1. 表記揺れチェック
   - 目的：キャラクター名の統一的な管理
   ```sql
   SELECT character_name, COUNT(*) as count
   FROM episode_characters 
   GROUP BY character_name
   HAVING count > 1;
   ```

### 2.2 関連性の整合性チェック
目的：エピソード間の関連付けの完全性確保

1. 孤立エピソードの確認
   ```sql
   -- 関連付けのないエピソードの検出
   SELECT e.id, e.title
   FROM episodes e
   LEFT JOIN episode_relations r 
   ON e.id = r.source_episode_id
   WHERE r.source_episode_id IS NULL;
   ```

2. 双方向関連付けの確認
   ```sql
   -- 片方向のみの関連付けを検出
   SELECT r1.source_episode_id, r1.target_episode_id
   FROM episode_relations r1
   LEFT JOIN episode_relations r2
   ON r1.source_episode_id = r2.target_episode_id
   AND r1.target_episode_id = r2.source_episode_id
   WHERE r2.source_episode_id IS NULL;
   ```

## 3. エピソード間の関連付け

### 3.1 関連付けの種類と目的
1. 直接的な関連（parallel）
   - 同一イベントの異なる視点
   例：帝都中戦の各視点
   ```sql
   -- 例：帝都中戦での異なる視点の関連付け
   INSERT INTO episode_relations VALUES
   ('eps_chr_igarashi_evolution', 
    'eps_chr_segawa_asahi_observation',
    'parallel', 
    '帝都中戦での五十嵐と朝陽の異なる視点');
   ```

2. 参照関連（reference）
   - 背景情報や影響関係
   - 同一テーマの異なるエピソード
   例：兄弟の物語、学校の特色
   ```sql
   -- 例：兄弟エピソードの関連付け
   INSERT INTO episode_relations VALUES
   ('eps_chr_kuga_brothers',
    'eps_chr_takayama_brothers',
    'reference',
    '異なる兄弟の進路選択と成長の対比');
   ```

3. 時系列関連（今後の拡張予定）
   - sequel: 後続イベント
   - prequel: 先行イベント

### 3.2 関連付けの実装ガイドライン

1. 基本原則
   - 常に双方向の関連付けを行う
   - 適切な relation_type を選択
   - 具体的な description を設定

2. 典型的なパターン
   a. 試合エピソードと個人視点
      ```sql
      -- メインの試合エピソードと選手視点の関連付け
      INSERT INTO episode_relations VALUES
      ('eps_mch_main_match', 'eps_chr_player_view', 
       'parallel', '試合の全体像と選手個人の視点'),
      ('eps_chr_player_view', 'eps_mch_main_match',
       'parallel', '選手視点と試合の全体像');
      ```

   b. 学校/チームの特色関連
      ```sql
      -- 学校の特色と実践例の関連付け
      INSERT INTO episode_relations VALUES
      ('eps_msc_school_style', 'eps_mch_practice_match',
       'reference', '学校の特色とその実践例'),
      ('eps_mch_practice_match', 'eps_msc_school_style',
       'reference', '実践例と学校の特色');
      ```

## 4. 検証とメンテナンス

### 4.1 定期的な検証
目的：データの品質維持と整合性確保

1. 基本チェック項目
   - summary未設定のエピソード
   - 孤立したエピソード
   - 片方向の関連付け

2. 関連性の検証
   ```sql
   -- relation_typeの使用状況確認
   SELECT relation_type, COUNT(*) as count
   FROM episode_relations
   GROUP BY relation_type;
   ```

### 4.2 メンテナンス手順
目的：システムの持続的な運用と改善

1. データクリーンアップ
   - 未使用データの特定と整理
   - 重複データの統合
   - 過去データの整理

2. システム改善
   - relation_typeの拡張検討
   - 関連性の強度表現の検討
   - 検索機能の強化
