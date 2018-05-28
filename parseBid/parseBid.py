import requests
from bs4 import BeautifulSoup

def parseBid(url:str):
        page = requests.get(url)
        soup = BeautifulSoup(page.text,'html.parser')
        price = int(soup.find(attrs = {"class":'exratetip','id':'asking'}).contents[0].replace(',',''))
        name = soup.find(attrs = {'class':'lot-name'}).contents[0]
        return (name,price)
        
