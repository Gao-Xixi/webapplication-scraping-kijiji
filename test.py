# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from bs4 import BeautifulSoup
import requests


def parse():
    req = requests.get("https://www.kijiji.ca/b-gta-greater-toronto-area/nike-shoes/k0l1700272)")
    bs = BeautifulSoup(req.text,'lxml')
    info_containers = bs.find_all('div', class_='info-container')
    for info_container in info_containers:
        price = info_container.find('div', class_='price').text.strip()
        title = info_container.find('div', class_='title').a.text.strip()
        try:
            location = info_container.find('div', class_='location').find('span', class_='').text.strip()
        except AttributeError:
            print("None")
        description = info_container.find('div', class_='description').text.strip()
        print(price)
        print(title)
        print(location)
        print(description)
    # def crawl(self):




if __name__ == '__main__':
    parse()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
