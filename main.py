import os
import ast
import tkinter as tk
from tkinter import filedialog
import pathspec
import subprocess
import argparse
from tqdm import tqdm

known_std_libs = set([
    "os", "sys", "math", "abc", "argparse", "array", "asyncio", "base64", "binascii",
    "bisect", "builtins", "bz2", "calendar", "collections", "concurrent", "configparser",
    "contextlib", "copy", "csv", "ctypes", "datetime", "dbm", "decimal", "difflib",
    "dis", "distutils", "email", "encodings", "enum", "fcntl", "fileinput", "fnmatch",
    "formatter", "fractions", "ftplib", "functools", "gc", "getopt", "getpass", "gettext",
    "glob", "gzip", "hashlib", "heapq", "hmac", "html", "http", "imaplib", "imghdr",
    "importlib", "inspect", "io", "ipaddress", "itertools", "json", "keyword", "lib2to3",
    "linecache", "locale", "logging", "lzma", "mailbox", "mailcap", "marshal", "mimetypes",
    "modulefinder", "msvcrt", "multiprocessing", "netrc", "nis", "nntplib", "numbers",
    "operator", "optparse", "pathlib", "pdb", "pickle", "pip", "pkgutil", "platform",
    "plistlib", "poplib", "posix", "pprint", "profile", "pstats", "pty", "pwd", "queue",
    "quopri", "random", "re", "readline", "reprlib", "resource", "rlcompleter", "runpy",
    "sched", "secrets", "select", "selectors", "shelve", "shlex", "shutil", "signal",
    "site", "smtpd", "smtplib", "sndhdr", "socket", "socketserver", "sqlite3", "ssl",
    "stat", "statistics", "string", "struct", "subprocess", "sunau", "symbol", "symtable",
    "sysconfig", "tabnanny", "tarfile", "telnetlib", "tempfile", "termios", "test",
    "textwrap", "threading", "time", "timeit", "tkinter", "token", "tokenize", "trace",
    "traceback", "tracemalloc", "tty", "turtle", "types", "typing", "unicodedata",
    "unittest", "urllib", "uu", "uuid", "venv", "warnings", "wave", "weakref", "webbrowser",
    "winreg", "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc", "zipapp", "zipfile", "zlib"
])


def extract_imports_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            node = ast.parse(f.read())
    except UnicodeDecodeError:
        print(f"Пропуск файла из-за ошибки декодирования: {file_path}")
        return set()

    imports = set()
    for elem in node.body:
        if isinstance(elem, (ast.Import, ast.ImportFrom)):
            for n in elem.names:
                imports.add(n.name.split('.')[0])
    return imports


def get_latest_package_version(package_name):
    try:
        output = subprocess.check_output([f"pip show {package_name}"], shell=True).decode('utf-8')
        for line in output.splitlines():
            if line.startswith('Version:'):
                return line.split(': ')[1]
    except Exception as e:
        print(f"Ошибка при получении версии для {package_name}: {e}")
    return None


def generate_requirements(project_folder, add_last_versions=False, force=False, only_packets_w_versions=False):
    all_imports = set()

    gitignore_path = os.path.join(project_folder, '.gitignore')
    if not os.path.exists(gitignore_path):
        gitignore_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.gitignore')
        print("Используется встроенный .gitignore")

    with open(gitignore_path, 'r') as f:
        gitignore = f.read()
    spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, gitignore.splitlines())

    for root, _, files in os.walk(project_folder):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, project_folder)
                if not spec.match_file(relative_path):
                    all_imports.update(extract_imports_from_file(full_path))

    external_imports_versions = {}
    for imp in tqdm(all_imports - known_std_libs, desc="Получение версий",
                    disable=not (add_last_versions or only_packets_w_versions)):
        if add_last_versions or only_packets_w_versions:
            version = get_latest_package_version(imp)
            if version:
                external_imports_versions[imp] = version
            elif not only_packets_w_versions:
                external_imports_versions[imp] = ""
        else:
            external_imports_versions[imp] = ""

    if force:
        requirements_path = os.path.join(project_folder, "requirements.txt")
    else:
        requirements_path = os.path.join(project_folder, "requirements_generated.txt")

    with open(requirements_path, "w", encoding="utf-8") as f:
        for imp, version in external_imports_versions.items():
            if version:
                f.write(f"{imp}=={version}\n")
            else:
                f.write(f"{imp}\n")


def select_folder_and_generate_requirements(add_last_versions, force, only_packets_w_versions):
    root = tk.Tk()
    root.withdraw()

    print("Выберите папку с проектом")
    folder = filedialog.askdirectory(title="Выберите папку с проектом")
    if folder:
        generate_requirements(folder, add_last_versions, force, only_packets_w_versions)
        print("Файл requirements.txt успешно создан!")
    else:
        print("Выбор папки отменен.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Генерация файла requirements.txt на основе импортов в проекте.")
    parser.add_argument('--add_last_versions', action='store_true', help='Добавить последние версии пакетов')
    parser.add_argument('--force', action='store_true', help='Перезаписать или создать requirements.txt')
    parser.add_argument('--only_packets_w_versions', action='store_true',
                        help='Добавить только пакеты, для которых найдены версии')
    args = parser.parse_args()

    if args.only_packets_w_versions:
        args.add_last_versions = True

    select_folder_and_generate_requirements(args.add_last_versions, args.force, args.only_packets_w_versions)
