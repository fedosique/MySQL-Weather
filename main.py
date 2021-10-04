import mysql.connector
import re, requests, sys
from bs4 import BeautifulSoup
from transliterator import transliteratе

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"}

db = mysql.connector.connect(host="localhost", user = "falexandrov", passwd = "xxx", database="dbdb")
mycursor = db.cursor()

print('\n')
id = input("Choose city by its number:        ")
print('\n')

mycursor.execute("SELECT city FROM cities WHERE id = %r;" %id)

for town in mycursor:
    town = re.sub("[(|'|)|,]", "", str(town))
    print(town)

town_lower = (transliteratе(town)).lower()                          #транслит текста и смена регистра
print(town_lower)

                                                                    # transliteration EXCEPTIONS
if town_lower == "velikiy_novgorod":
    town_lower = "novgorod"
elif town_lower == "rostov_na_donu":
    town_lower = "rostov-na-donu"


def pogoda():
    fullpage = requests.get("https://pogoda.mail.ru/prognoz/%s/24hours/" % town_lower, headers=headers)
    soup = BeautifulSoup(fullpage.content, 'html.parser')
    convert = soup.findAll("span", {"class": "p-forecast__temperature-value"})
    return (convert[0].text)


print("Погода сейчас:", pogoda())
