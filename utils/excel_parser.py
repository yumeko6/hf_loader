import glob
import json
import mimetypes
import os

import pandas as pd

from .models import Applicant


def walk(fullname) -> tuple[str, str, str]:
	"""
	Функция рекурсивно проходит по директории с файлами, если есть совпадение -
	возвращает имя файла, путь до файла и его mime_type.
	:param fullname: ФИО кандидата из xlsx файла
	:return: имя файла, путь до файла, mime_type
	"""
	directory = 'files/applicants'
	for root, dirs, files in os.walk(directory):
		for file in files:
			mimetypes.init()
			ext_data = os.path.splitext(file)
			if len(ext_data) > 1:
				mime_type = mimetypes.types_map.get(
					ext_data[len(ext_data) - 1]) or 'application/zip'
			else:
				mime_type = 'application/zip'
			if file.startswith(fullname):
				filepath = os.path.join(root, file)
				return file, filepath, mime_type


def parse_files(path) -> list:
	"""
	Функция парсит файл xlsx сначала в словарь json_dict (с первоначальной
	проверкой и удалением дубликатов).
	Затем на каждую запись в словаре находится соответствующий файл резюме,
	если файл есть - создает объект	модели Applicant включая имя файла,
	путь до файла и mime_type; если резюме	нет - создает со значением None.
	:param path: путь к базе xlsx
	:param filepath: путь до файла
	:return: список объектов модели Applicant
	"""
	filepath = glob.glob(fr'{path}\*.xlsx')
	df = pd.read_excel(filepath[0])
	unique_df = df.drop_duplicates()
	columns = unique_df.columns.values
	json_str = unique_df.to_json(orient='records')
	json_dict = json.loads(json_str)
	applicants: list = []
	for applicant in json_dict:
		fullname = applicant.get(columns[1]).rstrip()
		fullname_len = len(fullname.split())
		resume = walk(fullname)
		applicants.append(
			Applicant(
				fullname=fullname,
				first_name=fullname.split()[1],
				last_name=fullname.split()[0],
				middle_name=fullname.split()[2] if fullname_len > 2 else None,
				position=applicant.get(columns[0]),
				money=str(applicant.get(columns[2])),
				comment=applicant.get(columns[3]),
				status=applicant.get(columns[4]),
				filename=resume[0] if resume else None,
				filepath=resume[1] if resume else None,
				mime_type=resume[2] if resume else None,
				externals=None
			)
		)
	return applicants
