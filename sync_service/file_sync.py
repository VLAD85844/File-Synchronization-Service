import os
import time
import logging
import configparser
from cloud_storage import YandexDisk


def setup_logging(log_file):
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )



def read_config(config_file):
    """Чтение конфигурационного файла"""
    config = configparser.ConfigParser()
    config.read(config_file)

    try:
        return {
            'local_folder': config['DEFAULT']['local_folder'],
            'cloud_folder': config['DEFAULT']['cloud_folder'],
            'token': config['DEFAULT']['token'],
            'sync_interval': int(config['DEFAULT']['sync_interval']),
            'log_file': config['DEFAULT']['log_file']
        }
    except (KeyError, ValueError) as e:
        logging.error(f'Configuration error: {e}')
        raise


def get_local_files(local_folder):
    """Получение списка локальных файлов"""
    try:
        return {
            f: os.path.getmtime(os.path.join(local_folder, f))
            for f in os.listdir(local_folder)
            if os.path.isfile(os.path.join(local_folder, f))
        }
    except OSError as e:
        logging.error(f'Error reading local files: {e}')
        return {}


def sync_files(local_folder, cloud_storage):
    """Синхронизация файлов между локальной папкой и облаком"""
    local_files = get_local_files(local_folder)
    cloud_items = cloud_storage.get_info()
    cloud_files = {item['name']: item for item in cloud_items}

    for file_name, mtime in local_files.items():
        file_path = os.path.join(local_folder, file_name)
        cloud_storage.upload(file_path)

    for cloud_file in cloud_items:
        if cloud_file['name'] not in local_files:
            cloud_storage.delete(cloud_file['name'])


def main():
    try:
        config = read_config('config.ini')
        setup_logging(config['log_file'])
        logging.info(f'Starting synchronization service. Local folder: {config["local_folder"]}')
        if not os.path.exists(config['local_folder']):
            raise FileNotFoundError(f'Local folder does not exist: {config["local_folder"]}')

        cloud_storage = YandexDisk(config['token'], config['cloud_folder'])

        while True:
            sync_files(config['local_folder'], cloud_storage)
            time.sleep(config['sync_interval'])

    except Exception as e:
        logging.error(f'Fatal error: {e}')
        exit(1)


if __name__ == '__main__':
    main()