# Yiwen Wang

from US30_31_file import *
import sys
from unittest.mock import patch
from io import StringIO
# print(sys.argv)
file_name = sys.argv[1]
info = get_info(file_name)

def list_married():
    for fam in info['families']:	
        if fam['married'] != None:
            print(" Married people (husband, wife): " + str(fam['husband_name']) + str(fam['wife_name']))
    return 0



if __name__ == "__main__":
    list_married()