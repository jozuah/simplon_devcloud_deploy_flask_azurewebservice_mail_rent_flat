import logging

import psycopg2

from flask import Flask, flash, redirect, render_template, request, session, abort

from flask import jsonify

from mail import sendMail
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

logging.basicConfig(filename='my_log.txt', level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

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
        logging.warning("[FLASK] Failed to connec to db, message error:  %s", (e))
        error_message= "failed to connect"
        print(error_message)
        return error_message

def getValuesFromDB(conn):
    try:       
        #conn = connection_db()
        #print("ma connection :", conn)
        #print("type :", type(conn))
        cursor = conn.cursor()
        cursor.execute("select * from paruvendu;")
        #mon_fetchall = cursor.fetchall()
        #myresult = read(mon_fetchall)
        myresult = cursor.fetchall()
        #for data in myresult:
        #    print(data)
        logging.info("[FLASK] Successfully fetch database data")
        #print(type(myresult)) 
        return myresult
    except Exception as e :
        logging.warning("[FLASK] Failed to get data from db, message error:  %s", (e))


@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/home', methods=['POST'])
def search_bar():
    try:
        mail_user = request.form.get('search_bar_item')
        print("my address :", mail_user)
        my_data = getValuesFromDB(connection_db())
        #my_msg = ((1,"a","bla"),(2,"b","blb"),(3,"c","blc"))
        check_mail = sendMail(mail_user,my_data)
        if check_mail == "success" :
            logging.info("[FLASK] search_bar function => Successfully send email") 
            return request_success()
        else:
            logging.info("[FLASK] search_bar function => Fail send email")
            return request_failed(check_mail)
        #return render_template("index.html")
    except Exception as e :
        logging.warning("[FLASK] message error:  %s", (e))

@app.route('/success')
def request_success():
    try:
        logging.info("[FLASK] request_success function => Successfully go to page /success") 
        return "Email has been successfully sent"
    except Exception as e :
        logging.warning("[FLASK] message error:  %s", (e))

@app.route('/fail')
def request_failed(my_error):
    try:
        msg_error = "Lors de l'envoi du mail cette erreur est apparue :" + my_error
        logging.info("[FLASK] request_failed function => Successfully go to page /fail") 
        return msg_error
    except Exception as e :
        logging.warning("[FLASK] message error:  %s", (e))

#Tests en local
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=3500, debug=True)

