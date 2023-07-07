from datetime import datetime

from pydantic import BaseModel, FilePath


class Vacancy(BaseModel):
	account_division: int | None
	account_region: str | None
	position: str
	company: str | None
	money: str | None
	priority: int = 0
	hidden: bool = False
	state: str = 'OPEN'
	id: int
	created: datetime
	additional_fields_list: list
	multiple: bool = False
	parent: int | None
	account_vacancy_status_group: int | None


class Data(BaseModel):
	body: str


class Externals(BaseModel):
	auth_type: str = 'NATIVE'
	data: Data
	files: list[int]


class Applicant(BaseModel):
	fullname: str
	first_name: str
	last_name: str
	middle_name: str | None
	money: str
	position: str
	comment: str | None
	status: str
	filename: str | None
	filepath: FilePath | None
	mime_type: str | None
	externals: list[Externals] | None


a = [
	{
		'data': {
			'body': 'asd'
		},
		'files': 1
	}
]


