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
        print("1")
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
        cursor.execute("select * from test;")
        myresult = cursor.fetchall()
        for x in myresult:
            print(x)
        logging.info("[FLASK] Successfully fetch database data") 
        return myresult
    except Exception as e :
        logging.warning("[FLASK] message error:  %s", (e))

@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/home', methods=['POST'])
def search_bar():
    mail_user = request.form.get('search_bar_item')
    print("my address :", mail_user)

    my_msg = ((1,"a","bla"),(2,"b","blb"),(3,"c","blc"))
    check_mail = sendMail(mail_user,my_msg)
    if check_mail == "success" :
        return request_success()
    else:
        return request_failed(check_mail)
    #return render_template("index.html")

@app.route('/success')
def request_success():
    return "Email has been successfully sent"

@app.route('/fail')
def request_failed(my_error):
    msg_error = "Lors de l'envoi du mail cette erreur est apparue :" + my_error
    return msg_error

