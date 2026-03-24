"""TaskFlow CLIのE2Eテスト"""
import json
import os
import subprocess
import sys

import pytest

WORKTREE_PATH = "/home/neko/prog/agent-team-demo/.worktrees/feature-task-cli"


def run_cli(*args, env=None):
    """CLIをsubprocessで実行する。

    Args:
        *args: CLIに渡す引数
        env: 環境変数の辞書（Noneの場合は現在の環境変数を使用）

    Returns:
        subprocess.CompletedProcessオブジェクト
    """
    result = subprocess.run(
        [sys.executable, "-m", "taskflow"] + list(args),
        capture_output=True,
        text=True,
        cwd=WORKTREE_PATH,
        env=env,
    )
    return result


def make_env(tmp_path):
    """テスト用の環境変数を作成する。

    Args:
        tmp_path: 一時ディレクトリのパス

    Returns:
        TASKFLOW_STORAGEを設定した環境変数の辞書
    """
    env = os.environ.copy()
    env["TASKFLOW_STORAGE"] = str(tmp_path / "tasks.json")
    return env


def test_add_task(tmp_path):
    """タスク追加テスト"""
    env = make_env(tmp_path)
    result = run_cli("add", "テストタスク", env=env)
    assert result.returncode == 0
    assert "テストタスク" in result.stdout


def test_add_task_with_description(tmp_path):
    """説明付きタスク追加テスト"""
    env = make_env(tmp_path)
    result = run_cli("add", "説明付きタスク", "--description", "これは説明です", env=env)
    assert result.returncode == 0
    assert "説明付きタスク" in result.stdout


def test_list_tasks_empty(tmp_path):
    """空のタスク一覧テスト"""
    env = make_env(tmp_path)
    result = run_cli("list", env=env)
    assert result.returncode == 0
    assert "タスクはありません" in result.stdout


def test_list_tasks(tmp_path):
    """タスク一覧表示テスト"""
    env = make_env(tmp_path)
    run_cli("add", "タスク1", env=env)
    run_cli("add", "タスク2", env=env)

    result = run_cli("list", env=env)
    assert result.returncode == 0
    assert "タスク1" in result.stdout
    assert "タスク2" in result.stdout


def test_complete_task(tmp_path):
    """タスク完了テスト"""
    env = make_env(tmp_path)
    add_result = run_cli("add", "完了するタスク", env=env)
    assert add_result.returncode == 0

    # タスクIDを取得するためにlistを実行
    list_result = run_cli("list", env=env)
    # ストレージから直接IDを取得
    storage_path = tmp_path / "tasks.json"
    with open(storage_path) as f:
        tasks = json.load(f)
    task_id = tasks[0]["id"]

    done_result = run_cli("done", task_id, env=env)
    assert done_result.returncode == 0
    assert "完了しました" in done_result.stdout

    # リストでxマークを確認
    list_after = run_cli("list", env=env)
    assert "[x]" in list_after.stdout


def test_complete_task_not_found(tmp_path):
    """存在しないタスクの完了テスト"""
    env = make_env(tmp_path)
    result = run_cli("done", "nonexistent-id", env=env)
    assert result.returncode == 1
    assert "エラー" in result.stderr


def test_delete_task(tmp_path):
    """タスク削除テスト"""
    env = make_env(tmp_path)
    run_cli("add", "削除するタスク", env=env)

    storage_path = tmp_path / "tasks.json"
    with open(storage_path) as f:
        tasks = json.load(f)
    task_id = tasks[0]["id"]

    delete_result = run_cli("delete", task_id, env=env)
    assert delete_result.returncode == 0
    assert "削除しました" in delete_result.stdout

    # タスクが消えたことを確認
    list_result = run_cli("list", env=env)
    assert "タスクはありません" in list_result.stdout


def test_delete_task_not_found(tmp_path):
    """存在しないタスクの削除テスト"""
    env = make_env(tmp_path)
    result = run_cli("delete", "nonexistent-id", env=env)
    assert result.returncode == 1
    assert "エラー" in result.stderr


def test_no_command_shows_help(tmp_path):
    """コマンドなし実行でヘルプ表示テスト"""
    env = make_env(tmp_path)
    result = run_cli(env=env)
    assert result.returncode == 1
