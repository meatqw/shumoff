from static import get_content
from application.models import Product
from application import db

def get_all_elements(url):
    """GET ALL PRODUCTS FROM PAGE"""
    content = get_content(url)
    if content:
        # get product list
        list = content.find("section", {'class': 'shop-cat-content-list'}).find('ul').find_all('li')
        for item in list:
            
            vendor = item.get('class')[0].replace('sw', '')  # vendor
            
            # PRODUCT INFO
            product_info = item.find("section", {'class': 'product-info'})
            title = product_info.find('h2', {'itemprop': 'name'}).text
            desc = product_info.find("section", {'class': 'product-descr'}).find('div', {'itemprop': 'description'}).text
            attr = product_info.find("section", {'class': 'product-attr'}).text
            
            product_price = item.find("section", {'class': 'product-price'})
            
            # PRODUCT VARIATIONS: PRICE AND SIZE
            variants = product_price.find('div', {'class': 'product-variants-item'}).find_all('option')
            for variant in variants:
                
                price = variant.get('data-price')
                size = variant.text
                
                data = {'vendor': vendor, 'title': title, 'desc': desc, 'attr': attr, 'price': price, 'size': size}
                print(data)
                product = Product(
                    vendor = data['vendor'],
                    title=data['title'],
                    desc=data['desc'],
                    attr=data['attr'],
                    price=data['price'],
                    size=data['size'])

                db.session.add(product)
                db.session.commit()
            
            

get_all_elements('https://shumoff.biz/vibration_absorbing')
        