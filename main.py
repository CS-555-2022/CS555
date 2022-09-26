from gedcom.element.element import Element
from gedcom.element.individual import IndividualElement
from gedcom.element.family import FamilyElement
from gedcom.parser import Parser
from prettytable import PrettyTable
from datetime import datetime, date
import gedcom.tags
import sys


def calculate_age(dtob):
    today = date.today()
    return today.year - dtob.year - ((today.month, today.day) < (dtob.month, dtob.day))


def clean_id(id):
    return id.strip("@")


def pretty_individuals(individuals):
    t = PrettyTable()
    t.field_names = [
        "ID",
        "Name",
        "Gender",
        "Birthday",
        "Age",
        "Alive",
        "Death",
        "Child",
        "Spouse",
    ]
    for i in individuals:
        f = []
        f.append(clean_id(i.get_pointer()))
        (first, last) = i.get_name()
        f.append(first + " " + last)
        f.append(i.get_gender())
        birthday = datetime.strptime(i.get_birth_data()[0], "%d %b %Y")
        f.append(birthday.strftime("%Y-%m-%d"))
        f.append(calculate_age(birthday))
        f.append(not i.is_deceased())
        if i.get_death_data()[0] != "":
            deathday = datetime.strptime(i.get_death_data()[0], "%d %b %Y")
            f.append(deathday.strftime("%Y-%m-%d"))
        else:
            f.append("N/A")
        childs = []
        spouses = []
        for n in i.get_child_elements():
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_FAMILY_CHILD:
                childs.append("'" + clean_id(n.get_value()) + "'")
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE:
                spouses.append("'" + clean_id(n.get_value()) + "'")
        if childs != []:
            f.append("{" + ",".join(childs) + "}")
        else:
            f.append("N/A")
        if spouses != []:
            f.append("{" + ",".join(spouses) + "}")
        else:
            f.append("N/A")
        t.add_row(f)
    print("Individuals")
    print(t.get_string())


def pretty_families(families, individuals):
    t = PrettyTable()
    t.field_names = [
        "ID",
        "Married",
        "Divorced",
        "Husband ID",
        "Husband Name",
        "Wife ID",
        "Wife Name",
        "Children",
    ]
    for i in families:
        f = []
        f.append(clean_id(i.get_pointer()))
        married_date = "N/A"
        divorced_date = "N/A"
        husband_id = ""
        husband_name = ""
        wife_id = ""
        wife_name = ""
        children = []
        for n in i.get_child_elements():
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_MARRIAGE:
                married_date = datetime.strptime(
                    n.get_child_elements()[0].get_value(), "%d %b %Y"
                ).strftime("%Y-%m-%d")
            if n.get_tag() == "DIV":
                divorced_date = datetime.strptime(
                    n.get_child_elements()[0].get_value(), "%d %b %Y"
                ).strftime("%Y-%m-%d")
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND:
                id = n.get_value()
                husband_id = clean_id(id)
                for p in individuals:
                    if p.get_pointer() == id:
                        (fist, last) = p.get_name()
                        husband_name = fist + " " + "/" + last + "/"
                        break
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE:
                id = n.get_value()
                wife_id = clean_id(id)
                for p in individuals:
                    if p.get_pointer() == id:
                        (fist, last) = p.get_name()
                        wife_name = fist + " " + "/" + last + "/"
                        break
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_CHILD:
                children.append("'" + clean_id(n.get_value()) + "'")
        f.append(married_date)
        f.append(divorced_date)
        f.append(husband_id)
        f.append(husband_name)
        f.append(wife_id)
        f.append(wife_name)
        if children != []:
            f.append("{" + ",".join(children) + "}")
        else:
            f.append("N/A")
        t.add_row(f)
    print("Families")
    print(t.get_string())

# US24
def check_unique_families(families):
    remainder = {}
    for f in families:
        husband_id = ""
        wife_id = ""
        married_date = ""
        for n in f.get_child_elements():
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_MARRIAGE:
                married_date = datetime.strptime(
                    n.get_child_elements()[0].get_value(), "%d %b %Y"
                ).strftime("%Y-%m-%d")
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND:
                husband_id = n.get_value()
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE:
                wife_id = n.get_value()
        if remainder.get((husband_id, wife_id)) == married_date:
              print("ERROR: FAMILY: US24: {}: more than one families have same spouses and same marriage date.".format(clean_id(f.get_pointer())))
        else:
            remainder[(husband_id, wife_id)] = married_date


if __name__ == "__main__":
    # Using python-gedcom to parse GEDCOM file.
    # DOCUMENT https://gedcom.nickreynke.dev/gedcom/index.html
    # Plase read the element moudle in the document.
    if len(sys.argv) == 1:
        exit()
    file_path = sys.argv[1]
    gedcom_parser = Parser()
    gedcom_parser.parse_file(file_path)

    root_child_elements = gedcom_parser.get_root_child_elements()

    # A list contains all individual elements, you can use it as a parameter.
    individuals = [i for i in root_child_elements if isinstance(i, IndividualElement)]
    # A list contains all family elements, you can use it as a parameter.
    families = [i for i in root_child_elements if isinstance(i, FamilyElement)]

    # Call your functions from here.
    pretty_individuals(individuals)
    pretty_families(families, individuals)
    check_unique_families(families)
