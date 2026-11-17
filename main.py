import config
import requests
from bs4 import BeautifulSoup
import json

response = requests.get(config.URL,headers=config.HEADERS)

html = response.text



def get_data(html):

    soup = BeautifulSoup(html, "lxml").find("div", {"class": "a-list"}).find_all(
        "div", {"class": "a-list__item"}
    )


    unprocessed_data = []
    # Перебираем карточки по одной, card это одна карточка товара
    for card in soup:


        name = card.find("h5", {"class": "a-card__title"})
        price = card.find("span",{"class":"a-card__price"})
        description = card.find("p",{"class": "a-card__description"})
        city = card.find("span",{"class": "a-card__param"})


        fields = [ name , price, description,city]
        if not all(fields):
            continue
        unprocessed_data.append(
    {
        "name": name.get_text(strip=True),
        "price": price.get_text(strip=True),
        "description": description.get_text(strip=True),
        "city": city.get_text(strip=True),
    }
    )

    return unprocessed_data

def main():
    data = []
    unprocessed_data = get_data(html)
    data.extend(unprocessed_data)

    with open("item.json","w", encoding = "utf-8" ) as file:
        json.dump(data, file, indent=4,ensure_ascii = True)
main()
