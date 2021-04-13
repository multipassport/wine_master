import argparse
import collections
import pandas
import sys

from datetime import date
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape


def get_template():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
        )
    template = env.get_template('template.html')
    return template


def get_winery_age():
    foundation_year = 1920
    today = date.today()
    return today.year - foundation_year


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file_name',
        help='Имя и адрес файла с таблицей',
        )
    return parser


def get_wine_stock(wine_data):
    wine_stock = collections.defaultdict(list)
    for wine in wine_records_from_excel:
        wine_stock[wine['Категория']].append(wine)
    return wine_stock

if __name__ == '__main__':
    parser = create_parser()
    arguments = parser.parse_args()

    wine_records_from_excel = pandas.read_excel(arguments.file_name,
        keep_default_na=False).to_dict('records')
    table_headers = pandas.read_excel(arguments.file_name,
        keep_default_na=False).columns.ravel()
    categories_names = ['category', 'name', 'sort', 'price', 'image', 'discount']
    categories = dict(zip(categories_names, table_headers))

    rendered_page = get_template().render(
        winery_age=get_winery_age(),
        wine_stock=get_wine_stock(wine_records_from_excel),
        categories=categories,
        )

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
