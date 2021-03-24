import unittest
from mail import sendMail,table_data
import os
from app import getValuesFromDB,connection_db

class Test_file(unittest.TestCase):

    #Test que la fonction connection fonctionne
    def test_connection_to_db(self):
        self.assertTrue(connection_db())

    #Test que la fonction renvoie un tuple
    def test_get_value_from_db_is_tuple(self):
        self.assertEqual(type(getValuesFromDB()),list)

    #Test que la fonction renvoi une string de validation
    def test_sendMail(self):
        mail = "simplon.devcloud@gmail.com"
        my_msg = ((1,"a","bla","bli","bli"),(2,"b","blb","bli","bli"),(3,"c","blc","bli","bli"))
        self.assertEqual(type(sendMail(mail,my_msg)),str) 

    #Test que la fonction renvoi une string pour le tableau
    def test_table_data(self):
        my_msg = ((1,"a","bla","bli","bli"),(2,"b","blb","bli","bli"),(3,"c","blc","bli","bli"))
        #print(type(table_data(my_msg)))
        self.assertEqual(type(table_data(my_msg)),str) 
    

if __name__ == '__main__':
    #Verbosity indique le nombre d'info que va retourner l'execution
    #de mes tests
    unittest.main(verbosity=2)