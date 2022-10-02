import unittest
from gedcom.parser import Parser
from gedcom.element.individual import IndividualElement
from gedcom.element.family import FamilyElement
from main import check_unique_first_name
from main import check_unique_families 

NO_CHILD_TEST_EXAMPLE = "./testged/NO_CHILD_EXAMPLE.ged"
ONE_CHILD_TEST_EXAMPLE = "./testged/ONE_CHILD_EXAMPLE.ged"
TWO_CHILDREN_WITHOUT_SAME_NAME_TEST_EXAMPLE = "./testged/TWO_CHILDREN_WITHOUT_SAME_NAME.ged"
TWO_CHILDREN_WITH_SAME_NAME_TEST_EXAMPLE = "./testged/TWO_CHILDREN_WITH_SAME_NAME.ged"
THREE_CHILDREN_WITH_SAME_NAME_TEST_EXAMPLE = "./testged/THREE_CHILDREN_WITH_SAME_NAME.ged"
TWO_SAME_FAMILY_TEST_EXAMPLE = "./testged/TWO_SAME_FAMILY.ged"

#You can use this function to get families and individuals
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
        (families, individuals) = help_paser_ged(TWO_CHILDREN_WITHOUT_SAME_NAME_TEST_EXAMPLE)
        self.assertEqual(check_unique_first_name(families, individuals), None)

    def test_two_children_with_same_name(self):
        (families, individuals) = help_paser_ged(TWO_CHILDREN_WITH_SAME_NAME_TEST_EXAMPLE)
        self.assertNotEqual(check_unique_first_name(families, individuals), None)

    def test_three_children_with_same_name(self):
        (families, individuals) = help_paser_ged(THREE_CHILDREN_WITH_SAME_NAME_TEST_EXAMPLE)
        self.assertNotEqual(check_unique_first_name(families, individuals), None)

    def test_unique_family(self):
        (families, individuals) = help_paser_ged(TWO_SAME_FAMILY_TEST_EXAMPLE)
        self.assertNotEqual(check_unique_families(families), None)

if __name__ == '__main__':
    unittest.main()
