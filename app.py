import urllib.request
import os
from flask import Flask, send_file, render_template, redirect, url_for, request
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import zipfile
import asyncio
import psycopg2
from collections import namedtuple
import random
from bs4 import BeautifulSoup


Message = namedtuple('Message', 'url nesting_level')
messages = list()
screenshot_urls = list()
statuses = list()
sites = list()

con = psycopg2.connect(
  database="postgres",
  user="rolan",
  password="",
  host="127.0.0.1",
  port="5432"
)

app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
# print(os.environ['APP_SETTINGS'])


@app.route('/', methods=['GET'])
def start_page():
    return render_template('index.html')


@app.route('/add_message', methods=['POST'])
def add_message():
    messages.clear()
    url = request.form['url']
    """Вывод вложенных ссылок"""
    # nesting_level = request.form['nesting_level']
    # html = urllib.request.urlopen(url).read()
    # soup = BeautifulSoup(html)
    # for a in soup.find_all('a', href=True):
    #     if url not in a['href']:
    #         sites.append(a['href'])
    # print(sites)
    n = take_screenshot(url)
    path = os.getcwd()
    print("Текущая рабочая директория %s" % path)
    archive = f"{path+'/'}full_screenshot{n}.zip"
    newzip = zipfile.ZipFile(archive, 'w')  # создаём архив
    newzip.write(r'full_screenshot{}.png'.format(n))    # добавляем файл в архив
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO screenshot_web_service (status, screenshot_url) VALUES ('{take_status(archive)}', 'full_screenshot{n}.zip')"
    )
    con.commit()
    # cur = con.cursor()
    cur.execute(f"select id from screenshot_web_service where screenshot_url='full_screenshot{n}.zip';")
    [(task_id,)] = cur.fetchall()
    print(task_id)
    messages.append(task_id)
    return redirect(url_for('screenshot'))


def take_screenshot(url):
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.implicitly_wait(10)
    driver.get(url)
    S = lambda X: driver.execute_script("return document.body.parentNode.scroll" + X)
    driver.set_window_size(S('Width'), S('Height'))
    n = random.random()
    driver.find_element_by_tag_name('body').screenshot(f'full_screenshot{n}.png')
    print(n)
    return n


def take_status(path, ):
    if os.path.exists(path):
        return 'done'
    else:
        return 'canceled'


@app.route('/<name>')
def send_screenshot_zip(name):
    return send_file(f"{name}")


@app.route('/screenshot', methods=['GET'])
def screenshot():
    return render_template('screenshot.html', messages=messages)


@app.route('/check/<id>', methods=['GET'])
def check_id(id):
    statuses.clear()
    screenshot_urls.clear()
    cur = con.cursor()
    postgresql_select_query = f"select status, screenshot_url from screenshot_web_service where id={id};"
    cur.execute(postgresql_select_query)
    [(status, screenshot_url)] = cur.fetchall()
    print( status, screenshot_url)
    screenshot_urls.append(screenshot_url)
    statuses.append(status)
    return render_template('check_id.html', statuses=statuses, screenshot_urls=screenshot_urls)


if __name__ == '__main__':
    app.run()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(screenshot())
    loop.close()
    # print(os.environ['APP_SETTINGS'])