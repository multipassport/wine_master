from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import date
import collections
from dateutil.relativedelta import relativedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas


def get_template():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    return template


def get_winery_age():
    foundation_date = date(year=1920, month=1, day=1)
    current_date = date.today()
    time_delta = relativedelta(current_date, foundation_date)
    return time_delta


if __name__ == '__main__':
    excel_file = 'wine3.xlsx'
    excel_data_df = pandas.read_excel(excel_file, keep_default_na=False)
    table_headers = excel_data_df.columns.ravel()
    categories = excel_data_df[table_headers[0]].sort_values().unique().tolist()
    wines = excel_data_df.T.to_dict('dict')
    wine_stock = collections.defaultdict(list)

    for category in categories:
        for wine_index, wine_data in wines.items():
            if wine_data[table_headers[0]] == category:
                wine_stock[category].append(wine_data)

    rendered_page = get_template().render(
        winery_age=get_winery_age().years,
        wine_stock=wine_stock,
        categories=table_headers,
    )

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
