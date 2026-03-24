"""argparseベースのCLIエントリーポイント"""
import argparse
import os
import sys
from pathlib import Path

from taskflow.services.task_service import TaskNotFoundError, TaskService
from taskflow.storage.json_storage import JsonStorage


def get_default_storage_path() -> str:
    """デフォルトのストレージパスを返す。

    環境変数 TASKFLOW_STORAGE が設定されている場合はその値を使用する。

    Returns:
        ストレージファイルのパス
    """
    return os.environ.get("TASKFLOW_STORAGE", str(Path.home() / ".taskflow" / "tasks.json"))


def create_parser() -> argparse.ArgumentParser:
    """ArgumentParserを生成して返す。

    Returns:
        設定済みのArgumentParserインスタンス
    """
    parser = argparse.ArgumentParser(
        prog="taskflow",
        description="シンプルなタスク管理CLIツール",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    # add サブコマンド
    add_parser = subparsers.add_parser("add", help="タスクを追加する")
    add_parser.add_argument("title", help="タスクのタイトル")
    add_parser.add_argument("--description", "-d", default="", help="タスクの説明")

    # list サブコマンド
    subparsers.add_parser("list", help="タスク一覧を表示する")

    # done サブコマンド
    done_parser = subparsers.add_parser("done", help="タスクを完了にする")
    done_parser.add_argument("task_id", help="完了するタスクのID")

    # delete サブコマンド
    delete_parser = subparsers.add_parser("delete", help="タスクを削除する")
    delete_parser.add_argument("task_id", help="削除するタスクのID")

    return parser


def main(args=None) -> int:
    """CLIメイン関数。終了コードを返す。

    Args:
        args: コマンドライン引数（Noneの場合はsys.argvを使用）

    Returns:
        終了コード（0: 成功、1: エラー）
    """
    parser = create_parser()
    parsed = parser.parse_args(args)

    if parsed.command is None:
        parser.print_help()
        return 1

    storage = JsonStorage(get_default_storage_path())
    service = TaskService(storage)

    try:
        if parsed.command == "add":
            task = service.add_task(parsed.title, parsed.description)
            print(f"タスクを追加しました: [{task.id}] {task.title}")

        elif parsed.command == "list":
            tasks = service.list_tasks()
            if not tasks:
                print("タスクはありません。")
            else:
                for task in tasks:
                    status_mark = "x" if task.status.value == "completed" else " "
                    print(f"[{status_mark}] {task.id} - {task.title}")
                    if task.description:
                        print(f"    {task.description}")

        elif parsed.command == "done":
            task = service.complete_task(parsed.task_id)
            print(f"タスクを完了しました: [{task.id}] {task.title}")

        elif parsed.command == "delete":
            service.delete_task(parsed.task_id)
            print(f"タスクを削除しました: {parsed.task_id}")

    except TaskNotFoundError as e:
        print(f"エラー: {e}", file=sys.stderr)
        return 1

    return 0
