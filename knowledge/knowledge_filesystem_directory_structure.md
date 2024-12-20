# ファイルシステムディレクトリ構造ガイドライン

## 1. ルートディレクトリ構造

```
/isdf_volleyball2/
├── abilities/              # 能力値関連ファイル
├── episodes/               # エピソード関連ファイル
├── individual-characters/  # キャラクター個別プロファイル
├── manager/               # 管理者関連ファイル
├── personality/           # 性格特性関連ファイル
├── templates/             # 各種テンプレート
└── knowledge/             # ナレッジベース・ドキュメント
```

## 2. 各ディレクトリの構造と目的

### 2.1 abilities/
能力値定義と管理のためのディレクトリ
```
abilities/
├── abilities-structure.txt    # 能力値体系の定義
├── attack_skills/            # 攻撃技能
│   ├── basic_attacks.yml     # 基本攻撃定義
│   ├── combinations.yml      # コンビネーション攻撃定義
│   ├── moving_attacks.yml    # 移動攻撃定義
│   └── position_attacks.yml  # ポジション別攻撃定義
├── basic_abilities/          # 基礎能力定義
├── defense_skills/           # 防御技能定義
├── movement_skills/          # 移動技能定義
├── serve_skills/             # サーブ技能定義
├── setting_skills/           # セッター技能定義
└── team_skill/              # チーム技能定義
```

### 2.2 episodes/
キャラクターやチームに関するエピソード管理
```
episodes/
├── characters/              # キャラクター別エピソード
├── districts/              # 地区別エピソード
├── matches_middle_school/  # 中学校試合関連エピソード
├── matches_school/         # 高校試合関連エピソード
├── middle_schools/         # 中学校別エピソード
└── schools/               # 高校別エピソード
```

### 2.3 individual-characters/
キャラクター個別のプロファイル情報
```
individual-characters/
└── chr_{school_code}{number}_profile.md
```

### 2.4 manager/
システム管理用ファイル
```
manager/
└── [管理用ファイル群]
```

### 2.5 personality/
キャラクターの性格特性定義
```
personality/
└── [性格特性関連ファイル群]
```

### 2.6 templates/
各種テンプレートファイル
```
templates/
└── [テンプレートファイル群]
```

## 3. ディレクトリ構造の制約事項

### 3.1 変更禁止の構造
以下の構造は設計上重要な意味を持つため、変更禁止：
- キャラクター分類構造
- 学校区分構造（中学/高校）
- 試合区分構造（中学/高校）
- 地区分類構造
- 能力値カテゴリ構造

### 3.2 ディレクトリ階層の制限
- 最大階層深度: 4階層まで
- 各ディレクトリの役割を明確に維持すること
- 新規ディレクトリ作成時は承認必須

## 4. 運用ガイドライン

### 4.1 ディレクトリ作成時の注意点
- 目的に応じた適切な配置
- 命名規則の遵守
- 既存構造との整合性確認

### 4.2 構造変更時の注意点
- 影響範囲の事前確認
- 関連ファイルの移動計画
- データベースとの整合性確認

### 4.3 禁止事項
- 規定外のディレクトリの作成
- 既存ディレクトリの用途変更
- 構造の独自拡張
- 一時的なディレクトリの作成

## 5. 構造変更の手順

### 5.1 変更提案時の必要事項
- 変更目的の明確化
- 影響範囲の特定
- 移行計画の策定
- リスク評価

### 5.2 実施承認の条件
- 既存データの整合性維持
- システム全体への影響の最小化
- 運用への影響の考慮
- ドキュメントの更新計画