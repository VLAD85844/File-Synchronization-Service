import os
import requests
import logging
from urllib.parse import quote


class YandexDisk:
    BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources'


    def __init__(self, token, folder_path):
        self.token = token
        self.folder_path = folder_path
        self.headers = {
            'Authorization': f'OAuth {token}',
            'Accept': 'application/json'
        }
        self._ensure_folder_exists()


    def _ensure_folder_exists(self):
        """Создает папку, если она не существует"""
        try:
            response = requests.get(
                f'{self.BASE_URL}?path={quote(self.folder_path)}',
                headers=self.headers
            )
            if response.status_code == 404:
                requests.put(
                    f'{self.BASE_URL}?path={quote(self.folder_path)}',
                    headers=self.headers
                )
        except requests.RequestException as e:
            logging.error(f"Folder check failed: {str(e)}")
            raise


    def upload(self, file_path, overwrite=True):
        """Загружает файл с возможностью перезаписи"""
        try:
            file_name = os.path.basename(file_path)
            encoded_path = quote(f"{self.folder_path}/{file_name}")
            response = requests.get(
                f'{self.BASE_URL}/upload?path={encoded_path}&overwrite={str(overwrite).lower()}',
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            upload_data = response.json()
            if not upload_data.get('href'):
                raise ValueError("No upload URL received")
            with open(file_path, 'rb') as f:
                upload_response = requests.put(
                    upload_data['href'],
                    files={'file': f},
                    timeout=30
                )
                upload_response.raise_for_status()

            logging.info(f"File {file_name} uploaded successfully")
            return True
        except Exception as e:
            logging.error(f"Upload failed: {str(e)}")
            return False

    def get_info(self):
        """Получает информацию о файлах в папке"""
        try:
            response = requests.get(
                f'{self.BASE_URL}?path={quote(self.folder_path)}',
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json().get('_embedded', {}).get('items', [])
        except Exception as e:
            logging.error(f"Get info failed: {str(e)}")
            return []


    def delete(self, file_name, permanently=False):
        """Удаляет файл с Яндекс Диска"""
        try:
            encoded_path = quote(f"{self.folder_path}/{file_name}")
            url = f"{self.BASE_URL}?path={encoded_path}&permanently={str(permanently).lower()}"
            response = requests.delete(
                url,
                headers=self.headers,
                timeout=10
            )
            if response.status_code in [204, 202]:
                logging.info(f"File {file_name} deleted successfully")
                return True
            else:
                logging.error(f"Delete failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logging.error(f"Delete operation error: {str(e)}")
            return False