# Yiwen Wang

import unittest
from main import *
from datetime import *
from dateutil.parser import parse
from unittest.mock import patch
from io import StringIO
import sys
# from US30 import *
# from US31 import *


def list_married(name, id, death, spouse):
        if (death == "N/A" and spouse != "N/A"):
            info_str = f"Info US30: {name} ({id}) is alive and married."
            print(info_str)
            return(info_str)
        else:
            return
        
def list_single(age, spouse, name, alive, id):
        if (spouse == "N/A" and age > 30 and alive):
            info_str = f"Info US31: {name} ({id}) is over 30 years old and not married."
            print(info_str)
            return info_str
        else:
            return
 
    
class TestGedcom(unittest.TestCase):
    
    def test_married_pass(self):
        self.assertEqual(list_married("Winston Cyan", "@I1@", "N/A", "@F1@"), "Info US30: Winston Cyan (@I1@) is alive and married.")
        self.assertEqual(list_married("Pete Johnie", "@I8@", "N/A", "@F5@"), "Info US30: Pete Johnie (@I8@) is alive and married.")
        self.assertEqual(list_married("Richa Isidora", "@I6@", "N/A", "@F2@"), "Info US30: Richa Isidora (@I6@) is alive and married.")
        self.assertEqual(list_married("Rona Cyan", "@I7@", "N/A", "@F4@"), "Info US30: Rona Cyan (@I7@) is alive and married.")
    def test_married_fail(self):
        self.assertNotEqual(list_married("Orson Cyan", "@I5@", "N/A", "@F2@"), "Info US30: Orson Cyan (@I2@) is alive and married.")
    
    
if __name__ == '__main__':
	unittest.main()



# ## US31 - user story test
# class us31_test(unittest.TestCase):
# 	@patch.object(sys, 'argv', ['US31.py','Homework.ged'])
# 	def test_living_singles(self):
# 		self.assertEqual(list_single(), 0)

# ## US30 user story test
# class test_us30(unittest.TestCase):
# 	@patch.object(sys, 'argv', ['US30.py', 'Homework.ged'])
# 	def test_list_married(self):
# 		self.assertEqual(list_married(), 0)

# if __name__ == '__main__':
# 	unittest.main(argv=[sys.argv[0]])
