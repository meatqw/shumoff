from static import get_content
from application.models import Product
from application import db


catalog_links = ['https://shumoff.biz/vibration_absorbing', 'https://shumoff.biz/soundproofing',
                 'https://shumoff.biz/sound_absorbent', 'https://shumoff.biz/zvukoizolyaciya',
                 'https://shumoff.biz/sealing_and_decorative', 'https://shumoff.biz/instruments', 'https://shumoff.biz/aksessuary']
result_catalog_data = []


def get_data_all_elements(url):
    """GET ALL PRODUCTS FROM PAGE"""
    content = get_content(url)

    if content:
        type_ = content.find(
            'ul', {'class': 'depho_breadcrumb'}).find_all('li')[-1].text

        # get product list
        list = content.find(
            "section", {'class': 'shop-cat-content-list'}).find('ul').find_all('li')
        for item in list:

            try:
                vendor = item.get('class')[0].replace('sw', '')  # vendor
            except Exception as e:
                vendor = item.find(
                    'section', {'class': 'product-descr'}).find('strong').text.strip()

            # PRODUCT INFO
            product_info = item.find("section", {'class': 'product-info'})
            title = product_info.find('h2', {'itemprop': 'name'}).text
            
            link = product_info.find(
                'h2', {'itemprop': 'name'}).find('a').get('href')
            
            desc = product_info.find("section", {'class': 'product-descr'}).find('div', {'itemprop': 'description'}).text
            
            attr = product_info.find("section", {'class': 'product-attr'}).text

            product_price = item.find("section", {'class': 'product-price'})

            # PRODUCT VARIATIONS: PRICE AND SIZE
            try:
                variants = product_price.find(
                    'div', {'class': 'product-variants-item'}).find_all('option')
                
            except Exception as e:
                variants = None
                price = product_price.find('span', {'itemprop': 'price'}).text
                size = None

                data = {'vendor': vendor, 'title': title, 'desc': desc, 'attr': attr,
                        'price': price, 'size': size, 'type': type_, 'link': link}

                result_catalog_data.append(data)

            # more product options
            if variants != None:
                for variant in variants:

                    price = variant.get('data-price')
                    size = variant.text

                    data = {'vendor': vendor, 'title': title, 'desc': desc, 'attr': attr,
                            'price': price, 'size': size, 'type': type_, 'link': link}

                    result_catalog_data.append(data)


def main():
    for link in catalog_links:
        print(link)
        get_data_all_elements(link)

    for data in result_catalog_data:

        # add data to base
        product = Product(
            vendor=data['vendor'],
            title=data['title'],
            desc=data['desc'],
            attr=data['attr'],
            price=data['price'],
            size=data['size'],
            type=data['type'],
            link=data['link'])

        db.session.add(product)
        db.session.commit()
        
main()

