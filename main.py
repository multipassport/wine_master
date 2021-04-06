from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import date
import pprint
import collections
from dateutil.relativedelta import relativedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas

pp = pprint.PrettyPrinter(indent=4)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

foundation_date = date(year=1920, month=1, day=1)
current_date = date.today()
delta = relativedelta(current_date, foundation_date)

excel_file = 'wine2.xlsx'
excel_data_df = pandas.read_excel(excel_file)
table_headers = excel_data_df.columns.ravel()
categories = excel_data_df[table_headers[0]].unique().tolist()
wines = excel_data_df.T.to_dict('dict')
wine_stock = collections.defaultdict(list)


for category in categories:    
    for wine_index, wine_data in wines.items():        
        if wine_data[table_headers[0]] == category:            
            wine_stock[category].append(wine_data)

rendered_page = template.render(
    winery_age = delta.years,
    wine_stock = wine_stock,
)

with open('index.html', 'w', encoding='utf-8') as file:
    file.write(rendered_page)   


server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
