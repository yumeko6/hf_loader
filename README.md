## Тестовое задание Huntflow

### Подготовка и запуск проекта

##### Клонируйте репозиторий
`https://github.com/yumeko6/hf_loader.git`

##### Создайте и активируйте виртуальное окружение
```python
python -m venv venv
source venv/Scripts/activate
```

##### Установите зависимости
```python
pip install -r requirements.txt
```

##### Создайте файл .env
##### Добавьте в .env строку https://dev-100-api.huntflow.dev/v2/
```python
touch .env
```

##### Запустите скрипт командой
```python
python main.py -p <path_to_base> -t <api_token>
```
##### где '-p <path_to_base>' это путь к базе с кандидатами, например -p files/bases
##### и '-t <api_token>' это api токен авторизации
