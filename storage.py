"""Загрузка и сохранение данных проекта в JSON-файлах."""
import json
import os
from typing import Any


DATA_DIR = "data"


def _ensure_data_dir() -> None:
    """Создать каталог data, если его нет."""
    os.makedirs(DATA_DIR, exist_ok=True)


def load_data(filename: str, default: Any) -> Any:
    """Загрузить данные из JSON-файла.

    Если файл отсутствует или повреждён — вернуть значение по умолчанию.
    """
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Предупреждение: не удалось прочитать {filename}: {error}")
        return default


def save_data(filename: str, data: Any) -> None:
    """Сохранить данные в JSON-файл через контекстный менеджер."""
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError as error:
        print(f"Ошибка сохранения {filename}: {error}")
