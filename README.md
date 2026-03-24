# TaskFlow

シンプルなタスク管理CLIツール。

## インストール

```bash
pip install -e .
```

## 使い方

### タスクを追加する

```bash
taskflow add "買い物をする"
taskflow add "レポートを書く" --description "月次レポートの作成"
```

### タスク一覧を表示する

```bash
taskflow list
```

出力例:

```
[ ] a1b2c3d4-... - 買い物をする
[ ] e5f6g7h8-... - レポートを書く
    月次レポートの作成
```

### タスクを完了にする

```bash
taskflow done <task_id>
```

### タスクを削除する

```bash
taskflow delete <task_id>
```

## データの保存場所

タスクデータはデフォルトで `~/.taskflow/tasks.json` に保存されます。

環境変数 `TASKFLOW_STORAGE` でパスを変更できます:

```bash
export TASKFLOW_STORAGE=/path/to/tasks.json
taskflow list
```

## テスト実行

```bash
pytest tests/ -v
```

## ディレクトリ構成

```
taskflow/
├── models/          # データモデル（Task, TaskStatus）
├── services/        # ビジネスロジック（TaskService）
├── cli/             # CLIインターフェース（app.py）
└── storage/         # データ永続化（JsonStorage）
tests/
└── test_cli.py      # E2Eテスト
```
