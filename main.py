from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from add_products import add
from database import SessionLocal, base, engine, get_db
from models import Brand, Category, Product

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def inr(value):
    return "₹" + format(value, ",.0f")


templates.env.filters["inr"] = inr
base.metadata.create_all(bind=engine)
db_new = SessionLocal()
add(db_new)
db_new.close()


def add_to_product(db, products):
    for p in products:
        p.category = db.get(Category, p.category_id)
        p.brand = db.get(Brand, p.brand_id)

        if p.stock_quantity > 0:
            p.in_stock = True
        else:
            p.in_stock = False
    return products


def add_to_category(db, categories):
    for c in categories:
        c.products = (
            db.query(Product)
            .filter(Product.category_id == c.id, Product.is_active == True)
            .all()
        )
    return categories


def add_to_brand(db, brands):
    for b in brands:
        b.products = (
            db.query(Product)
            .filter(Product.brand_id == b.id, Product.is_active == True)
            .all()
        )
    return brands


def get_number(text):
    if text is None or text == "":
        return None
    try:
        return float(text)
    except ValueError:
        return None


# for user search
def get_products(db, q, category_id, brand_id, min_price, max_price, sort):
    query = db.query(Product).filter(Product.is_active == True)
    if q:
        query = query.filter(Product.name.ilike("%" + q.strip() + "%"))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if brand_id:
        query = query.filter(Product.brand_id == brand_id)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if sort == "low_to_high":
        query = query.order_by(Product.price.asc())
    elif sort == "high_to_low":
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.id)
    products = query.all()
    return add_to_product(db, products)


def listing_page(request, db, title, action, category=None, q=None):
    params = request.query_params
    min_price = get_number(params.get("min_price"))
    max_price = get_number(params.get("max_price"))
    sort = params.get("sort", "")
    brand_id = None
    brand_text = params.get("brand_id", "")
    if brand_text.isdigit():
        brand_id = int(brand_text)
    category_id = None
    if category:
        category_id = category.id
    products = get_products(db, q, category_id, brand_id, min_price, max_price, sort)
    # remember the filters so the form can show them again
    f = {
        "min_price": min_price,
        "max_price": max_price,
        "sort": sort,
        "brand_id": brand_id,
    }
    context = {
        "title": title,
        "action": action,
        "products": products,
        "q": q,
        "category": category,
        "brands": db.query(Brand).all(),
        "f": f,
        "hide_filters": False,
    }
    return templates.TemplateResponse(request, "listing.html", context)


@app.get("/")
def home(req: Request, db: Session = Depends(get_db)):
    categories = add_to_category(db, db.query(Category).all())
    featured = (
        db.query(Product)
        .filter(Product.is_active == True)
        .order_by(Product.id)
        .limit(4)
        .all()
    )
    featured = add_to_product(db, featured)
    context = {"categories": categories, "featured": featured}
    return templates.TemplateResponse(req, "home.html", context)


@app.get("/products")
def products(request: Request, db: Session = Depends(get_db)):
    return listing_page(request, db, "All products", "/products")


@app.get("/categories/{category_id}")
def category_page(category_id: int, request: Request, db: Session = Depends(get_db)):
    cat = db.get(Category, category_id)
    if not cat:
        raise HTTPException(404, "Category not found")
    return listing_page(
        request, db, cat.name, "/categories/" + str(cat.id), category=cat
    )


@app.get("/products/{product_id}")
def product_detail(product_id: int, request: Request, db: Session = Depends(get_db)):
    prod = db.get(Product, product_id)
    if not prod or not prod.is_active:
        raise HTTPException(404, "Product not found")

    related = (
        db.query(Product)
        .filter(
            Product.category_id == prod.category_id,
            Product.id != prod.id,
            Product.is_active == True,
        )
        .limit(4)
        .all()
    )

    add_to_product(db, [prod])
    add_to_product(db, related)

    context = {"p": prod, "related": related}
    return templates.TemplateResponse(request, "details.html", context)


# Search: /search?q=dell
@app.get("/search")
def search(request: Request, q: str = "", db: Session = Depends(get_db)):
    if q:
        title = f"Results for '{q}' "
    else:
        title = "Search"
    return listing_page(request, db, title, "/search", q=q)


@app.get("/categories")
def categories(request: Request, db: Session = Depends(get_db)):
    all_categories = add_to_category(db, db.query(Category).all())
    return templates.TemplateResponse(
        request, "categories.html", {"categories": all_categories}
    )


@app.get("/brands")
def brands(request: Request, db: Session = Depends(get_db)):
    all_brands = add_to_brand(db, db.query(Brand).all())
    return templates.TemplateResponse(request, "brands.html", {"brands": all_brands})


# About: /about
@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse(request, "about.html", {})


# 404 page
@app.exception_handler(404)
def not_found(request: Request, exc):
    context = {
        "title": "Page not found",
        "action": "/products",
        "products": [],
        "q": None,
        "category": None,
        "brands": [],
        "f": {},
        "hide_filters": True,
    }
    return templates.TemplateResponse(request, "listing.html", context, status_code=404)
