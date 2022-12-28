from bitrix24 import *
from bs4 import BeautifulSoup
import re
import requests

bx24 = Bitrix24('https://b24-7387tw.bitrix24.ru/rest/1/c2kvs60rg1nnex2k/')


def parse_data(url) -> bool:
    headers = {
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.5.1034 Yowser/2.5 Safari/537.36'

    }

    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, 'lxml')
    all_product = soup.find('div', class_='items-items-kAJAg')
    category = soup.find('a', class_="rubricator-list-item-link-uPiO2 rubricator-list-item-link_current-fnAHj").get(
        'title')

    data = dict()

    for item in all_product:
        item_href = 'https://www.avito.ru' + item.find('div', class_="iva-item-titleStep-pdebR").find('a').get('href')
        item_title = item.find('div', class_="iva-item-titleStep-pdebR").find('a').get('title')
        item_description = item.find('div',
                                     class_="iva-item-text-Ge6dR iva-item-description-FDgK4 text-text-LurtD text-size-s-BxGpL").get_text(
            strip=True)

        item_price = item.find('span', class_="price-text-_YGDY text-text-LurtD text-size-s-BxGpL").get_text(
            strip=True).rstrip('₽')

        if item_price == 'Цена не указана':
            item_price = str(0)
        new_item_price = re.sub('\xa0', '', item_price)

        desciption_and_href = f"Ссылка на объявление: {item_href} \nОписание: {item_description}"

        data["TITLE"] = item_title
        data["UTM_CONTENT"] = desciption_and_href
        data["OPPORTUNITY"] = new_item_price
        data["SOURCE_DESCIPTION"] = category
        saveDeal(data)


def saveDeal(item: dict) -> bool:
    try:
        bx24.callMethod("crm.deal.add",
                        fields=item
                        )
    except Exception as e:
        print(e)
    return True
