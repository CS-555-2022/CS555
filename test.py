import sys
import unittest
from unittest.mock import patch

from gedcom.element.family import FamilyElement
from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser

from main import *
from main import (check_dupplicates_name_dob, check_unique_families,
                  check_unique_first_name, marry_after_14)

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
            TWO_CHILDREN_WITH_SAME_NAME_TEST_EXAMPLE
        )
        self.assertEqual(check_dupplicates_name_dob(individuals), None)

    def test_one_child_example(self):
        (families, individuals) = help_paser_ged(ONE_CHILD_TEST_EXAMPLE)
        self.assertEqual(check_dupplicates_name_dob(individuals), None)

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

    # US21
    def test_correct_gender(self):
        (families, individuals) = help_paser_ged(WRONG_GENDER_EXAMPLE)
        self.assertIsNotNone(correct_gender(families, individuals))

    # US22
    def test_unique_id(self):
        (families, individuals) = help_paser_ged(UNIQUE_ID_EXAMPLE)
        self.assertIsNotNone(unique_id(families, individuals))
        
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


class test_us30_1(unittest.TestCase):
    @patch.object(sys, "argv", ["main.py", "Homework.ged"])
    def test_list_married(self):
        self.assertEqual(list_married(), 0)


class test_us30_2(unittest.TestCase):
    @patch.object(sys, "argv", ["main.py", "ONE_CHILD_TEST_EXAMPLE"])
    def test_list_married(self):
        self.assertEqual(list_married(), 0)


class test_us30_3(unittest.TestCase):
    @patch.object(sys, "argv", ["main.py", "NO_CHILD_TEST_EXAMPLE"])
    def test_list_married(self):
        self.assertEqual(list_married(), 0)


class test_us31(unittest.TestCase):
    @patch.object(sys, "argv", ["main.py", "Homework.ged"])
    def test_living_singles(self):
        self.assertNotEqual(list_single(), 0)


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
