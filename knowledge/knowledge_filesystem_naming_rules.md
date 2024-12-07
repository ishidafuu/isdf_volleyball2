# ファイルシステム命名規則

## 1. 基本原則

### 1.1 命名の共通規則
- スネークケースまたはケバブケースを使用
- 意味のある名前を使用
- 英数字のみを使用
- 特殊文字は原則として使用禁止（ハイフンとアンダースコアを除く）

## 2. ディレクトリ命名規則

### 2.1 エピソードディレクトリ
- 時系列ディレクトリ: `{N}_years_ago`
  * 例: `1_year_ago`, `2_years_ago`, `3_years_ago`
- サブカテゴリディレクトリ:
  * 学校別: `schools`
  * キャラクター別: `characters`
  * 試合別: `matches`
  * 地区別: `districts`

### 2.2 学校関連ディレクトリ
- フォーマット: `jhs_{school_code}_{number}`
- school_code: DBのjunior_high_schools.idに基づく
- 例:
  * `jhs_sakurada_01`
  * `jhs_aoba_01`
  * `jhs_teito_01`

## 3. ファイル命名規則

### 3.1 エピソードファイル
基本形式: `eps_{timeline}_{category}_{identifier}.md`

構成要素:
- timeline: 時系列識別子（例: 3ya, 2ya, 1ya）
- category: コンテンツ種別
  * chr: キャラクター関連
  * sch: 学校関連
  * mch: 試合関連
  * dst: 地区関連
- identifier: 識別用の説明的な名前

例:
- `eps_3ya_chr_kuga_brothers.md`
- `eps_3ya_sch_sakurada_alumni.md`
- `eps_3ya_mch_finals.md`
- `eps_3ya_dst_aoba_history.md`

### 3.2 キャラクタープロファイル
フォーマット: `chr_{school_code}{number}_profile.md`

- school_code: 学校コード（2文字）
  * ao: 青葉中学校
  * hi: 光丘中学校
  * og: 大原中学校
  * se: 誠心中学校
  * sk: 桜田中学校
  * so: 蒼陽中学校
  * tk: 帝都中学校
  * to: 東陵中学校
- number: 2桁の連番（01-08）

例:
- `chr_sk01_profile.md`
- `chr_ao02_profile.md`

### 3.3 能力値関連ファイル
- YAMLファイル: スネークケース使用
  * 例: `basic_attacks.yml`, `combinations.yml`
- 構造定義ファイル: ケバブケース使用
  * 例: `abilities-structure.txt`

## 4. 禁止事項

### 4.1 絶対に使用してはいけない要素
- 空白文字
- 日本語文字
- 特殊文字（ハイフンとアンダースコア以外）
- 大文字（既存の規約がある場合を除く）
- 拡張子の省略
- 連続するアンダースコアやハイフン

### 4.2 避けるべきパターン
- 意味不明な略語
- 一貫性のない命名パターン
- 数字のみの識別子
- 過度に長いファイル名（50文字以上）

## 5. 命名時の注意事項

### 5.1 確認事項
- 既存の命名パターンとの整合性
- データベース上のIDとの一致（該当する場合）
- カテゴリ識別子の適切な使用
- タイムライン識別子の正確な指定

### 5.2 命名変更時の手順
1. 既存の参照関係の確認
2. データベースとの整合性確認
3. 変更影響範囲の特定
4. 関連ファイルの更新計画作成
5. 一括変更の実施
6. 変更結果の検証