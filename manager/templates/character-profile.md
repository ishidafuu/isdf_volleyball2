---
# Character Profile Template
version: 1.0.0
last_updated: YYYY-MM-DD
status: draft|review|final

# Basic Information
character_id: XX-00  # School code (2 chars) + Number (2 digits)
name:
  given: ""  # 名前
  family: ""  # 苗字
  full: ""   # フルネーム
  reading: "" # フリガナ

# Core Stats
year: 1|2|3  # 学年
position: WSP|MB|S|L|OPP  # ポジション
height: 000  # 身長(cm)
team: ""     # 所属チーム
previous_team: ""  # 前所属（中学校）
previous_club: ""  # 前所属部活

# Abilities (S|A|B|C)
abilities:
  attack: 
  receive: 
  serve: 
  block: 
  stamina: 
  technique: 

# Personality Traits (1-5 scale)
personality:
  normal:
    openness: 0     # 開放性
    conscientiousness: 0  # 誠実性
    extraversion: 0    # 外向性
    agreeableness: 0   # 協調性
    neuroticism: 0     # 神経症的傾向
  under_pressure:
    openness: 0
    conscientiousness: 0
    extraversion: 0
    agreeableness: 0
    neuroticism: 0

# Tags for filtering and categorization
tags:
  - tag1
  - tag2

# Related files
related_files:
  - path/to/related/file1.md
  - path/to/related/file2.md
---

# {character_name}（{character_name_reading}）

## 基本情報
- ID: {character_id}
- 学年：{year}年
- ポジション：{position}
- 身長：{height}cm
- 所属：{team}
- 出身：{previous_team}（{previous_club}）

## 能力値
- 攻撃力：{abilities.attack}
- レシーブ：{abilities.receive}
- サーブ：{abilities.serve}
- ブロック：{abilities.block}
- スタミナ：{abilities.stamina}
- テクニック：{abilities.technique}

## 性格分析（ビッグファイブ）

### 平常時の性格
- **開放性**: {personality.normal.openness}
  * 特徴：[開放性の特徴を説明]
  * 表現：[具体的な表れ方]

- **誠実性**: {personality.normal.conscientiousness}
  * 特徴：[誠実性の特徴を説明]
  * 表現：[具体的な表れ方]

- **外向性**: {personality.normal.extraversion}
  * 特徴：[外向性の特徴を説明]
  * 表現：[具体的な表れ方]

- **協調性**: {personality.normal.agreeableness}
  * 特徴：[協調性の特徴を説明]
  * 表現：[具体的な表れ方]

- **神経症的傾向**: {personality.normal.neuroticism}
  * 特徴：[神経症的傾向の特徴を説明]
  * 表現：[具体的な表れ方]

### ピンチ時の性格（本質的性格）
- **開放性**: {personality.under_pressure.openness}
  * 特徴：[開放性の特徴を説明]
  * 表現：[具体的な表れ方]

- **誠実性**: {personality.under_pressure.conscientiousness}
  * 特徴：[誠実性の特徴を説明]
  * 表現：[具体的な表れ方]

- **外向性**: {personality.under_pressure.extraversion}
  * 特徴：[外向性の特徴を説明]
  * 表現：[具体的な表れ方]

- **協調性**: {personality.under_pressure.agreeableness}
  * 特徴：[協調性の特徴を説明]
  * 表現：[具体的な表れ方]

- **神経症的傾向**: {personality.under_pressure.neuroticism}
  * 特徴：[神経症的傾向の特徴を説明]
  * 表現：[具体的な表れ方]

## 性格・特徴
### 性格
[性格の詳細な説明]

### 特徴的な要素
[特徴的な要素の説明]

## 来歴
### 中学時代
[中学時代の詳細]

### 高校での成長
[高校でのエピソード]

## キャリア
[主な実績や経験]

## 人間関係
### 家族関係
[家族との関係]

### チーム内
[チームメイトとの関係]

### ライバル
[ライバルとの関係]

## 特記事項
[その他の重要な情報]
