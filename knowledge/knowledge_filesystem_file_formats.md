# ファイルフォーマット規約

## 1. 共通規則

### 1.1 基本要件
- 文字エンコーディング: UTF-8
- 改行コード: LF (Line Feed)
- ファイル末尾に空行を1行入れること
- BOMは使用しない

### 1.2 ファイル拡張子
- Markdown: `.md`
- YAML: `.yml`
- テキスト: `.txt`
- データベース: `.db`

## 2. Markdownファイル規約

### 2.1 エピソードファイル
```markdown
# [エピソードタイトル]

## 概要
[エピソードの簡潔な説明]

## 登場人物
- [キャラクター名]: [エピソードでの役割]

## 詳細
[エピソードの詳細な内容]

## 関連情報
- 関連キャラクター: [関連するキャラクター]
- 関連エピソード: [関連するエピソード]
```

### 2.2 キャラクタープロファイル
```markdown
# [キャラクター名]

## 基本情報
- 所属: [学校名]
- ポジション: [ポジション]
- 学年: [学年]

## キャラクター詳細
[キャラクターの詳細情報]

## 特徴
[キャラクターの特徴]
```

## 3. YAMLファイル規約

### 3.1 能力値定義ファイル
```yaml
# 基本構造
skill_type:
  name: スキル名
  description: 説明
  properties:
    property1: 値
    property2: 値
```

### 3.2 インデント規則
- スペース2文字を使用
- タブ文字は使用禁止
- 配列要素は同じレベルでインデント

## 4. テキストファイル規約

### 4.1 設定ファイル
- 1行1項目の形式
- コメントは#で開始
- 空行による項目の区切り

### 4.2 データファイル
- カンマ区切り形式の場合はCSVとして保存
- 固定長形式の場合は項目長を明記

## 5. 禁止事項

### 5.1 ファイル形式
- HTMLファイルの使用
- バイナリファイルの使用
- エクセルなどの独自形式ファイル
- 実行可能ファイル

### 5.2 命名規則に関する禁止事項
- 空白文字の使用
- 日本語ファイル名
- 特殊文字の使用
- 拡張子の省略

## 6. 作業時の注意点

### 6.1 ファイル作成時
- 適切なテンプレートの使用
- 文字コードの確認
- 改行コードの確認
- 不要な空白行・空白文字の削除

### 6.2 ファイル更新時
- 既存フォーマットの踏襲
- インデントの統一
- 文字コードの維持
- フォーマットの一貫性確保