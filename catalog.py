from itertools import product
from static import get_content
from application.models import Product, Options
from application import db
from transliterate import translit
from datetime import datetime


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
                
                
            product_arr = []
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

                product_arr.append(data)

            # more product options
            if variants != None:
                for variant in variants:

                    price = variant.get('data-price')
                    size = variant.text

                    data = {'vendor': vendor, 'title': title, 'desc': desc, 'attr': attr,
                            'price': price, 'size': size, 'type': type_, 'link': link}

                    product_arr.append(data)
            
            result_catalog_data.append(product_arr)


def main():
    for link in catalog_links:
        print(link)
        get_data_all_elements(link)

    for data in result_catalog_data:
        
        vendor = data[0]['vendor']
        title = data[0]['title']
        title_transliteration =  translit(data[0]['title'], language_code='ru', reversed=True)
        desc = data[0]['desc']
        attr = data[0]['attr']
        price = data[0]['price']
        size = data[0]['size']
        type_ = data[0]['type']
        link = data[0]['link']
        date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        
        all_size = ''
        
        for i in data:
            if size != None:
                all_size += i['size']+'|'
                
            
        all_size = all_size[:-1]
        
        # add data to base
        product = Product(
            post_title = title,
            post_name = title_transliteration,
            # ID = 
            post_content = desc,
            post_status = 'publish',
            menu_order = 0,
            post_date = date,
            post_parent = 0,
            comment_status = 'closed',
            sku = int(vendor),
            downloadable  = 'no',
            virtual  = 'no',
            stock_status  = 'instock',
            backorders  = 'no',
            manage_stock  = 'no',
            regular_price = price,
            tax_status  = 'taxable',
            featured  = 'no',

            tax_product_type = 'variable',
            tax_product_cat = type_,
            attribute_pa_size = all_size,
            attribute_data_pa_size = '')
        
        db.session.add(product)
        db.session.commit()
        
        product_id = product.ID
        
        
        for i in data:
            if size != None:
                size = translit(i['size'].strip().replace(' ', '-'), language_code='ru', reversed=True)
        
                # add data to base
                options = Options(
                    Parent  = title,
                    parent_sku = vendor,
                    post_parent = product_id,
                    post_status  = 'publish',
                    menu_order = 0,
                    downloadable  = 'no',
                    virtual  = 'no',
                    stock_status  = 'instock',
                    regular_price = int(i['price']),
                    tax_class   = 'parent',
                    meta_attribute_pa_size  = size)

                db.session.add(options)
                db.session.commit()
                
        print(all_size, date, title_transliteration)
main()

