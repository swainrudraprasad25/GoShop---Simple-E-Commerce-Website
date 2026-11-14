from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Text

from database import base

# CATEGORY TABLE: Electronics, Fashion, Footwear, ...


class Category(base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, default="")
    image = Column(String(100))


# BRAND TABLE: Dell, JBL, Noise, ...
class Brand(base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, default="")
    logo = Column(String(100))


# PRODUCT TABLE: each item in the shop
class Product(base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, default="")
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    image = Column(String(120))
    is_active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    brand_id = Column(Integer, ForeignKey("brands.id"))
