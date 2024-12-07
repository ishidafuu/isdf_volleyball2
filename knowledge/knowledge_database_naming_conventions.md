# データベース命名規則ガイドライン

## 1. 基本原則

### 1.1 命名の一般規則
- スネークケース（小文字、アンダースコア区切り）を使用
- 略語は原則として使用しない
- 予約語は使用しない
- 意味のある名前を使用すること

## 2. テーブル名規則

### 2.1 基本形式
- 複数形を使用
- 小文字のスネークケース
- プレフィックス・サフィックスは使用しない

### 2.2 命名例
良い例：
- characters
- junior_high_schools
- team_members
- match_results

避けるべき例：
- character （単数形）
- JuniorHighSchools （パスカルケース）
- TEAM_MEMBERS （大文字）
- tbl_match_results （不要なプレフィックス）

## 3. カラム名規則

### 3.1 基本規則
- スネークケースを使用
- プレフィックスは機能的に必要な場合のみ使用
- 一貫性のある命名パターンを使用

### 3.2 特別な規則
ID関連：
- 主キー: `{テーブル名の単数形}_id`
- 外部キー: `{参照先テーブル名の単数形}_id`

### 3.3 命名例
良い例：
- character_id
- school_id
- first_name
- last_name
- team_name

避けるべき例：
- id （具体性に欠ける）
- CharacterId （パスカルケース）
- character_number （IDを意味する場合）
- schoolId （キャメルケース）

## 4. インデックス名規則

### 4.1 基本形式
- idx_{テーブル名}_{カラム名}
- unq_{テーブル名}_{カラム名}（一意インデックス）
- fk_{参照元テーブル}_{参照先テーブル}（外部キー）

### 4.2 命名例
- idx_characters_last_name
- unq_schools_school_code
- fk_team_members_characters

## 5. 制約名規則

### 5.1 基本形式
- pk_{テーブル名} （主キー制約）
- fk_{テーブル名}_{参照先テーブル名} （外部キー制約）
- uq_{テーブル名}_{カラム名} （一意性制約）
- ck_{テーブル名}_{制約内容} （チェック制約）

### 5.2 命名例
- pk_characters
- fk_team_members_teams
- uq_schools_school_code
- ck_characters_valid_status

## 6. 禁止事項

### 6.1 使用禁止の要素
- スペース
- 特殊文字
- アルファベット以外の文字
- 予約語
- 2バイト文字

### 6.2 避けるべきパターン
- 意味不明な略語
- 一貫性のない複数形/単数形
- テーブル種類を示すプレフィックス（tbl_, mst_等）
- 用途不明な数字サフィックス