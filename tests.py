import unittest
from mail import sendMail,table_data
import os
from app import getValuesFromDB,connection_db
#Import de patch qui va servir à faire des mock 
from unittest.mock import patch, MagicMock
import psycopg2

class Test_file(unittest.TestCase):

    #Test que la fonction connection fonctionne
    def test_connection_to_db(self):
        self.assertTrue(connection_db())

    #Test que la fonction renvoie un tuple
    def test_get_value_from_db_is_tuple(self):
        self.assertEqual(type(getValuesFromDB(connection_db())),list)

    #Test que la fonction renvoi une string de validation
    # def test_sendMail(self):
    #     mail = "simplon.devcloud@gmail.com"
    #     my_msg = ((1,"a","bla","bli","bli"),(2,"b","blb","bli","bli"),(3,"c","blc","bli","bli"))
    #     self.assertEqual(type(sendMail(mail,my_msg)),str) 

    #Test que la fonction renvoi une string pour le tableau
    def test_table_data(self):
        my_msg = ((1,"a","bla","bli","bli"),(2,"b","blb","bli","bli"),(3,"c","blc","bli","bli"))
        #print(type(table_data(my_msg)))
        self.assertEqual(type(table_data(my_msg)),str) 
    
    #1er test mock => connection_db() fonctionne méthode in-line
    def test_connection_to_db_mock_success(self):
        with patch('app.psycopg2.connect') as mocked_response:
            #je passe en value de ma connection une string
            mocked_response.return_value = "test_connection_done"
            #appel de la fonction, je suis censé récuperer une string de connection
            cnx = connection_db()
            print("ma connexion",cnx)
            self.assertEqual(cnx, "test_connection_done")
    
    #2eme test mock => connection_db() fonctionne méthode in-line
    def test_connection_to_db_mock_failed(self):
        with patch('app.psycopg2.connect') as mocked_response:
            #je peux faire basculer ma fonctionvers le EXCEPT tu try/excep avec .side_effect
            mocked_response.side_effect = Exception
            #appel de la fonction
            cnx = connection_db()
            print("ma connexion",cnx)
            self.assertEqual(cnx, "failed to connect")

    #3eme test mock => getValuesFromDB() retourne une list avec MagickLock()
    def test_get_value_from_db_is_tuple_mock(self):
        #Je configure mon fetchall pour retourner une liste
        expected = ["test"]

        mock_connect = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = expected
        mock_connect.cursor.return_value = mock_cursor

        #Je met comme value a mon connect ce que j'ai paramétré, il va remplacer de lui même le vrai fetchall par le fake
        result = getValuesFromDB(mock_connect)
        print("result :",result)
        self.assertEqual(result, expected)
        self.assertEqual(type(result), list)

    #4eme test mock => sendMail() renvoie la string de connection
    def test_mail_sender_mock(self):
        #On va fake la partie sendmail() de smtplib
        with patch("smtplib.SMTP_SSL.sendmail", create=True) as sendmail:
            sendmail("hoolla", "jalla", "ohyeah")
            #print("test_using_context_manager:", sendmail.call_args_list)

            # Création des paramètres d'entrée de la fonction sendMail()
            receiver = 'les.mechants@simplon.co'
            message = ((1,"a","bla","bli","bli"),(2,"b","blb","bli","bli"),(3,"c","blc","bli","bli"))
            message_return = sendMail(receiver,message)
            #print(message_return)
            self.assertEqual(message_return, "success")

    #5eme test mock => sendMail() fail 
    def test_mail_sender_mock_fail(self):
        #On va fake la partie sendmail() de smtplib
        with patch("smtplib.SMTP_SSL.sendmail", create=True) as sendmail:
            sendmail.side_effect = EOFError
            #print("test_using_context_manager:", sendmail.call_args_list)

            # Création des paramètres d'entrée de la fonction sendMail()
            receiver = 'les.mechants@simplon.co'
            message = ((1,"a","bla","bli","bli"),(2,"b","blb","bli","bli"),(3,"c","blc","bli","bli"))
            message_return = sendMail(receiver,message)
            print("mon message de retour :", message_return)
            #je m'assure que mon message de retour n'est pas "success" qui a une longueur de 7 caractères
            self.assertLess(len(message_return),7)

if __name__ == '__main__':
    #Verbosity indique le nombre d'info que va retourner l'execution
    #de mes tests
    unittest.main(verbosity=2)