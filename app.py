import pymysql
from flask import Flask, request, render_template
import scraping
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'bdc9862b5d7b08'
app.config['MYSQL_DATABASE_PASSWORD'] = '78b018d5'
app.config['MYSQL_DATABASE_DB'] = 'heroku_d021a21ad933d81'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-04.cleardb.com'
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=["GET"])
def scrape():
    item_name = request.args.get("item_name")
    page_num = int(request.args.get("page_num"))
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("USE heroku_d021a21ad933d81")
    # cursor.execute(f"SELECT * FROM information_schema.tables WHERE table_schema = 'heroku_d021a21ad933d81' AND table_name = '{item_name}'LIMIT 1;")


    try:
        cursor.execute(f'CREATE TABLE {item_name}(id BIGINT(7) NOT NULL AUTO_INCREMENT, '
                f'price VARCHAR (500), title VARCHAR(500), location VARCHAR(500),'
                f' posted VARCHAR(500), img VARCHAR(5000), PRIMARY KEY(id));')
    except pymysql.err.OperationalError:
        cursor.execute(f"DROP TABLE {item_name}")
        cursor.execute(f'CREATE TABLE {item_name}(id BIGINT(7) NOT NULL AUTO_INCREMENT, '
                       f'price VARCHAR (500), title VARCHAR(500), location VARCHAR(500),'
                       f' posted VARCHAR(500), img VARCHAR(5000), PRIMARY KEY(id));')
    for i in range(page_num):
        webpage = scraping.Webpage(item_name.replace(" ", "-"), i + 1)
        url = webpage.geturl()
        print(url)
        clawer = scraping.Clawer()

        products = clawer.parse(webpage)
        for product in products:
            title = product.title.replace("'","^")
            cursor.execute(
                (f"INSERT INTO {item_name} (price, title, location, posted, img) VALUES ('{product.price}','{title}', '{product.location}', '{product.posted}', '{product.img}');"))
            conn.commit()

    cursor.execute(f"SELECT * From {item_name};")
    rows = cursor.fetchall()
    cursor.execute(f"DROP TABLE {item_name}")
    cursor.close()
    conn.close()
    return render_template("product.html", rows=rows)

