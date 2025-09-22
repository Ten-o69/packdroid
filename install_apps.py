#!/usr/bin/env python3
import subprocess
import json
import requests
from pathlib import Path
from datetime import datetime

# Пути к инструментам
ADB = "adb"
JAVA = "java"
RACCOON = "/home/rio/Downloads/raccoon-4.24.0.jar"  # укажи свой путь к raccoon.jar
APK_DIR = Path("apks")

DEVICE_SERIAL = None

# =================== УТИЛИТЫ ===================
def log(msg):
    print(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}")

def run_cmd(cmd, check=True, capture_output=False):
    """Запуск adb с выбранным устройством"""
    full_cmd = [ADB]
    if DEVICE_SERIAL:
        full_cmd += ["-s", DEVICE_SERIAL]
    full_cmd += cmd
    log("CMD: " + " ".join(full_cmd))
    return subprocess.run(full_cmd, check=check, capture_output=capture_output, text=True)

def run_local_cmd(cmd, check=True):
    """Запуск локальной команды (Java, curl и т.д.)"""
    log("LOCAL CMD: " + " ".join(cmd))
    return subprocess.run(cmd, check=check, text=True)

# =================== ВЫБОР УСТРОЙСТВА ===================
def select_device():
    global DEVICE_SERIAL
    out = subprocess.check_output([ADB, "devices"], text=True).splitlines()
    devices = [l.split()[0] for l in out[1:] if l.strip() and "device" in l]

    if not devices:
        log("Нет подключённых устройств!")
        raise SystemExit(1)

    if len(devices) == 1:
        DEVICE_SERIAL = devices[0]
        log(f"Выбрано устройство: {DEVICE_SERIAL}")
    else:
        log("Найдено несколько устройств:")
        for idx, dev in enumerate(devices, start=1):
            log(f"{idx}: {dev}")
        while True:
            choice = input("Выберите устройство по номеру: ")
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(devices):
                    DEVICE_SERIAL = devices[idx]
                    log(f"Выбрано устройство: {DEVICE_SERIAL}")
                    break
            except ValueError:
                pass
            log("Некорректный ввод, попробуйте снова.")

# =================== ЗАГРУЗКА APK ===================
def download_with_raccoon(package: str) -> Path:
    """Скачивание ABB через Raccoon"""
    log(f"Скачиваю {package} через Raccoon ...")
    app_dir = APK_DIR / package
    app_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        JAVA, "-jar", RACCOON,
        "--gpa-download", package,
        "--gpa-download-dir", str(app_dir)
    ]
    run_local_cmd(cmd)

    # рекурсивно ищем все apk
    apk_files = list(app_dir.rglob("*.apk"))
    if not apk_files:
        raise FileNotFoundError(f"Raccoon не скачал {package}")

    log(f"Скачано {len(apk_files)} apk для {package}")
    return app_dir

def download_with_url(url: str, package: str) -> Path:
    """Загрузка APK с прямой ссылки"""
    log(f"Скачиваю {package} из URL ...")
    target = APK_DIR / f"{package}.apk"
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(target, "wb") as f:
        for chunk in r.iter_content(1024 * 32):
            f.write(chunk)
    log(f"Скачано: {target}")
    return target

def resolve_source(entry) -> Path:
    method = entry.get("method")
    package = entry["package"]

    if method == "raccoon":
        return download_with_raccoon(package)
    elif method == "url":
        return download_with_url(entry["url"], package)
    elif method == "local":
        return Path(entry["path"])
    else:
        raise ValueError(f"Неизвестный метод: {method}")

# =================== УСТАНОВКА APK ===================
def install_split_apk(package: str, app_dir: Path):
    """Установка split APK (ABB) рекурсивно"""
    apk_files = sorted(app_dir.rglob("*.apk"))
    if not apk_files:
        raise FileNotFoundError(f"Нет APK в {app_dir}")

    log(f"Устанавливаю ABB ({len(apk_files)} файлов) для {package}")
    cmd = ["install-multiple", "-r"] + [str(f) for f in apk_files]
    run_cmd(cmd)

def check_installed(package: str) -> bool:
    """Проверяет, установлен ли пакет на устройстве"""
    res = run_cmd(["shell", "pm", "list", "packages", package], capture_output=True)
    return package in res.stdout

def install_apk(package: str, source: Path):
    if source.is_file():
        log(f"Устанавливаю одиночный APK для {package}")
        run_cmd(["install", "-r", str(source)])
    elif source.is_dir():
        install_split_apk(package, source)
    else:
        raise ValueError(f"Неправильный source: {source}")

    # Проверка после установки
    if check_installed(package):
        log(f"✅ {package} успешно установлено")
    else:
        log(f"❌ {package} НЕ установлено!")

# =================== ОСНОВНОЙ ЦИКЛ ===================
def main():
    log("=== START ===")
    APK_DIR.mkdir(exist_ok=True)

    select_device()

    log("Загружаю sources.json ...")
    with open("sources.json", "r", encoding="utf-8") as f:
        sources = json.load(f)

    for entry in sources:
        package = entry["package"]
        try:
            source = resolve_source(entry)
            install_apk(package, source)
        except Exception as e:
            log(f"Ошибка для {package}: {e}")

    log("=== FINISHED ===")

if __name__ == "__main__":
    main()
