# Yiwen Wang

import datetime
import re
import sys

from prettytable import PrettyTable

tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT",  "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]

month_to_num = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6, "JUL": 7, 
				"AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}

def get_info(file_name):
	# error
	if(file_name.split(".")[1] != "ged"):
		print("Must supply GEDCOM file.")
	else:
		with open(file_name, 'r') as reader:
			gedcom = reader.read()
			blocks = gedcom.split('\n0 ')
			individuals = []
			families = []
			for block in blocks:
				block = block.replace('\r', '')
				if re.search('@I\d+@ INDI', block) != None:
					block = '0 ' + block
					individuals.append(block)
				elif re.search('@F\d+@ FAM', block) != None:
					block = '0 ' + block
					families.append(block)

		individuals_table = []
		for individual in individuals:
			info = individual.split('\n')
			ind_id = None
			name = None
			sex = None
			birthday = None
			age = None
			alive = None
			death = None
			child = None
			spouse = None
			for index in range(0, len(info)):
				values = info[index].split(' ')
				if tags[0] in values:
					ind_id = values[1]
				elif tags[1] in values:
					name = ''
					for num in range(2, len(values)):
						name += values[num] + " "
					name = name[0:len(name)-1]
				elif tags[2] in values:
					sex = values[2]
				elif tags[3] in values:
					birthday = info[index+1][7:]
				elif tags[4] in values:
					death = info[index+1][7:]
				elif tags[5] in values:
					child = values[2]
				elif tags[6] in values:
					spouse = values[2]
		
			if birthday != None:
				birth_dmy = birthday.split(" ")
				birth_day = int(birth_dmy[0])
				birth_month = month_to_num[birth_dmy[1]]
				birth_year = int(birth_dmy[2])
				try:
					datetime.datetime(birth_year, birth_month, birth_day)
				except ValueError: 
					print("Value Error: US42 illegitimate Date")
					return 0
				b = datetime.datetime(birth_year, birth_month, birth_day)
				birthday = b
			if death != None:
				death_dmy = death.split(" ")
				death_day = int(death_dmy[0])
				death_month = month_to_num[death_dmy[1]]
				death_year = int(death_dmy[2])
				d = datetime.datetime(death_year, death_month, death_day)
				if birthday != None:
					age = d - birthday
				alive = False
				death = d
			else:
				if birthday != None:
					age = datetime.datetime.now().year - birthday.year
					if datetime.datetime.now().month < birthday.month or (datetime.datetime.now().month == birthday.month and datetime.datetime.now().day < birthday.day):
						age -= 1
				alive = True
			obj = {"id": ind_id, "name": name, "sex": sex, "birthday": birthday, "age": age, "alive": alive, "death": death, "child": child, "spouse": spouse}
			individuals_table.append(obj)

		# get info
		family_table = []
		for family in families:
			info = family.split('\n')
			fam_id = None
			married = None
			divorced = None
			husband_id = None
			husband_name = None
			wife_id = None
			wife_name = None
			children = []
			for index in range(0, len(info)):
				values = info[index].split(' ')
				if tags[7] in values:
					fam_id = values[1]
				if tags[8] in values:
					married = info[index+1][7:]
				if tags[12] in values:
					divorced = info[index+1][7:]
				if tags[9] in values:
					husband_id = values[2]
					for ind in individuals_table:
						if ind["id"] == husband_id:
							husband_name = ind["name"]
							break
				if tags[10] in values:
					wife_id = values[2]
					for ind in individuals_table:
						if ind["id"] == wife_id:
							wife_name = ind["name"]
							break
				if tags[11] in values:
					children.append(values[2])
			obj = {"id": fam_id, "married": married, "divorced": divorced, "husband_id": husband_id, "husband_name": husband_name, "wife_id": wife_id, "wife_name": wife_name, "children": children}
			family_table.append(obj)

		return {"individuals": individuals_table, "families": family_table}


def print_tables(file_name):
	info = get_info(file_name)
	print("Individuals")
	individuals_print = PrettyTable()
	individuals_print.field_names = list(info['individuals'][0].keys())
	for ind in info['individuals']:
		individuals_print.add_row(list(ind.values()))
	print(individuals_print)

	print("Families")
	families_print = PrettyTable()
	families_print.field_names = list(info['families'][0].keys())
	for fam in info['families']:
		families_print.add_row(list(fam.values()))
	print(families_print)


print_tables("Homework.ged")