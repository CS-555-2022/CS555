import sys
import unittest
from unittest.mock import patch

from gedcom.element.family import FamilyElement
from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser

from main import *
from main import (check_dupplicates_name_dob, check_unique_families,
                  check_unique_first_name, marry_after_14,birth_before_marriage02,birth_before_death03)

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
