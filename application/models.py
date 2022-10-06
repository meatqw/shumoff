from application import db
from datetime import datetime

# DB Model PRODUCT
# class Product(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     vendor = db.Column(db.String(200), nullable=True)
#     title = db.Column(db.String(200), nullable=True)
#     desc = db.Column(db.TEXT, nullable=True)
#     attr = db.Column(db.TEXT, nullable=True)
#     price = db.Column(db.Float(), nullable=True)
#     size = db.Column(db.String(400), nullable=True)
#     type = db.Column(db.String(400), nullable=True)
#     link = db.Column(db.String(400), nullable=True)
#     datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())

# DB Model BODY
# class Body(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(200), nullable=True)
#     effect_max = db.Column(db.JSON, nullable=True)
#     effect_great = db.Column(db.JSON, nullable=True)
#     effect_good = db.Column(db.JSON, nullable=True)
#     effect_practical = db.Column(db.JSON, nullable=True)
#     datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())
    
# # DB Model Auto
# class Auto(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     brand = db.Column(db.String(200), nullable=True)
#     model = db.Column(db.String(200), nullable=True)
#     body = db.Column(db.Integer(), db.ForeignKey('body.id'), nullable=True)
#     datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())
    
class Product(db.Model):
    post_title = db.Column(db.String(200), nullable=True) # Название товара
    post_name = db.Column(db.String(200), nullable=True) # Транслитированое название товара
    ID = db.Column(db.Integer(), primary_key=True)
    post_content = db.Column(db.TEXT, nullable=True) # Подробное описание
    post_status = db.Column(db.String(200), nullable=True) # всегда publish (Опубликовано)
    menu_order = db.Column(db.Integer(), nullable=True) # плевать что тут будет
    post_date = db.Column(db.String(200), nullable=True) # (2022-10-05 2:08:29) 
    post_parent = db.Column(db.String(200), nullable=True) # родитель (0)
    comment_status = db.Column(db.String(200), nullable=True) # всегда closed
    sku = db.Column(db.Integer(), nullable=True) # артикул товара
    downloadable  = db.Column(db.String(200), nullable=True) # всегда no
    virtual  = db.Column(db.String(200), nullable=True) # всегда no
    stock_status  = db.Column(db.String(200), nullable=True) # всегда instock
    backorders  = db.Column(db.String(200), nullable=True) # всегда no
    manage_stock  = db.Column(db.String(200), nullable=True) # всегда no
    regular_price = db.Column(db.Integer(), nullable=True) # цена товара
    tax_status  = db.Column(db.String(200), nullable=True) # всегда taxable
    featured  = db.Column(db.String(200), nullable=True) # всегда no

    tax_product_type = db.Column(db.String(200), nullable=True) # всегда variable
    tax_product_cat = db.Column(db.String(200), nullable=True) # Название категории товара
    attribute_pa_size = db.Column(db.String(400), nullable=True) # список типов упаковки, разделитель | например ( Коробка|лист 750 х 1000 мм|Лист 750 х 460 мм|Лист 750 х 500 мм|лист 750 х 560 мм|м² )
    attribute_data_pa_size = db.Column(db.String(200), nullable=True) # выбранные атрибуты, разделитель | например (0|1|1)

    
class Options(db.Model):
    Parent  = db.Column(db.String(200), nullable=True) # Название родительского товара
    parent_sku = db.Column(db.Integer(), nullable=True) # артикул родительского товара
    post_parent = db.Column(db.Integer(), nullable=True) # ID родительского товара
    ID = db.Column(db.Integer(), primary_key=True) # ID вариации
    post_status  = db.Column(db.String(200), nullable=True) #- всегда publish (Опубликовано)
    menu_order = db.Column(db.Integer(), nullable=True) # плевать что тут будет
    sku = db.Column(db.Integer(), nullable=True) # артикул вариации (если отличается от родительской)
    downloadable  = db.Column(db.String(200), nullable=True) # всегда no
    virtual  = db.Column(db.String(200), nullable=True) # всегда no
    stock_status  = db.Column(db.String(200), nullable=True) # всегда instock
    regular_price = db.Column(db.Integer(), nullable=True) # цена  вариации (если отличается от родительской)
    tax_class   = db.Column(db.String(200), nullable=True) # всегда parent
    meta_attribute_pa_size  = db.Column(db.String(200), nullable=True) # Транслитированое значение из поля attribute:pa_size родительского товара, с заменой пробелов на - и приведением всех букв в ловеркейс, например (лист 750 х 1000 мм  =>   list-750-h-1000-mm)
