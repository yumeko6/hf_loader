from argparse import ArgumentParser


def create_parser() -> ArgumentParser:
	"""
	Функция создает парсер параметров командной строки.
	:return: объект parser
	"""
	parser = ArgumentParser()
	parser.add_argument(
		'-p', '--path',
		help='Путь к папке с базой кандидатов',
		type=str, required=True
	)
	parser.add_argument(
		'-t', '--token',
		help='Токен авторизации',
		required=True
	)
	return parser
