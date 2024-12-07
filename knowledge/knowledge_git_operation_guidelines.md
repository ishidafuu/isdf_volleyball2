# Git運用ルール

## 1. ブランチ戦略
### メインブランチ
- `main`: プロダクションブランチ。常に安定した状態を維持

### 作業用ブランチ
- `feature/{作業内容}`: 機能追加・修正用
- `fix/{修正内容}`: バグ修正用
- `docs/{文書名}`: ドキュメント更新用

## 2. ブランチ運用フロー
1. mainブランチから作業用ブランチを作成
2. 作業用ブランチで開発を実施
3. 作業完了後、mainブランチにマージ

## 3. コミットメッセージ規約
### 基本ルール
- 日本語で1行
- 動詞で開始
- 簡潔に要点のみ記載

### コミットメッセージ例
```
データベースのcharactersテーブルにニックネームカラムを追加
キャラクターの基本能力値を更新
エピソードファイルのフォーマットを修正
ドキュメントの誤字を修正
```

## 4. 作業手順
1. 作業前にmainブランチを最新化
   ```bash
   git checkout main
   git pull origin main
   ```

2. 作業用ブランチを作成
   ```bash
   git checkout -b feature/作業内容
   ```

3. 作業完了後、変更をコミット
   ```bash
   git add .
   git commit -m "コミットメッセージ"
   ```

4. mainブランチにマージ
   ```bash
   git checkout main
   git merge feature/作業内容
   ```

## 5. 注意事項
- コミットは論理的な単位で行う
- バイナリファイルのコミットは最小限に抑える
- コンフリクトが発生した場合は、関係者と相談の上で解決する
- 不要になったブランチは適宜削除する