import curses.ascii
from bs4 import BeautifulSoup
import requests
# why make this searching engine?
# some not relative items shown, not good efficient
#

#store data in mysql



# def store(conn,table_name, price, title, location, posted, img):
#     title = title.replace("'", "\'")
#
#     conn.cursor.execute(
#         (f"INSERT INTO {table_name} (price, title, location, posted, img) VALUES ('{price}','{title}', '{location}', '{posted}', '{img}');"))
#     conn.commit()

# Object storing product's information
class Product:
    def __init__(self, price, title, location, posted, img):
        self.price = price
        self.title = title
        self.location = location
        self.posted = posted
        self.img = img
        # self.description = description
    def print(self):
        print(f'Title: {self.title}')
        print(f'Price: {self.price}')
        print(f'Location: {self.location}')
        print(f'Posted time: {self.posted}')
        print(f'Img: {self.img}')
        # print(f'Description: {self.description}')
# object store webpage's information
class Webpage:
    def __init__(self,name,page):
        self.name = name
        self.page = page
        self.url = f"https://www.kijiji.ca/b-gta-greater-toronto-area/{self.name}/page-{self.page}/k0l1700272"
    def geturl(self):
        return self.url
    def getname(self):
        return self.name
# scraping data
class Clawer:
    def getpage(self, webpage):
        url = webpage.geturl()
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'lxml')
    def getimg(self,webpage):
        bs = self.getpage(webpage)
        if bs is not None:
            picture_containers = bs.find_all('div', class_='image')
            imgs = []
            for picture_container in picture_containers:
                try:
                    img_src = picture_container.picture.img['data-src']
                    imgs.append(img_src)
                except AttributeError:
                    imgs.append("NO IMG")
        return imgs
    def parse(self, webpage):
        bs = self.getpage(webpage)
        imgs = self.getimg(webpage)
        if bs is not None:
            products = []
            i = 0
            info_containers = bs.find_all('div', class_='info-container')
            for info_container in info_containers:
                title = info_container.find('div', class_='title').a.text.strip()
                name = webpage.getname().lower().replace("-", " ")
                img = imgs[i]
                if name in title.lower():
                    try:
                        price = info_container.find('div', class_='price').text.strip().replace('$', '')
                    except AttributeError:
                        price = 'no price'
                    # try:
                    #     description = info_container.find('div', class_='description').text.strip()
                    # except AttributeError:
                    #     description = "no description"
                    try:
                        posted = info_container.find('div', class_='location').find('span',class_='date-posted').text.strip()
                    except AttributeError:
                        posted = "unknown date"
                    try:
                        location = info_container.find('div', class_='location').find('span', class_='').text.strip()
                    except AttributeError:
                        location = "unknown location"


                    product = Product(price, title, location, posted, img)
                    product.print()
                    products.append(product)
                    i = i + 1
                else:
                    i = i + 1
                    continue
        return products

    # def createtable(self, webpage):
    #     sql = Msql()
    #     table_name = webpage.getname().lower().replace("-", "")
    #     sql.table(table_name)

        # sql.cur.close()
        # sql.conn.close()


# if __name__ == '__main__':
#     name = input("Enter the name of the item you want to scrape: ")
#     num = int(input("Enter the num of pages you want to scrape: "))
#     sql = Msql()
#     table_name = name.replace(" ", "")
#     sql.table(table_name)
#     for i in range(num):
#         webpage = Webpage(name.replace(" ", "-"),i+1)
#         url = webpage.geturl()
#         clawer = Clawer()
#         print(url)
#         clawer.parse(webpage, sql)
#     sql.cur.execute(f"SELECT * From {table_name};")
#     rows = sql.cur.fetchall()
#     for row in rows:
#         print(row[5])
#
#
#     sql.cur.close()
#     sql.conn.close()
