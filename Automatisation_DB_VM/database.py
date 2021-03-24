from scrapper import request_se_loger_website

import logging

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename='my_log.txt', encoding='utf-8', level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def reset_logfile(logfile_path):
    ### Reset du fichier log
    my_txt_file= open(logfile_path, "r+")    
    # to erase all data  
    my_txt_file.truncate() 
    # to close file
    my_txt_file.close() 

reset_logfile("my_log.txt")

class Database_location():

    def __init__(self):
        self.url_paruvendu = 'https://www.paruvendu.fr/immobilier/annonceimmofo/liste/listeAnnonces?nbp=0&tt=5&tbApp=1&tbDup=1&tbChb=1&tbLof=1&tbAtl=1&tbPla=1&at=1&nbp0=10&nbp1=20&sur0=20&px1=700&pa=FR&lol=5&ddlFiltres=nofilter&codeINSEE=92050,92040,92012,,'

        self.data_from_paruvendu = request_se_loger_website(self.url_paruvendu)
        self.conn = self.connect()
        self.set_data_into_table()

    def connect(self):
        try:
            #J'utilise l'ip public Azure pour me connecter à ma VM et aller sur le PG dessus
            cnx = psycopg2.connect(host= os.getenv('PG_HOST'),
                            user= os.getenv('PG_USER'),
                            database= os.getenv('PG_DATABASE'),
                            password= os.getenv('PG_PASSWORD'))
                                            
            print("Connected to database ")
            logging.info("[DATABASE] Successfully connected to your database") 
            return cnx
        except Exception as e:
            logging.warning("[DATABASE] message error:  %s", (e))
        return cnx

    def create_table(self):
       
        sql_query = self.conn.cursor()
        sql_query.execute("CREATE TABLE IF NOT EXISTS PARUVENDU (id SERIAL PRIMARY KEY NOT NULL, caracteristiques VARCHAR(100) NOT NULL, localisation VARCHAR(100) NOT NULL,loyer VARCHAR(100) NOT NULL, description VARCHAR(500) NOT NULL)")
        self.conn.commit()

    def set_data_into_table(self):

        sql_query = self.conn.cursor()
        insert = "INSERT INTO paruvendu (caracteristiques, localisation, loyer, description) VALUES (%s, %s, %s, %s);"
        value = self.data_from_paruvendu
        sql_query.executemany(insert, value)
        self.conn.commit()



def connection_db ():
    try:
        #J'utilise l'ip public Azure pour me connecter à ma VM et aller sur le PG dessus
        cnx = psycopg2.connect(host= os.getenv('PG_HOST'),
                            user= os.getenv('PG_USER'),
                            database= os.getenv('PG_DATABASE'),
                            password= os.getenv('PG_PASSWORD'))
                                        
        print("Connected to database ")
        logging.info("[FLASK] Successfully connected to your database") 
        return cnx
    except Exception as e:
        logging.warning("[FLASK] message error:  %s", (e))
    return cnx

def getValuesFromDB():
    try:       
        conn = connection_db()
        cursor = conn.cursor()
        logging.info("[FLASK] Successfully connect to db")
        cursor.execute("select * from paruvendu;")
        myresult = cursor.fetchall()
        #for data in myresult:
        #    print(data)
        logging.info("[FLASK] Successfully fetch database data") 
        return myresult
    except Exception as e :
        logging.warning("[FLASK] message error:  %s", (e))

#db = Database_location()
getValuesFromDB()