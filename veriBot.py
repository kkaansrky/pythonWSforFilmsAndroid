
from bs4 import BeautifulSoup
import requests
import time
import pyrebase
import json



config = {
  "apiKey": "apiKey",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "projectId.appspot.com",
}

firebase = pyrebase.initialize_app(config)


db = firebase.database()




filmSet=set()

r = requests.get('https://www.sinemalar.com/liste/278/olmeden-once-mutlaka-izlenmesi-gereken-100-film')
source = BeautifulSoup(r.content,"html.parser")





filmSet=source.find_all('article')

for item in filmSet:
    nameTurk=item.find("span",{"itemprop": "itemListElement"}).text
    if(item.find("small")!=None):
        nameEng=item.find("small").text
    else:
        nameEng="turkcesiyok"
    rank=item.find("div",{"class": "rank"}).text
    rating=item.find(id="rating").text
    imgLink=item.find("img")
    detail=item.find("p",{"style":"max-height:36px;overflow:hidden;"}).text
    
    data = {
    "name": nameTurk,
    "nameEng": nameEng,
    "listNumbers": rank,
    "rating":rating,
    "topRating": "10",
    "img": imgLink['src'],
    "detail": detail[16:]
    }
    print(data)
    json_object = json.dumps(data, indent = 7)

  
    
    db.child("films").child(rank).set(data)


