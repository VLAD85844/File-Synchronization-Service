# File Synchronization Service


Сервис для синхронизации локальной папки с Яндекс Диском


## 📌 Функционал
- Автоматическая синхронизация указанной папки с Яндекс Диском
- Отслеживание изменений (добавление/изменение/удаление файлов)
- Логирование всех операций
- Настройка через конфигурационный файл


## ⚙️ Требования
- Python 3.8+
- Библиотека `requests` (`pip install requests`)


## 🚀 Установка
1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/VLAD85844/File-Synchronization-Service.git

2. Создайте файл .myenv и установите зависимости:

   ```bash
   python -m venv myenv # Создаёт окружение в папке myenv   
   pip install requests
   myenv\Scripts\activate # Активирует окружение
   

## 🖥️ Настройка config.ini

[DEFAULT]
local_folder = /путь/к/локальной/папке
cloud_folder = /sync_folder  # Папка на Яндекс.Диске
token = ваш_oauth_токен
sync_interval = 300  # Интервал синхронизации (секунды)
log_file = sync.log


## 📂 Запуск сервиса

    ```bash
    python file_sync.py