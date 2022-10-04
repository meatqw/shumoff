from itertools import product
import requests
from bs4 import BeautifulSoup
from static import get_content
from application.models import Product, Body, Auto
from application import db

headers = {"accept": "*/*",
           "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
           'referer': 'https://shumoff.biz/calc?mode=body&body_id=1',
           'origin': 'https://shumoff.biz'}


def get_model(url, brand_id):
    """Get auto list"""
    try:
        request = requests.post(url, headers=headers, data={
                                'brand_id': brand_id, 'selected': ''})
        # redirect check
        if request.status_code == 200:
            content = BeautifulSoup(request.content, 'html.parser')
            return content
        else:
            print(request.status_code)
            return False

    except Exception as e:
        print(e)
        return False
    
    
def get_auto():
    """Get model and brand"""
    content = get_content('https://shumoff.biz/calc')
    
    if content:
        # all brands
        brand_list = content.find('select', {'name': 'brand_id'}).find_all('option')
        
        for i in brand_list[1:]:
            id_ = i.get('value')
            brand = i.text.strip()
            
            # get models
            model_content = get_model('https://shumoff.biz/ajax/getCarModels', id_)
            if model_content:
                models = model_content.find_all('option')
                for model in models:
                    body = model.text.split(' ')[-1].strip()
                    model_name = model.text.split(body)[0].strip()
                    
                    # find id by name
                    body_id = Body.query.filter_by(name=body).first()
                    
                    if body_id:
                        # add data to base
                        auto = Auto(
                            brand=brand,
                            model=model_name,
                            body=body_id.id)

                        db.session.add(auto)
                        db.session.commit()
                        print(brand, model, body_id)
                    else:
                        
                        print('pass', body)
                    
            
def get_calc_data(url):
    """GET CALC DATA"""

    content = get_content(url)

    result_data = {}

    if content:

        # effect tables
        table_max = {'table': content.find(
            'section', {'class': 'w1280 tab1 tab-content'}), 'name': 'max'}
        table_great = {'table': content.find(
            'section', {'class': 'w1280 tab2 tab-content'}), 'name': 'great'}
        table_good = {'table': content.find(
            'section', {'class': 'w1280 tab3 tab-content tab4-marg'}), 'name': 'good'}
        table_practical = {'table': content.find(
            'section', {'class': 'w1280 tab4 tab-content tab4-marg'}), 'name': 'pactical'}

        for i in [table_max, table_great, table_good, table_practical]:

            data = {}
            ul = i['table'].find('ul').find_all('li')
            for li in ul[1:]:

                # set
                set_name = li.find('div', {'class': 'name-komplekt'}).text
                item_list = li.find(
                    'div', {'class': 'matlist group-item'}).find_all('div', {'class': 'str-item'})

                # Products
                for item in item_list:
                    item_title = item.find(
                        'div', {'class': 'matlist-b group-item-name'}).find('a').text
                    item_link = item.find(
                        'div', {'class': 'matlist-b group-item-name'}).find('a').get('href')
                    item_value = item.find(
                        'input', {'class': 'group-item-quantity'}).get('value')
                    item_price = item.find(
                        'select', {'class': 'group-item-prop'}).find('option').get('data-price')
                    item_size = item.find(
                        'select', {'class': 'group-item-prop'}).find('option').text
                    item_weight = item.find(
                        'select', {'class': 'group-item-prop'}).find('option').get('data-mass')

                    # get the data from Product table
                    product = Product.query.filter_by(link=item_link).first()
                    
                    if product.vendor not in data:
                        data[product.vendor] = {'link': item_link, 'price': float(item_price), 'weight': float(item_weight), 'value': float(item_value),
                                            'size': item_size, 'total_price': float(item_price) * float(item_value), 'title': item_title, 'total_weight': float(item_weight)}
                    else:
                        data[product.vendor]['total_weight'] += round(float(item_weight), 3)
                        data[product.vendor]['value'] += float(item_value)
                        data[product.vendor]['total_price'] = data[product.vendor]['price'] * data[product.vendor]['value']

            # calculate total_price and total_weight
            total_price = 0
            total_weight = 0
            for k, v in data.items():
               total_price += v['total_price']
               total_weight += v['total_weight']
               
               
            result_data[i['name']] = data
            result_data[i['name']]['total_price'] = total_price
            result_data[i['name']]['total_weight'] = round(total_weight, 3)
        
    return result_data

body_links = [{'link': 'https://shumoff.biz/calc?mode=body&body_id=1', 'name': 'Хэтчбек'},
              {'link': 'https://shumoff.biz/calc?mode=body&body_id=11', 'name': 'Купе'},
              {'link': 'https://shumoff.biz/calc?mode=body&body_id=2', 'name': 'Седан'},
              {'link': 'https://shumoff.biz/calc?mode=body&body_id=3', 'name': 'Универсал'},
              {'link': 'https://shumoff.biz/calc?mode=body&body_id=4', 'name': 'Кроссовер'},
              {'link': 'https://shumoff.biz/calc?mode=body&body_id=5', 'name': 'Джип'},
              {'link': 'https://shumoff.biz/calc?mode=body&body_id=6', 'name': 'Пикап'},
              {'link': 'https://shumoff.biz/calc?mode=body&body_id=10', 'name': 'Микроавтобус'}
              ]

def calc():
    for link in body_links:
        
        result = get_calc_data(link['link'])
        
        # add data to base
        body = Body(
            name=link['name'],
            effect_max=result['max'],
            effect_great=result['max'],
            effect_good=result['max'],
            effect_practical=result['max'])

        db.session.add(body)
        db.session.commit()
        
        print(link['name'])
        

get_auto()
    


