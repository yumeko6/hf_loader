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

##### Создайте файл .env, 
##### Запишите в него переменную BASE_STAGE_URL и присвойте ей url песочницы
```python
touch .env
```

##### Запустите скрипт командой
```python
python main.py -p <path_to_base> -t <api_token>
```
##### где '-p <path_to_base>' это путь к базе с кандидатами, например -p files/bases
##### и '-t <api_token>' это api токен авторизации
