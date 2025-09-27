import json
from pathlib import Path

from ten_utils.log import Logger

from raccoon.command import Raccoon
from adb.command import Adb
from common.constants import (
    DIR_APKS,
)
from common.helpers import download_file

logger = Logger(__name__)
adb = Adb()


# =================== ВЫБОР УСТРОЙСТВА ===================
def select_device():
    out = adb.get_devices().splitlines()
    devices = [l.split()[0] for l in out[1:] if l.strip() and "device" in l]

    if not devices:
        logger.critical("Нет подключённых устройств!")

    if len(devices) == 1:
        adb.set_device(devices[0])
        logger.info(f"Выбрано устройство: {devices[0]}")

    else:
        logger.info("Найдено несколько устройств:")
        for idx, dev in enumerate(devices, start=1):
            logger.info(f"{idx}: {dev}")

        while True:
            choice = input("Выберите устройство по номеру: ")

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(devices):
                    adb.set_device(devices[idx])
                    logger.info(f"Выбрано устройство: {devices[idx]}")

                    break

            except ValueError:
                pass

            logger.warning("Некорректный ввод, попробуйте снова.")


# =================== ЗАГРУЗКА APK ===================
def download_with_raccoon(package: str) -> Path:
    """Скачивание ABB через Raccoon"""
    logger.info(f"Скачиваю {package} через Raccoon ...")
    app_dir = DIR_APKS / package
    raccoon = Raccoon()

    app_dir.mkdir(parents=True, exist_ok=True)

    apk_files = list(app_dir.rglob("*.apk"))

    if not apk_files:
        success_run = raccoon.download_apk(
            package_name=package,
            out_path=app_dir
        )

        # рекурсивно ищем все apk
        apk_files = list(app_dir.rglob("*.apk"))
        if not apk_files or success_run.returncode != 0:
            logger.critical(f"Raccoon не скачал {package}")

    logger.info(f"Скачано {len(apk_files)} apk для {package}")
    return app_dir


def download_with_url(url: str, package: str) -> Path:
    """Загрузка APK с прямой ссылки"""
    logger.info(f"Скачиваю {package} из URL ...")
    target = DIR_APKS / f"{package}.apk"

    if not target.exists():
        download_file(
            url=url,
            path=target,
        )

    logger.info(f"Скачано: {target}")
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
def check_installed(package: str) -> bool:
    """Проверяет, установлен ли пакет на устройстве"""
    return package in adb.get_packages().stdout

def install_apk(package: str, source: Path):
    if source.is_file():
        logger.info(f"Устанавливаю одиночный APK для {package}")
        adb.install_apk(source)

    elif source.is_dir():
        adb.install_split_apk(package, source)

    else:
        raise ValueError(f"Неправильный source: {source}")

    # Проверка после установки
    if check_installed(package):
        logger.info(f"✅ {package} успешно установлено")

    else:
        logger.error(f"❌ {package} НЕ установлено!")


# =================== ОСНОВНОЙ ЦИКЛ ===================
def run_install():
    logger.info("=== START ===")

    select_device()

    logger.info("Загружаю sources.json ...")
    with open("sources.json", "r", encoding="utf-8") as f:
        sources = json.load(f)

    for entry in sources:
        package = entry["package"]
        try:
            source = resolve_source(entry)
            install_apk(package, source)

        except Exception as e:
            logger.info(f"Ошибка для {package}: {e}")

    logger.info("=== FINISHED ===")
