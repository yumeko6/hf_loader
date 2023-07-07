import logging
import os
import sys

import requests
from requests.exceptions import RequestException

from utils.cli_handler import create_parser
from utils.excel_parser import parse_files
from utils.models import Externals, Data, Applicant
from utils.variables import get_variables


def get_account_id() -> int:
	"""
	Функция получает текущий id компании через GET-запрос для дальнейшего
	использования в url.
	:return: id: int
	"""
	try:
		result = requests.get(ACCOUNTS_URL, headers=headers)
		account_id = result.json()['items'][0]['id']
		logging.info('Получение id компании успешно выполнено')
		return account_id
	except RequestException as request_error:
		logging.error(
			f'При запросе на получение id компании '
			f'произошла ошибка: {request_error}'
		)
		raise request_error
	except IndexError as index_error:
		logging.error(
			f'При попытке получить id компании произошла ошибка: {index_error}'
		)
		raise index_error


def get_vacancies(acc_id: int) -> dict:
	"""
	Функция получает id всех вакансий через GET-запрос.
	:type acc_id: id компании
	:return: vacancies: dict
	"""
	vacancies_url = ACCOUNTS_URL + f'/{acc_id}/vacancies'
	try:
		result = requests.get(vacancies_url, headers=headers)
		logging.info(
			f'Получение всех вакансий компании id={acc_id} успешно выполнено.'
		)
		vacancies: dict = {}
		for vacancy in result.json()['items']:
			vacancies.update(
				{vacancy['position']: vacancy['id']}
			)
		return vacancies
	except RequestException as request_error:
		logging.error(
			f'При получении всех вакансий компании id={acc_id} '
			f'произошла ошибка: {request_error}'
		)
		raise request_error
	except IndexError as index_error:
		logging.error(
			f'При обработке списка вакансий компании id={acc_id} '
			f'произошла ошибка: {index_error}'
		)
		raise index_error


def get_vacancy_statuses(acc_id: int) -> dict:
	"""
	Функция получает все статусы вакансии через GET-запрос
	:param acc_id: id компании
	:return: словарь со всеми вакансиями
	"""
	vacancy_statuses_url = ACCOUNTS_URL + f'/{acc_id}/vacancies/statuses'
	try:
		vacancy_statuses = requests.get(
			vacancy_statuses_url, headers=headers)
		logging.info(
			f'Запрос на получение статусов вакансий компании id={acc_id} '
			f'успешно выполнен.'
		)
		statuses: dict = {}
		for status in vacancy_statuses.json()['items']:
			statuses.update(
				{status['name']: status['id']}
			)
		return statuses
	except RequestException as request_error:
		logging.error(
			f'При получении статусов вакансий компании id={acc_id} '
			f'произошла ошибка: {request_error}'
		)
		raise request_error
	except IndexError as index_error:
		logging.error(
			f'При обработке статусов вакансий компании id={acc_id} '
			f'произошла ошибка: {index_error}'
		)
		raise index_error


def load_applicant(acc_id: int, applicant: Applicant) -> dict:
	"""
	Функция заносит кандидата в базу через POST-запрос.
	:param acc_id: id компании
	:param applicant: объект модели Applicant
	:return: json-объект загруженного кандидата
	"""
	url = ACCOUNTS_URL + f'/{acc_id}/applicants'
	data_to_load = applicant.model_dump(
		exclude={'fullname', 'comment', 'status', 'filepath', 'mime_type'}
	)
	try:
		loaded_applicant = requests.post(
			url, headers=headers, json=data_to_load)
		logging.info(
			f'Кандидат {applicant.fullname} успешно загружен в базу Huntflow.'
		)
		return loaded_applicant.json()
	except RequestException as request_error:
		logging.error(
			f'При загрузке кандидата {applicant.fullname} '
			f'произошла ошибка: {request_error}'
		)
		raise request_error


def upload_file(
		acc_id: int, filename: str, filepath: str, mime_type: str) -> dict:
	"""
	Функция загружает файл резюме кандидата в базу через POST-запрос.
	:param acc_id: id компании
	:param filename: имя фала
	:param filepath: путь до файла
	:param mime_type: mime_type (например 'application/msword')
	:return: json-объект загруженного файла
	"""
	url = ACCOUNTS_URL + f'/{acc_id}/upload'
	headers['content-type'] = None
	headers['x-file-parse'] = 'true'
	file = {'file': (filename, open(filepath, 'rb'), mime_type)}
	try:
		uploaded_file = requests.post(
			url, headers=headers, files=file)
		logging.info(f'Файл {filename} успешно загружен в базу Huntflow.')
		return uploaded_file.json()
	except RequestException as error:
		logging.error(
			f'При загрузке файла {filename} произошла ошибка: {error}'
		)
		raise error


def add_applicant_to_vacancy(
		app_id: int, acc_id: int, vacancy: int,
		status: int, comment: str) -> None:
	"""
	Функция добавляет кандидата к существующей вакансии через POST-запрос.
	:param comment: комментарий из файла
	:param app_id: id загруженного кандидата
	:param acc_id: id компании
	:param vacancy: id вакансии
	:param status: id статуса (этапа)
	:return:
	"""
	add_url = ACCOUNTS_URL + f'/{acc_id}/applicants/{app_id}/vacancy'
	data_to_load = {'vacancy': vacancy, 'status': status, 'comment': comment}
	try:
		requests.post(add_url, headers=headers, json=data_to_load)
		logging.info(
			f'Кандидат id={app_id} успешно добавлен к вакансии id={vacancy}'
		)
	except RequestException as error:
		logging.error(
			f'При добавлении кандидата к вакансии возникла ошибка: {error}'
		)
		raise error


def main(path: str) -> None:
	"""
	Основная функция, которая выполняет последовательно загрузку данных в базу
	Хантфлоу, а также получение данных из базы.
	:param path: путь до файла с базой xlsx для парсинга кандидатов
	:return: None
	"""
	try:
		applicants = parse_files(path)
		logging.info(f'Парсинг файла из директории {path} успешно завершен')
	except Exception as error:
		logging.error(
			f'При парсинге файла из директории {path} '
			f'произошла ошибка: {error}'
		)
		raise error
	acc_id = get_account_id()
	vacancies = get_vacancies(acc_id)
	statuses = get_vacancy_statuses(acc_id)

	for applicant in applicants:
		if applicant.filepath:
			#  загружаем файл резюме
			uploaded_file = upload_file(
				acc_id,
				applicant.filename,
				applicant.filepath,
				applicant.mime_type
			)

			file_id = uploaded_file['id']
			file_text = uploaded_file['text']

			external = Externals(
				data=Data(body=file_text),
				files=[file_id]
			)
			applicant.externals = [external]

			#  загружаем кандидата
			loaded_applicant = load_applicant(acc_id, applicant)
			applicant_id = loaded_applicant['id']

			#  добавляем кандидата к вакансии
			add_applicant_to_vacancy(
				applicant_id,
				acc_id,
				vacancies[applicant.position],
				statuses[applicant.status],
				applicant.comment
			)


if __name__ == '__main__':
	root_path = os.getcwd()
	logging.basicConfig(
		filename=f'{root_path}/logs/main.log',
		level=logging.DEBUG,
		format='%(levelname)s %(asctime)s %(message)s',
		datefmt='%Y/%m/%d %I:%M:%S %p'
	)
	parser = create_parser()
	namespace = parser.parse_args(sys.argv[1:])
	account_id, vacancy_id, ACCOUNTS_URL, headers = get_variables()
	headers['Authorization'] = f'Bearer {namespace.token}'
	main(namespace.path)
