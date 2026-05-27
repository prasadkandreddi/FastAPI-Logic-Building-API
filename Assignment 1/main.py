from fastapi import FastAPI
 
app = FastAPI()
 
# ── Temporary data — acting as our database for now ──────────
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook',       'price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub',         'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set',          'price':  49, 'category': 'Stationery',  'in_stock': True },
    {'id': 5, 'name': 'Laptop Stand','price':200,'category':'Electronics','in_stock': False},
    {'id': 6, 'name': 'Mechanical Keyboard','price':800,'category':'Electronics','in_stock':True},
    {'id': 7, 'name': 'Webcam','price':1500,'category':'Electronics','in_stock':True},
]
 
# ── Endpoint 0 — Home ────────────────────────────────────────
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}
 
# ── Endpoint 1 — Return all products ──────────────────────────
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}


# EndPoint 2 - Return instock products
@app.get("/products/instocks")
def products_instock():
    list_instock=[]
    for product in products:
        if(product['in_stock']==True):
            list_instock.append(product)
    return {"In stock Products":list_instock,"Total Instock":len(list_instock)}


# EndPoint 3 - Cheapest & Most Expensive Product
@app.get("/products/deals")
def get_deals():
    cheapest = min(products, key=lambda p: p["price"]) 
    expensive = max(products, key=lambda p: p["price"]) 
    return { "best_deal": cheapest, "premium_pick": expensive, }



# ── Endpoint 3 — Return one product by its ID ──────────────────
@app.get('/products/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}

# EndPoint 4 - Return category of products
@app.get('/products/category/{category}')
def get_product_category(category: str):
    list_category=[]
    for product in products:
        if(product['category']==category):
            list_category.append(product)
    if(len(list_category)!=0):
        return {"List Category": list_category,"Total Product of this category:":len(list_category)}
    else:
        return {"Error":"Product of that Category not there"}
    
# Endpoint 5 - Get Store Summary
@app.get("/store/summary")
def get_store_summary():
    total_products = len(products)
    in_stock_count = 0
    out_stock_count = 0
    category_list = []
    for product in products:
        if(product['in_stock']==True):
            in_stock_count+=1
        else:
            out_stock_count+=1

        if(product['category'] not in category_list):
            category_list.append(product['category'])
    return { "Store Name": "My E-commerce Store", "Total products": total_products, "in_stock": in_stock_count, "out_of_stock": out_stock_count, "categories": category_list }

# Endpoint 6 - Search Product by name
@app.get("/products/search/{keyword}")
def get_search_products(keyword: str):
    list_products=[]
    for product in products:
        if(keyword.lower() in product['name'].lower()):
            list_products.append(product)
    if(len(list_products)!=0):
        return {"Keyword":keyword,"List Category of Search":list_products,"Total Matches":len(list_products)}
    else:
        return {"Message":"No products matched in search"}