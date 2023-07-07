import os

from dotenv import load_dotenv

load_dotenv()


def get_variables() -> tuple:
	"""
	Функция хранит в себе пеобходимые переменные для работы основных функций.
	:return: кортеж переменных
	"""
	account_id: int | None = None
	vacancy_id: int | None = None
	base_dev_url: str = os.getenv('BASE_DEV_URL')
	accounts_url: str = os.path.join(base_dev_url, 'accounts')
	headers: dict = {'content-type': 'application/json'}

	return account_id, vacancy_id, accounts_url, headers
