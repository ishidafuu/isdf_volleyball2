# Git運用ルール

## 1. ブランチ戦略
### メインブランチ
- `main`: プロダクションブランチ

### 作業用ブランチ
- 特に作成せず、指示がない限りmainブランチのみでの運用とする

## 2. コミットメッセージ規約
### 基本ルール
- 日本語で1行
- 簡潔に要点のみ記載

### コミットメッセージ例
```
データベースのcharactersテーブルにニックネームカラムを追加
キャラクターの基本能力値を更新
エピソードファイルのフォーマットを修正
ドキュメントの誤字を修正
```

## 3. コミット手順
   ```bash
   # リポジトリパス: /users/ishida/documents/isdf_volleyball2
   git checkout main
   git pull origin main
   git add .
   git commit -m "コミットメッセージ"
   ```

## 4. 注意事項
- コミットは論理的な単位で行う
- バイナリファイルのコミットは最小限に抑える
- コンフリクトが発生した場合は、関係者と相談の上で解決する

## 5. プロジェクト情報
- リポジトリパス: `/users/ishida/documents/isdf_volleyball2`