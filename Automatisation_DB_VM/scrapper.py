# import libraries
from bs4 import BeautifulSoup
#Permet de faire d'établir des connexions avec les pages web
from urllib.request import Request, urlopen
import urllib
import urllib.request as urlRequest

#necessaire au fonctionnement du beautifulsoup
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context

#Module de log
import logging

logging.basicConfig(filename='my_log.txt', level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def request_se_loger_website (my_url):
    try:
        try:
            # stockage de la page de top
            page = urllib.request.urlopen(my_url)
            logging.info("[SCRAPPING] Request has been successfully achieve from %s" , (my_url)) 
        except:
            logging.warning("[SCRAPPING] Cant't acces to %s", (my_url))  
            #return

        # parse the html using beautiful soup and store in variable 'soup'
        soup = BeautifulSoup(page, 'html.parser')

        #définition de mes variables de stockage
        carac = []
        lieu = []
        description = []
        price = []


        type_location = soup.findAll("div", class_= "ergov3-txtannonce")
        price_location = soup.findAll("div", class_= "ergov3-priceannonce")

        for items in range (len(type_location)):
            carac.append(type_location[items].find("span").text.replace("\t","").replace("\n","").replace("\r","").replace("Appartement","")) #caractéristiques
            lieu.append(type_location[items].find("cite").text.replace("\r","").replace("\n","")) #lieu
            description.append(type_location[items].find("p").text.replace("\r","").replace("\n","")) #descriptif
            price.append(price_location[items].text.replace("\t","").replace("\n","").replace("\r","")) #prix

        All_data = list(set(zip(carac, lieu, price, description)))
        
        logging.info("[SCRAPPING] Data has been successfully put in a dict from %s" , (my_url))    

        return All_data
        
    except:
        logging.warning("[SCRAPPING] Fail to put data in a dict from %s", (my_url))  


my_url = 'https://www.paruvendu.fr/immobilier/annonceimmofo/liste/listeAnnonces?nbp=0&tt=5&tbApp=1&tbDup=1&tbChb=1&tbLof=1&tbAtl=1&tbPla=1&at=1&nbp0=10&nbp1=20&sur0=20&px1=700&pa=FR&lol=5&ddlFiltres=nofilter&codeINSEE=92050,92040,92012,,'

#My_data=request_se_loger_website(my_url)


