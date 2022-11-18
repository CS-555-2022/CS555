import datetime
import sys
from datetime import date

import gedcom.tags
from gedcom.element.element import Element
from gedcom.element.family import FamilyElement
from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
from matplotlib.pyplot import get
from prettytable import PrettyTable

# from US30_31_help_code import *


#(US27)
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
        birthday = datetime.datetime.strptime(i.get_birth_data()[0], "%d %b %Y")
        f.append(birthday.strftime("%Y-%m-%d"))
        f.append(calculate_age(birthday))
        f.append(not i.is_deceased())
        if i.get_death_data()[0] != "":
            deathday = datetime.datetime.strptime(i.get_death_data()[0], "%d %b %Y")
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
                married_date = datetime.datetime.strptime(
                    n.get_child_elements()[0].get_value(), "%d %b %Y"
                ).strftime("%Y-%m-%d")
            if n.get_tag() == "DIV":
                divorced_date = datetime.datetime.strptime(
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
                married_date = datetime.datetime.strptime(
                    n.get_child_elements()[0].get_value(), "%d %b %Y"
                ).strftime("%Y-%m-%d")
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND:
                husband_id = n.get_value()
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE:
                wife_id = n.get_value()
        if remainder.get((husband_id, wife_id)) == married_date:
              return "ERROR: FAMILY: US24: {}: more than one families have same spouses and same marriage date.".format(clean_id(f.get_pointer()))
        else:
            remainder[(husband_id, wife_id)] = married_date


# US23
def check_dupplicates_name_dob(individuals):
    check_list=[]
    for individual in individuals:
        check_list.append((individual.get_name(),individual.get_birth_data()))
    dup = [individuals[check_list.index(person,ind_p)].get_pointer() for ind_p,person in enumerate(check_list) if check_list.count(person) > 1]
    if len(dup)!=0 :
        return "ERROR: INDIVIDUAL: US23: {}: Duplicates with same name and date of birth appear.".format(dup)



# US25
def check_unique_first_name(families, individuals):
    for f in families:
        remainder = []
        for n in f.get_child_elements():
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_CHILD:
                for i in individuals:
                    if i.get_pointer() == n.get_value():
                        if i.get_name() in remainder:
                            (first, _) = i.get_name()
                            return "ERROR: FAMILY: US24: {}: in a family have more than one children have same first name: {}.".format(clean_id(f.get_pointer()), first)
                        else:
                            remainder.append(i.get_name())

# US30

# file_name = sys.argv[1]
# info = get_info(file_name)

# def list_married():
#     for fam in info['families']:	
#         if fam['married'] != None:
#             print(" Married people (husband, wife): " + str(fam['husband_name']) + str(fam['wife_name']))
#     return 0

def list_married(families, individuals):
    for fam in families:
        for f in fam.get_child_elements():
            if f.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE:
                wife_id = f.get_value()

            if f.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND:
                husband_id = f.get_value()
                
        # print(wife_id, husband_id)
        for i in individuals:
            if i.get_pointer() == wife_id:
                wife = i.get_name()
                wife_name = ""
                for n in wife:
                    wife_name += " " + str(n)
                wife_name = wife_name.strip()
                # print(wife_name)
            if i.get_pointer() == husband_id:
                husband = i.get_name()
                husband_name = ""
                for n in husband:
                    husband_name += " " + str(n)
                husband_name = husband_name.strip()
                # print(husband_name)
        print(" Married people (husband, wife): " + husband_name + wife_name)
        # name_list.append(" Married people (husband, wife): " + husband_name + wife_name)
    # print(name_list)
        
            
# US31

# def list_single():
# 	file_name = sys.argv[1]
# 	info = get_info(file_name)
# 	alone_forever = []
# 	for ind in info['individuals']:
# 		birth = ind['birthday']
# 		dt = datetime.datetime.now() - datetime.timedelta(days=30*365)
# 		if birth < dt and ind['spouse'] == None:
# 			alone_forever.append(ind['id'])

# 	if len(alone_forever) == 0:
# 		return 1
# 	else:
# 		print(alone_forever)
# 	return 0

def list_single(families, individuals):
    married = set()
    for fam in families:
        for f in fam.get_child_elements():
            # print(f)
            if f.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE or f.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND:
                married.add(f.get_value())
        
    # print(married)
    alone = []
    for i in individuals:
        if i.get_pointer() not in married:
            birth = i.get_birth_year()
            # print(birth)
            diff = datetime.datetime.today().year - birth
            # print(diff)
            if diff > 30:
                alone.append(i.get_pointer())
    if alone:
        print(alone)
    else:
        return 0

# US07
def less_than_150(individuals):
    thisYear = date.today().year
    for i in individuals:
        death = i.get_death_year()
        birth = i.get_birth_year()
        if death != -1 and death - birth >= 150:
            return "ERROR: INDIVIDAL: US07: Death should be less than 150 years after birth for dead people, and current date should be less than 150 years after birth for all living people, NAME: {}.".format('-'.join(str(x) for x in i.get_name()))
        elif death == -1 and thisYear - birth >= 150:
            return "ERROR: INDIVIDAL: US07: Death should be less than 150 years after birth for dead people, and current date should be less than 150 years after birth for all living people, NAME: {}.".format('-'.join(str(x) for x in i.get_name()))
    
# US10
def marry_after_14(families,individuals):
    married_year = ""
    husband_ID = ""
    wife_ID = ""
    husName = ""
    wifeName = ""
    husBirthYear = ""
    wifeBirthYear = ""
    for fam in families:
        for n in fam.get_child_elements():
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_MARRIAGE:
                married_year = datetime.datetime.strptime(n.get_child_elements()[0].get_value(), "%d %b %Y").strftime("%Y")
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND:
                husband_ID = n.get_value()
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE:
                wife_ID = n.get_value()
        for m in individuals:
            if m.get_pointer() == husband_ID:
                husName = '-'.join(str(x) for x in m.get_name())
                husBirthYear = m.get_birth_year()
            if m.get_pointer() == wife_ID:
                wifeName = '-'.join(str(x) for x in m.get_name())
                wifeBirthYear = m.get_birth_year()
        #print(married_year,husBirthYear,wifeBirthYear,husName,wifeName)   
        if int(married_year) - int(husBirthYear) < 14 or int(married_year) - int(wifeBirthYear) < 14:
                return "ERROR: INDIVIDAL: US10: Marriage should be at least 14 years after birth of both spouses, NAME: {} and {}.".format(husName, wifeName)

# US02
def birth_before_marriage02(families,individuals):
    married_date = ""
    husband_ID = ""
    wife_ID = ""
    husName = ""
    wifeName = ""
    husBirthDate = ""
    wifeBirthDate = ""
    for fam in families:
        for n in fam.get_child_elements():
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_MARRIAGE:
                married_date = datetime.datetime.strptime(n.get_child_elements()[0].get_value(), "%d %b %Y")
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND:
                husband_ID = n.get_value()
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE:
                wife_ID = n.get_value()
        for m in individuals:
            if m.get_pointer() == husband_ID:
                husName = '-'.join(str(x) for x in m.get_name())
                husBirthDate = datetime.datetime.strptime(m.get_birth_data()[0], "%d %b %Y")
            if m.get_pointer() == wife_ID:
                wifeName = '-'.join(str(x) for x in m.get_name())
                wifeBirthDate = datetime.datetime.strptime(m.get_birth_data()[0], "%d %b %Y")
        #print(married_date,husBirthDate,wifeBirthDate,husName,wifeName)   
        if married_date <= husBirthDate:
            print( "ERROR: INDIVIDAL: US02: Birth should occur before marriage of an individual, NAME: {}.".format(husName))
        if married_date <= wifeBirthDate:
            print( "ERROR: INDIVIDAL: US02: Birth should occur before marriage of an individual, NAME: {}.".format(wifeName))

# US03
def birth_before_death03(individuals):
    birth_date = ""
    death_date = ""
    currentname = ""
    for i in individuals:
        birth_date = datetime.datetime.strptime(i.get_birth_data()[0], "%d %b %Y")
        currentname = '-'.join(str(x) for x in i.get_name())
        if i.get_death_data()[0] != "":
            death_date = datetime.datetime.strptime(i.get_death_data()[0], "%d %b %Y")
        else:
            death_date = "N/A"
        #print(death_date, birth_date, currentname)
        if death_date != "N/A" and death_date <= birth_date:
            print( "ERROR: INDIVIDAL: US03: Birth should occur before death of an individual, NAME: {}.".format(currentname))

# US04
def marry_before_divor(families,individuals):
    for fam in families:
        married_date = ""
        divorced_date = "N/A"
        husband_ID = ""
        wife_ID = ""
        husName = ""
        wifeName = ""
        for n in fam.get_child_elements():
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_MARRIAGE:
                married_date = datetime.datetime.strptime(n.get_child_elements()[0].get_value(), "%d %b %Y")
            if n.get_tag() == "DIV":
                divorced_date = datetime.datetime.strptime(n.get_child_elements()[0].get_value(), "%d %b %Y")
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND:
                husband_ID = n.get_value()
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE:
                wife_ID = n.get_value()
        for m in individuals:
            if m.get_pointer() == husband_ID:
                husName = '-'.join(str(x) for x in m.get_name())
            if m.get_pointer() == wife_ID:
                wifeName = '-'.join(str(x) for x in m.get_name())
        #print(married_date,divorced_date,husName,wifeName)
        if divorced_date != "N/A" and divorced_date < married_date:
            print( "ERROR: FAMILY: US04: Marriage should occur before divorce of spouses, and divorce can only occur after marriage, NAME: {} and {}.".format(husName, wifeName))

# US05
def marry_before_death(families, individuals):
    for fam in families:
        married_data = "N/A"
        husDeathDate = "N/A"
        wifeDeathDate = "N/A"
        husband_ID = ""
        wife_ID = ""
        hus_name = ""
        wife_name = ""
        for n in fam.get_child_elements():
            # print(n.get_tag())
            # print(gedcom.tags.GEDCOM_TAG_MARRIAGE)
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_MARRIAGE:
                married_data = datetime.datetime.strptime(n.get_child_elements()[0].get_value(), "%d %b %Y")
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND:
                husband_ID = n.get_value()
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE:
                wife_ID = n.get_value()
        for m in individuals:
            if m.get_pointer() == husband_ID:
                hus_name = '-'.join(str(x) for x in m.get_name())
                if m.get_death_data()[0] != "":
                    husDeathDate = datetime.datetime.strptime(m.get_death_data()[0], "%d %b %Y")
                else:
                    husDeathDate = "N/A"
            if m.get_pointer() == wife_ID:
                wife_name = '-'.join(str(x) for x in m.get_name())
                if m.get_death_data()[0] != "":
                    wifeDeathDate = datetime.datetime.strptime(m.get_death_data()[0], "%d %b %Y")
                else:
                    wifeDeathDate = "N/A"
        
        if married_data != "N/A" and husDeathDate != "N/A":
            if married_data > husDeathDate:
                print("ERROR: FAMILY: US05: Marry data can only occur before death of both spouses(husband), NAME: {} and {}.".format(hus_name, wife_name))
        if married_data != "N/A" and wifeDeathDate != "N/A":
            if married_data > wifeDeathDate:
                print("ERROR: FAMILY: US05: Marry data can only occur before death of both spouses(wife), NAME: {} and {}.".format(hus_name, wife_name))
                    
    
# US06
def divor_before_death(families,individuals):
    for fam in families:
        divorced_date = "N/A"
        husband_ID = ""
        wife_ID = ""
        husName = ""
        wifeName = ""
        husDeathDate = ""
        wifeDeathDate = ""
        for n in fam.get_child_elements():
            if n.get_tag() == "DIV":
                divorced_date = datetime.datetime.strptime(n.get_child_elements()[0].get_value(), "%d %b %Y")
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND:
                husband_ID = n.get_value()
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE:
                wife_ID = n.get_value()
        for m in individuals:
            if m.get_pointer() == husband_ID:
                husName = '-'.join(str(x) for x in m.get_name())
                if m.get_death_data()[0] != "":
                    husDeathDate = datetime.datetime.strptime(m.get_death_data()[0], "%d %b %Y")
                else:
                    husDeathDate = "N/A"
            if m.get_pointer() == wife_ID:
                wifeName = '-'.join(str(x) for x in m.get_name())
                if m.get_death_data()[0] != "":
                    wifeDeathDate = datetime.datetime.strptime(m.get_death_data()[0], "%d %b %Y")
                else:
                    wifeDeathDate = "N/A"
        #print(divorced_date,husName,husDeathDate,wifeName,wifeDeathDate)
        if divorced_date != "N/A" and husDeathDate != "N/A":
            if divorced_date > husDeathDate:
                print( "ERROR: FAMILY: US06: Divorce can only occur before death of both spouses(husband), NAME: {} and {}.".format(husName, wifeName))
        if divorced_date != "N/A" and wifeDeathDate != "N/A":
            if divorced_date > wifeDeathDate:
                print( "ERROR: FAMILY: US06: Divorce can only occur before death of both spouses(wife), NAME: {} and {}.".format(husName, wifeName))    
     
# US21 
def correct_gender(families, individuals):
    result = None
    for f in families:
        for n in f.get_child_elements():
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND:
                for i in individuals:
                    if i.get_pointer() == n.get_value():
                       for child in i.get_child_elements():
                           if child.get_tag() == gedcom.tags.GEDCOM_TAG_SEX:
                                if child.get_value() != "M":
                                    result = f.get_pointer()
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE:
                for i in individuals:
                    if i.get_pointer() == n.get_value():
                       for child in i.get_child_elements():
                           if child.get_tag() == gedcom.tags.GEDCOM_TAG_SEX:
                                if child.get_value() != "F":
                                    result = f.get_pointer()
    if result:
        return "ERROR: INDIVIDAL: US21: {} familiy's gender is not correct".format(result)

#US 22
def unique_id(families, individuals):
    remainder = {}
    result = []
    for f in families:
        if f.get_pointer() in remainder:
            result.append(f.get_pointer())
        else:
            remainder[f.get_pointer()] = True
    for i in individuals:
        if i.get_pointer() in remainder:
            result.append(i.get_pointer())
        else:
            remainder[i.get_pointer()] = True
    if result != []:
        return "ERROR: INDIVIDAL: US22: {} is not unique".format(result)


# US 08
def birth_before_marriage(families,individuals):
    parent_children = []
    for fam in families:
        for f in fam.get_child_elements():
            # print(f)
            if f.get_tag() == gedcom.tags.GEDCOM_TAG_MARRIAGE:
                # print(f.get_child_elements())
                # print(datetime.datetime.strptime(f.get_child_elements()[0].get_value(), "%d %b %Y"))
                married_data = datetime.datetime.strptime(f.get_child_elements()[0].get_value(), "%d %b %Y")
                # print(married_data)
            if f.get_tag() == gedcom.tags.GEDCOM_TAG_CHILD:
                child_ID = f.get_value()
                # print(child_ID)
            
        for i in individuals:
            if i.get_pointer() == child_ID:
                # print(i.get_birth_data())
                
                childBirth = datetime.datetime.strptime(i.get_birth_data()[0], "%d %b %Y")
                # print(married_data, child_ID, childBirth)
                parent_children.append((married_data, child_ID, childBirth))
                
    # print(parent_children)     
    cnt = 0      
    for pair in parent_children:
        # print(pair)
        married_day = pair[0]
        child_birth = pair[2]
        child = pair[1]
        # print(child_birth, married_day)
        if(child_birth < married_day):
            print("ANOMALY: FAMILY: US08: " + " Child " + str(child) + " born " + str(child_birth) + " before marriage on " + str(married_day))
            cnt += 1
        
    # print(cnt)   
    return cnt        


# US 9
def birth_after_death(families, individuals):
    child_parent = []
            
    for fam in families:
        for f in fam.get_child_elements():
            for i in individuals:
                death = i.get_death_year()
                if death != -1:
                    death_date = datetime.datetime.strptime(i.get_death_data()[0], "%d %b %Y")    
                else:
                    death_date = None
                
                if f.get_tag() == gedcom.tags.GEDCOM_TAG_CHILD:
                    # print(f.get_value())
                    if f.get_value() == i.get_pointer():
                        childBirth = datetime.datetime.strptime(i.get_birth_data()[0], "%d %b %Y")
                        # print(death_date,childBirth)
                        child_parent.append((death_date, f.get_value(), childBirth))
    
    cnt = 0
    for pair in child_parent:
        death_day = pair[0]
        child_id = pair[1]
        child_birth = pair[2]
        if death_day and death_day < child_birth:
            print("ERROR: FAMILY: US09: " + child_id + ": Birthday " + child_birth + " born before parents death day: " + death_day)
            cnt += 1
    return cnt                   
                        
            




# US01
def check_future_dates(individuals,families):
    ierrorlist=[]
    ferrorlist=[]
    Today=date.today()
    for i in individuals:
        if i.get_death_data()[0] != '':
            if date.fromisoformat(datetime.datetime.strptime(i.get_death_data()[0], "%d %b %Y").strftime("%Y-%m-%d")) > Today:
                print("ERROR: INDIVIDUAL: US01: {}: Death Date after the current date.".format(i.get_pointer()))

        if date.fromisoformat(datetime.datetime.strptime(i.get_birth_data()[0], "%d %b %Y").strftime("%Y-%m-%d")) > Today:
            print("ERROR: INDIVIDUAL: US01: {}: Birth Date after the current date.".format(i.get_pointer()))

    
    for f in families:
        for n in f.get_child_elements():
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_MARRIAGE:
                married_date = datetime.datetime.strptime(n.get_child_elements()[0].get_value(), "%d %b %Y").strftime("%Y-%m-%d")
                if date.fromisoformat(married_date) > Today:
                    print("ERROR: INDIVIDUAL: US01: {}: Married Date after the current date.".format(f.get_pointer()))
            if n.get_tag() == "DIV":
                divorced_date = datetime.datetime.strptime(n.get_child_elements()[0].get_value(), "%d %b %Y").strftime("%Y-%m-%d")
                if date.fromisoformat(divorced_date) > Today:
                    print("ERROR: INDIVIDUAL: US01: {}: Divorced Date after the current date.".format(f.get_pointer()))
    

# US14
def no_more_than_five_c(families,individuals):

    for fam in families:
        flag=False
        fammem=[]
        birth_dates=[]
        for f in fam.get_child_elements():
            if f.get_tag() == gedcom.tags.GEDCOM_TAG_CHILD:
                fammem.append(f.get_value())
        
        if len(fammem) >= 5:
            for i in individuals:
                if i.get_pointer() in fammem:
                    birth_dates.append(datetime.datetime.strptime(i.get_birth_data()[0], "%d %b %Y").strftime("%Y-%m-%d"))
            for each in birth_dates:
                if birth_dates.count(each) >= 5:
                    flag=True
        if flag == True:
            print("ERROR: FAMILIES: US13: {}: More than five siblings borned at the same date.".format(fam.get_pointer()))
            #         if child == i.get_value():
            #             birth_dates.append(datetime.datetime.strptime(i.get_birth_data()[0], "%d %b %Y").strftime("%Y-%m-%d"))
            # print(birth_dates)     

# US16
def family_with_same_last_name(families, individuals):
    for f in families:
        name = ""
        for n in f.get_child_elements():
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND or n.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE or n.get_tag() == gedcom.tags.GEDCOM_TAG_CHILD:
                for i in individuals:
                    if i.get_pointer() == n.get_value():
                        if name != "" and i.get_name()[1] != name:
                            return "ERROR: FAMILY: US16: {} family with different last name.".format(f.get_pointer())
                        elif name == "":
                            name = i.get_name()[1]
    return None
# US12
def parents_is_not_too_old(families, individuals):
    for f in families:
        age = 0
        for n in f.get_child_elements():
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_CHILD:
                for i in individuals:
                    if i.get_pointer() == n.get_value():
                        birthday = datetime.datetime.strptime(i.get_birth_data()[0], "%d %b %Y")
                        age = max(age, calculate_age(birthday))
        for n in f.get_child_elements():
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND:
                for i in individuals:
                    if i.get_pointer() == n.get_value():
                        birthday = calculate_age(datetime.datetime.strptime(i.get_birth_data()[0], "%d %b %Y"))
                        if age != 0 and (birthday - age) > 80:
                            return "ERROR:US12: {} family's parents is too old".format(f.get_pointer())
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE:
                for i in individuals:
                    if i.get_pointer() == n.get_value():
                        birthday = calculate_age(datetime.datetime.strptime(i.get_birth_data()[0], "%d %b %Y"))
                        if age != 0 and (birthday - age) > 60:
                            return "ERROR:US12: {} family's parents is too old".format(f.get_pointer())
    return None

#US17
def marry_descendants(families, individuals):
    child = set()
    spouse = dict()
    spouse_ID = "N/A"
    spouse_name = "N/A"
    error_name = "N/A"
    for fam in families:
        for n in fam.get_child_elements():
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_CHILD:
              # print(n.get_value())
                child.add(n.get_value())
            # print(n)

        
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE or n.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND:
                spouse_ID = n.get_value()
                for m in individuals:
                    if m.get_pointer() == spouse_ID:
                        spouse_name = '-'.join(str(x) for x in m.get_name())
                        spouse[spouse_ID] = spouse_name
                      
    for c in child:
        if c in spouse:
            error_name = spouse[c]    
            print("Error: US17: Cannot marry with descendents, {} is not correct".format(error_name))
                
    # print("child: {}".format(child))
    # print("spouse: {}".format(spouse))
            
# US38 39 helper function
def next_30_day():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    # print(now_time)
    now_time_li = now_time.split('-')
    for i in range(len(now_time_li)):
        now_time_li[i] = int(now_time_li[i])
        
    max_day = [31, 27, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if now_time_li[0] % 100 == 0:
        if now_time_li[0] % 4 == 0:
            max_day[1] = 28
    elif now_time_li[0] % 4 == 0:
        max_day[1] = 28
    
    next_day_li = now_time_li
    mon = now_time_li[1]
    
    if now_time_li[2] + 30 > max_day[mon - 1]:
        next_day_li[2] = now_time_li[2] + 30 - max_day[mon - 1]
        next_day_li[1] = now_time_li[1] + 1
        
    return next_day_li
    
# US 38
def upcoming_birthday(families, individuals):
    next_day_li = next_30_day()
    upcoming = []
    cnt = 0
    
    # print(next_day_li)
    
    mon_data = ("", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
    for i in individuals:
        # print(i.get_name())
        death = i.get_death_year()
        if death != -1:
            continue    
        else:
            # death_date = None
            birth = i.get_birth_data()[0]
            bir_list = birth.split(" ")
            if mon_data[next_day_li[1]] == bir_list[1] and next_day_li[2] == int(bir_list[0]):
                upcoming.append(i.get_name())
        
        # print(bir_list)
    
    if len(upcoming):
        for name in upcoming:
            cnt += 1
            print("All living people in a GEDCOM file whose birthdays occur in the next 30 days is: " + str(name))
    return cnt

# US39   
def upcoming_anniversaries(families, individuals):
    next_day_li = next_30_day()
    # print(next_day_li)
    upcoming = []
    cnt = 0
    mon_data = ("", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
    for fam in families:
        wife_ID = ""
        hus_ID = ""
        hus_Name = ""
        wife_Name = ""
        married_date = ""
        divorced_date = "N/A"
        
        for n in fam.get_child_elements():
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_MARRIAGE:
                married_date = n.get_child_elements()[0].get_value()
                married_list = married_date.split(" ")
                # print(married_list)
            if n.get_tag() == "DIV":
                divorced_date = datetime.datetime.strptime(n.get_child_elements()[0].get_value(), "%d %b %Y")
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND:
                hus_ID = n.get_value()
            if n.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE:
                wife_ID = n.get_value()
            # print(divorced_date)
        for m in individuals:
            if m.get_pointer() == hus_ID:
                husName = '-'.join(str(x) for x in m.get_name())
            if m.get_pointer() == wife_ID:
                wifeName = '-'.join(str(x) for x in m.get_name())
            if divorced_date == "N/A":
                # print("in")
                # print(int(married_list[0]) == next_day_li[2] and mon_data[next_day_li[1]] == married_date[1])
                if int(married_list[0]) == next_day_li[2] and mon_data[next_day_li[1]] == married_date[1]:
                    upcoming.append("The husband name is: " + str(hus_Name) + "The wife name is: " + str(wife_Name))
        
    if len(upcoming):
        for name in upcoming:
            cnt += 1
            print("All living couples in a GEDCOM file whose marriage anniversaries occur in the next 30 days: " + str(name))
    
    return cnt


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
    if check_unique_families(families): print(check_unique_families(families))
    if check_unique_first_name(families, individuals): print(check_unique_first_name(families, individuals))
    # list_married()
    # list_single()
    list_married(families, individuals)
    list_single(families, individuals)
    if check_dupplicates_name_dob(individuals): print(check_dupplicates_name_dob(individuals))
    if less_than_150(individuals): print(less_than_150(individuals))
    if marry_after_14(families,individuals): print(marry_after_14(families,individuals))
    if correct_gender(families, individuals): print(correct_gender(families, individuals))
    if unique_id(families, individuals): print(unique_id(families, individuals))
    if birth_before_marriage(families, individuals): print(birth_before_marriage(families, individuals))
    if birth_after_death(families, individuals): print(birth_after_death(families, individuals))
    if birth_before_marriage02(families,individuals): print(birth_before_marriage02(families,individuals))
    if birth_before_death03(individuals): print(birth_before_death03(individuals))
    if no_more_than_five_c(families,individuals): print(no_more_than_five_c(families,individuals))
    if check_future_dates(individuals,families): print(check_future_dates(individuals,families))
    if marry_before_divor(families,individuals): print(marry_before_divor(families,individuals))
    if divor_before_death(families,individuals): print(divor_before_death(families,individuals))
    if family_with_same_last_name(families,individuals): print(family_with_same_last_name(families, individuals))
    if parents_is_not_too_old(families,individuals): print(parents_is_not_too_old(families, individuals))
    if marry_before_death(families, individuals):print(marry_before_death(families, individuals))
    if(marry_descendants(families, individuals)): print(marry_descendants(families, individuals))
    upcoming_birthday(families, individuals)
    upcoming_anniversaries(families, individuals)
