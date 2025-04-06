#!/usr/bin/env python3

# uv venv --python 3.13
# chmod +x <thisfile> then use: ./run.py init (or format, check, etc.)
import os
import subprocess
import sys

commands = [
    "uv venv --python 3.13",
    "uv init",
    "uv venv",
    "uv add ruff dotenv pyright mypy",
    "uv run ruff format",
    "uv run ruff check",
]


def ensure_git_user_config():
    """Ensures the [user] section exists in .git/config."""
    git_config_path = ".git/config"
    if not os.path.exists(git_config_path):
        print(f"ERROR: {git_config_path} does not exist.")
        return

    with open(git_config_path, "r+") as file:
        content = file.read()
        if "[user]" not in content:
            file.write(
                "\n[user]\n\tname = dylandevus\n\temail = dylanlogic@outlook.com\n"
            )
            print("--- Added [user] section to .git/config")
        else:
            print("--- [user] section already exists in .git/config")


def create_pre_commit_config():
    """Creates or overwrites the .pre-commit-config.yaml file."""
    pre_commit_config_content = """repos:
- repo: https://github.com/astral-sh/ruff-pre-commit
  # Ruff version.
  rev: v0.11.2
  hooks:
    # Run the linter.
    - id: ruff
    # Run the formatter.
    - id: ruff-format

- repo: https://github.com/RobertCraigie/pyright-python
  rev: v1.1.398
  hooks:
  - id: pyright
"""
    try:
        with open(".pre-commit-config.yaml", "w") as file:
            file.write(pre_commit_config_content)
        print("--- Created .pre-commit-config.yaml")
    except Exception as e:
        print(f"ERROR: Failed to create .pre-commit-config.yaml: {e}", file=sys.stderr)


def run_commands():
    for cmd in commands:
        print(f"--- Running: {cmd}")
        try:
            result = subprocess.run(
                cmd,
                shell=True,  # Be cautious with shell=True and untrusted input!
                check=True,
                capture_output=True,
                text=True,
            )
            print("STDOUT:")
            print(result.stdout)
            if result.stderr:
                print("STDERR:")
                print(result.stderr, file=sys.stderr)
        except subprocess.CalledProcessError as e:
            print(
                f"ERROR: Command failed with exit code {e.returncode}", file=sys.stderr
            )
            print("STDOUT:")
            print(e.stdout)
            print("STDERR:")
            print(e.stderr, file=sys.stderr)
        except FileNotFoundError:
            print(f"!!! Command not found: {cmd.split()[0]} !!!", file=sys.stderr)
        print("-" * 20 + "\n")


def list_files():
    subprocess.run(["ls", "-l"])


def print_version():
    subprocess.run(["python", "--version"])


def echo_message():
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        subprocess.run(["echo", message])
    else:
        print("Usage: uv run say-something <message>")


def run_ruff_format():
    """Runs the 'uv run ruff format' command."""
    try:
        subprocess.run(["uv", "run", "ruff", "format"], check=True)
        print("--- Successfully ran 'uv run ruff format'")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to run 'uv run ruff format': {e}", file=sys.stderr)


def run_cli(command: str):
    """
    Runs a shell command and prints the output.

    Args:
        command (str): The shell command to execute.
    """
    try:
        print(f"--- Running command: {command}")
        subprocess.run(command.split(), check=True)
        print(f"--- Successfully ran: {command}")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to run '{command}': {e}", file=sys.stderr)
    except FileNotFoundError:
        print(f"ERROR: Command not found: {command.split()[0]}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if "init" in sys.argv:
            ensure_git_user_config()
            run_commands()
            create_pre_commit_config()
        elif "format" in sys.argv:
            run_cli("uv run ruff format")
        elif "check" in sys.argv:
            run_cli("uv run ruff check")
        elif "pyright" in sys.argv:
            run_cli("uv run pyright")
        elif "mypy" in sys.argv:
            run_cli("uv run mypy src/**/*.py")
