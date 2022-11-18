import sys
import unittest
from unittest.mock import patch

from gedcom.element.family import FamilyElement
from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser

from main import *
from main import (check_dupplicates_name_dob, check_unique_families,
                  check_unique_first_name, marry_after_14,birth_before_marriage02,birth_before_death03,marry_before_divor,divor_before_death)

NO_CHILD_TEST_EXAMPLE = "./testged/NO_CHILD_EXAMPLE.ged"
ONE_CHILD_TEST_EXAMPLE = "./testged/ONE_CHILD_EXAMPLE.ged"
TWO_CHILDREN_WITHOUT_SAME_NAME_TEST_EXAMPLE = (
    "./testged/TWO_CHILDREN_WITHOUT_SAME_NAME.ged"
)
TWO_CHILDREN_WITH_SAME_NAME_TEST_EXAMPLE = "./testged/TWO_CHILDREN_WITH_SAME_NAME.ged"
THREE_CHILDREN_WITH_SAME_NAME_TEST_EXAMPLE = (
    "./testged/THREE_CHILDREN_WITH_SAME_NAME.ged"
)
TWO_SAME_FAMILY_TEST_EXAMPLE = "./testged/TWO_SAME_FAMILY.ged"
DUPLICATES_MORE_THAN_TWO = "./testged/DUPLICATES_MORE_THAN_TWO.ged"
TWO_PAIRS_DUPLICATES_EXAMPLE = "./testged/TWO_PAIRS_DUPLICATES_EXAMPLE.ged"
NO_DUPLICATES_EXAMPLE = "./testged/NO_DUPLICATES_EXAMPLE.ged"
WRONG_GENDER_EXAMPLE = "./testged/WRONG_GENDER_EXAMPLE.ged"
UNIQUE_ID_EXAMPLE = "./testged/UNIQUE_ID_EXAMPLE.ged"

# US10 Test file
NO_MARRYERROR = "./testged/NO_MARRYERROR.ged"
ONE_MARRYERROR = "./testged/ONE_MARRYERROR.ged"
TWO_MARRYERROR = "./testged/TWO_MARRYERROR.ged"
THREE_MARRYERROR = "./testged/THREE_MARRYERROR.ged"
ONEPAIR_MARRYERROR = "./testged/ONEPAIR_MARRYERROR.ged"

#US01 Test files
BIRTH_DATES_AFTER_TODAY= "./testged/BIRTH_DATES_AFTER_TODAY.ged"
DEATH_DATES_AFTER_TODAY= "./testged/DEATH_DATES_AFTER_TODAY.ged"
DIVORCED_DATE_AFTER_TODAY= "./testged/DIVORCED_DATE_AFTER_TODAY.ged"
MARRIED_DATE_AFTER_TODAY= "./testged/MARRIED_DATE_AFTER_TODAY.ged"

#US13 Test files
MORE_THAN_FIVE_SIBLINGS="./testged/MORE_THAN_FIVE_SIBLINGS.ged"
NORMAL = "./testged/NORMAL.ged"

# US02 Test file
ONE_DEATHERROR = "./testged/ONE_DeathBeforeBirth.ged"
TWO_DEATHERROR = "./testged/TWO_DeathBeforeBirth.ged"
# US03 Test file
ONE_MbeforeD = "./testged/ONE_MbefD.ged"
TWO_MbeforeD = "./testged/TWO_MbefD.ged"
# US04 Test file
US04OneErr = "./testged/US04OneErr.ged"
US04TwoErr = "./testged/US04TwoErr.ged"
# US06 Test file
US06OneErr = "./testged/US06OneErr.ged"
US06TwoErr = "./testged/US06TwoErr.ged"

# US16 test file
DIFFERENT_NAME = "./testged/DIFFERENT_NAME.ged"
# US12 test file
PARENT_TOO_OLD = "./testged/PARENTS_TOO_OLD.ged"

# You can use this function to get families and individuals
def help_paser_ged(ged):
    gedcom_parser = Parser()
    gedcom_parser.parse_file(ged)
    root_child_elements = gedcom_parser.get_root_child_elements()
    individuals = [i for i in root_child_elements if isinstance(i, IndividualElement)]
    families = [i for i in root_child_elements if isinstance(i, FamilyElement)]
    return (families, individuals)


class TestClass(unittest.TestCase):
    def test_no_child(self):
        (families, individuals) = help_paser_ged(NO_CHILD_TEST_EXAMPLE)
        self.assertEqual(check_unique_first_name(families, individuals), None)

    def test_one_child(self):
        (families, individuals) = help_paser_ged(ONE_CHILD_TEST_EXAMPLE)
        self.assertEqual(check_unique_first_name(families, individuals), None)

    def test_two_children_without_same_name(self):
        (families, individuals) = help_paser_ged(
            TWO_CHILDREN_WITHOUT_SAME_NAME_TEST_EXAMPLE
        )
        self.assertEqual(check_unique_first_name(families, individuals), None)

    def test_two_children_with_same_name(self):
        (families, individuals) = help_paser_ged(
            TWO_CHILDREN_WITH_SAME_NAME_TEST_EXAMPLE
        )
        self.assertNotEqual(check_unique_first_name(families, individuals), None)

    def test_three_children_with_same_name(self):
        (families, individuals) = help_paser_ged(
            THREE_CHILDREN_WITH_SAME_NAME_TEST_EXAMPLE
        )
        self.assertNotEqual(check_unique_first_name(families, individuals), None)

    def test_unique_family(self):
        (families, individuals) = help_paser_ged(TWO_SAME_FAMILY_TEST_EXAMPLE)
        self.assertNotEqual(check_unique_families(families), None)

    # US23 Test
    def test_over_two_duplicates(self):
        (families, individuals) = help_paser_ged(DUPLICATES_MORE_THAN_TWO)
        self.assertNotEqual(check_dupplicates_name_dob(individuals), None)

    def test_two_pairs_example(self):
        (families, individuals) = help_paser_ged(TWO_PAIRS_DUPLICATES_EXAMPLE)
        self.assertNotEqual(check_dupplicates_name_dob(individuals), None)

    def test_no_duplicates_example(self):
        (families, individuals) = help_paser_ged(NO_DUPLICATES_EXAMPLE)
        self.assertEqual(check_dupplicates_name_dob(individuals), None)

    def test_same_name_example(self):
        (families, individuals) = help_paser_ged(
            TWO_CHILDREN_WITH_SAME_NAME_TEST_EXAMPLE)
        self.assertEqual(check_dupplicates_name_dob(individuals), None)

    def test_one_child_example(self):
        (families, individuals) = help_paser_ged(ONE_CHILD_TEST_EXAMPLE)
        self.assertEqual(check_dupplicates_name_dob(individuals), None)

    # US01 Test
    def test_birth_dates_after_today(self):
        (families, individuals) = help_paser_ged(BIRTH_DATES_AFTER_TODAY)
        self.assertEqual(check_future_dates(individuals,families), None)

    def test_birth_dates_after_today(self):
        (families, individuals) = help_paser_ged(BIRTH_DATES_AFTER_TODAY)
        self.assertEqual(check_future_dates(individuals,families), None)

    def test_death_dates_after_today(self):
        (families, individuals) = help_paser_ged(DEATH_DATES_AFTER_TODAY)
        self.assertEqual(check_future_dates(individuals,families), None)

    def test_divorced_dates_after_today(self):
        (families, individuals) = help_paser_ged(DIVORCED_DATE_AFTER_TODAY)
        self.assertEqual(check_future_dates(individuals,families), None)

    def test_married_dates_after_today(self):
        (families, individuals) = help_paser_ged(MARRIED_DATE_AFTER_TODAY)
        self.assertEqual(check_future_dates(individuals,families), None)


    # US13 Test
    def test_normal(self):
        (families, individuals) = help_paser_ged(NORMAL)
        self.assertEqual(no_more_than_five_c(families,individuals), None)
    
    def test_more_than_five_sibs(self):
        (families, individuals) = help_paser_ged(MORE_THAN_FIVE_SIBLINGS)
        self.assertEqual(no_more_than_five_c(families,individuals), None)
    
    def test_more_than_five_sibs(self):
        (families, individuals) = help_paser_ged(MORE_THAN_FIVE_SIBLINGS)
        self.assertEqual(no_more_than_five_c(families,individuals), None)
    
    def test_more_than_five_sibs(self):
        (families, individuals) = help_paser_ged(MORE_THAN_FIVE_SIBLINGS)
        self.assertEqual(no_more_than_five_c(families,individuals), None)

    def test_more_than_five_sibs(self):
        (families, individuals) = help_paser_ged(MORE_THAN_FIVE_SIBLINGS)
        self.assertEqual(no_more_than_five_c(families,individuals), None)

    # US10 Test
    def test_no_marryerror(self):
        (families, individuals) = help_paser_ged(NO_MARRYERROR)
        self.assertEqual(marry_after_14(families, individuals), None)

    def test_one_marryerror(self):
        (families, individuals) = help_paser_ged(ONE_MARRYERROR)
        self.assertEqual(marry_after_14(families, individuals), None)

    def test_two_marryerror(self):
        (families, individuals) = help_paser_ged(TWO_MARRYERROR)
        self.assertEqual(marry_after_14(families, individuals), None)

    def test_three_marryerror(self):
        (families, individuals) = help_paser_ged(THREE_MARRYERROR)
        self.assertEqual(marry_after_14(families, individuals), None)

    def test_onepair_marryerror(self):
        (families, individuals) = help_paser_ged(ONEPAIR_MARRYERROR)
        self.assertEqual(marry_after_14(families, individuals), None)

    # US02 Test
    def test_one_marriageerror(self):
        (families, individuals) = help_paser_ged(ONE_MbeforeD)
        self.assertEqual(birth_before_marriage02(families,individuals), None)

    def test_two_marriageerror(self):
        (families, individuals) = help_paser_ged(TWO_MbeforeD)
        self.assertEqual(birth_before_marriage02(families,individuals), None)

    # US03 Test
    def test_one_deatherror(self):
        (families, individuals) = help_paser_ged(ONE_DEATHERROR)
        self.assertEqual(birth_before_death03(individuals), None)

    def test_two_deatherror(self):
        (families, individuals) = help_paser_ged(TWO_DEATHERROR)
        self.assertEqual(birth_before_death03(individuals), None)

    # US04 Test
    def test_one_divErr(self):
        (families, individuals) = help_paser_ged(US04OneErr)
        self.assertEqual(marry_before_divor(families,individuals), None)

    def test_two_divErr(self):
        (families, individuals) = help_paser_ged(US04TwoErr)
        self.assertEqual(marry_before_divor(families,individuals), None)

    # US06 Test
    def test_one_deathErr(self):
        (families, individuals) = help_paser_ged(US06OneErr)
        self.assertEqual(divor_before_death(families,individuals), None)

    def test_two_deathErr(self):
        (families, individuals) = help_paser_ged(US06TwoErr)
        self.assertEqual(divor_before_death(families,individuals), None)

    # US21
    def test_correct_gender(self):
        (families, individuals) = help_paser_ged(WRONG_GENDER_EXAMPLE)
        self.assertIsNotNone(correct_gender(families, individuals))

    # US22
    def test_unique_id(self):
        (families, individuals) = help_paser_ged(UNIQUE_ID_EXAMPLE)
        self.assertIsNotNone(unique_id(families, individuals))
        
    # 30
    def test_birth_after_death(self):
        (families, individuals) = help_paser_ged(WRONG_GENDER_EXAMPLE)
        self.assertEqual(list_married(families, individuals), None)
    
    def test_birth_after_death(self):
        (families, individuals) = help_paser_ged(WRONG_GENDER_EXAMPLE)
        self.assertIsNotNone(list_married(families, individuals))
    
    # 31
    def test_birth_after_death(self):
        (families, individuals) = help_paser_ged(WRONG_GENDER_EXAMPLE)
        self.assertEqual(list_single(families, individuals), None)
    
    def test_birth_after_death(self):
        (families, individuals) = help_paser_ged(WRONG_GENDER_EXAMPLE)
        self.assertIsNotNone(list_single(families, individuals))
        
    # US 08
    def test_birth_before_marriage(self):
        (families, individuals) = help_paser_ged(WRONG_GENDER_EXAMPLE)
        self.assertEqual(birth_before_marriage(families, individuals), None)
    
    def test_birth_before_marriage(self):
        (families, individuals) = help_paser_ged(WRONG_GENDER_EXAMPLE)
        self.assertIsNotNone(birth_before_marriage(families, individuals))
    
    # US 09
    def test_birth_after_death(self):
        (families, individuals) = help_paser_ged(WRONG_GENDER_EXAMPLE)
        self.assertEqual(birth_after_death(families, individuals), None)
    
    def test_birth_after_death(self):
        (families, individuals) = help_paser_ged(WRONG_GENDER_EXAMPLE)
        self.assertIsNotNone(birth_after_death(families, individuals))

    #US 16
    def test_different_name(self):
        (families, individuals) = help_paser_ged(WRONG_GENDER_EXAMPLE)
        self.assertIsNotNone(family_with_same_last_name(families, individuals))
    #US 16
    def test_parent_too_ld(self):
        (families, individuals) = help_paser_ged(PARENT_TOO_OLD)
        self.assertIsNotNone(parents_is_not_too_old(families, individuals))
        
    #US 05
    def test_marry_before_death_1(self):
        (families, individuals) = help_paser_ged(ONE_MbeforeD)
        self.assertEqual(marry_before_death(families,individuals), None)

    def test_marry_before_death_2(self):
        (families, individuals) = help_paser_ged(TWO_MbeforeD)
        self.assertEqual(marry_before_death(families,individuals), None)
        
    def test_marry_before_death_3(self):
        (families, individuals) = help_paser_ged(PARENT_TOO_OLD)
        self.assertEqual(marry_before_death(families,individuals), None)
    
    def test_marry_before_death_4(self):
        (families, individuals) = help_paser_ged(MORE_THAN_FIVE_SIBLINGS)
        self.assertEqual(marry_before_death(families,individuals), None)
        
    def test_marry_before_death_5(self):
        (families, individuals) = help_paser_ged(NORMAL)
        self.assertEqual(marry_before_death(families,individuals), None)
    
    #US 17
    def test_marry_descendents_1(self):
        (families, individuals) = help_paser_ged(MORE_THAN_FIVE_SIBLINGS)
        self.assertEqual(marry_descendants(families,individuals), None)
    
    def test_marry_descendents_2(self):
        (families, individuals) = help_paser_ged(TWO_PAIRS_DUPLICATES_EXAMPLE)
        self.assertEqual(marry_descendants(families,individuals), None)
    
    def test_marry_descendents_3(self):
        (families, individuals) = help_paser_ged(ONEPAIR_MARRYERROR)
        self.assertEqual(marry_descendants(families,individuals), None)
    
    def test_marry_descendents_4(self):
        (families, individuals) = help_paser_ged(TWO_MbeforeD)
        self.assertEqual(marry_descendants(families,individuals), None)
    
    def test_marry_descendents_5(self):
        (families, individuals) = help_paser_ged(UNIQUE_ID_EXAMPLE)
        self.assertEqual(marry_descendants(families,individuals), None)
    
    # US 38
    def test_upcoming_birth_1(self):
        (families, individuals) = help_paser_ged(MORE_THAN_FIVE_SIBLINGS)
        self.assertEqual(upcoming_birthday(families,individuals), None)
    
    def test_upcoming_birth_2(self):
        (families, individuals) = help_paser_ged(TWO_PAIRS_DUPLICATES_EXAMPLE)
        self.assertEqual(upcoming_birthday(families,individuals), None)
    
    def test_upcoming_birth_3(self):
        (families, individuals) = help_paser_ged(ONEPAIR_MARRYERROR)
        self.assertEqual(upcoming_birthday(families,individuals), None)
    
    def test_upcoming_birth_4(self):
        (families, individuals) = help_paser_ged(TWO_MbeforeD)
        self.assertEqual(upcoming_birthday(families,individuals), None)
    
    def test_marry_descendents_5(self):
        (families, individuals) = help_paser_ged(UNIQUE_ID_EXAMPLE)
        self.assertEqual(upcoming_birthday(families,individuals), None)
    
    # US 39
    def test_upcoming_anniversaries_1(self):
        (families, individuals) = help_paser_ged(MORE_THAN_FIVE_SIBLINGS)
        self.assertEqual(upcoming_anniversaries(families,individuals), None)
    
    def test_upcoming_anniversaries_2(self):
        (families, individuals) = help_paser_ged(TWO_PAIRS_DUPLICATES_EXAMPLE)
        self.assertEqual(upcoming_anniversaries(families,individuals), None)
    
    def test_upcoming_anniversaries_3(self):
        (families, individuals) = help_paser_ged(ONEPAIR_MARRYERROR)
        self.assertEqual(upcoming_anniversaries(families,individuals), None)
    
    def test_upcoming_anniversaries_4(self):
        (families, individuals) = help_paser_ged(TWO_MbeforeD)
        self.assertEqual(upcoming_anniversaries(families,individuals), None)
    
    def test_upcoming_anniversaries_5(self):
        (families, individuals) = help_paser_ged(UNIQUE_ID_EXAMPLE)
        self.assertEqual(upcoming_anniversaries(families,individuals), None)


# class test_us30_1(unittest.TestCase):
#     @patch.object(sys, "argv", ["main.py", "Homework.ged"])
#     def test_list_married(self):
#         self.assertEqual(list_married(), 0)


# class test_us30_2(unittest.TestCase):
#     @patch.object(sys, "argv", ["main.py", "ONE_CHILD_TEST_EXAMPLE"])
#     def test_list_married(self):
#         self.assertEqual(list_married(), 0)


# class test_us30_3(unittest.TestCase):
#     @patch.object(sys, "argv", ["main.py", "NO_CHILD_TEST_EXAMPLE"])
#     def test_list_married(self):
#         self.assertEqual(list_married(), 0)


# class test_us31(unittest.TestCase):
#     @patch.object(sys, "argv", ["main.py", "Homework.ged"])
#     def test_living_singles(self):
#         self.assertNotEqual(list_single(), 0)


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
