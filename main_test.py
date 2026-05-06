((.venv) ) @BerraDamar ➜ /workspaces/elite102 (main) $ cat main_test.py
# ---- Write your tests below ----
import sys
import unittest

from main import success_message, transfer_message


class TestMyFunctions(unittest.TestCase):


    def test_success_message(self): 
        self.assertEqual(success_message("Berra", 100),"Account created successfully for Berra with balance 100.")
    def test_transfer_message(self):
        self.assertEqual(transfer_message("Berra", 100),"Transfer successful! 100 transferred from Berra.")
       
loader = unittest.TestLoader()
suite = loader.loadTestsFromTestCase(TestMyFunctions)
runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
runner.run(suite)((.venv) ) @BerraDamar ➜ /workspaces/elite102 (main) $ 
