import unittest
import os
import datetime
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import tostring

import elanwriter as ew

class TestFunctions(unittest.TestCase):
    def get_test_directory(self):
        return os.path.dirname(os.path.abspath(__file__))

    def test_empty(self):

    	ed = ew.ElanDoc()
    	doc = str(tostring(ed._get_doc(), encoding='utf8', method='xml'))
    	
    	self.assertTrue("ANNOTATION_DOCUMENT" in doc)
    	self.assertTrue("MEDIA_DESCRIPTOR" in doc)
    	self.assertTrue("LINGUISTIC_TYPE" in doc)
    	self.assertTrue("LOCALE" in doc)
    	self.assertTrue("TIER" in doc)
    	self.assertTrue("TIME_ORDER" in doc)
    	self.assertTrue(datetime.datetime.now().strftime("%y-%m-%d") in doc)



if __name__ == '__main__':
    unittest.main()