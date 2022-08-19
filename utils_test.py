import unittest
from unittest.case import TestCase
from py_utility import *


class TestTinUtility(unittest.TestCase):
    def test_get_file_name(self):
        path_test = "Corpus 5 Million/novel/novel.txt"
        cases = [
            # parameter : tail="",  without_extension=False,  set extension=None
            ["",False,None,"novel.txt"],#000
            ["",False,".csv","novel.csv"],#001
            ["",True,None,"novel"],#010
            ["",True,".csv","novel"],#011
            ["_test",False,None,"novel_test.txt"],#100
            ["_test",False,".csv","novel_test.csv"],#101
            ["_test",True,None,"novel_test"],#110
            ["_test",True,".csv","novel_test"],#111
        ]
        for i,case in enumerate(cases):
            file_name = get_file_name_without_extension(path_test,tail=case[0],without_extension=case[1],set_extension=case[2])
            try:
                self.assertEqual(case[3],file_name)
            except:
                print("case {} :{} != {}".format(i+1,case[3],file_name))

if __name__ == '__main__':
   unittest.main()