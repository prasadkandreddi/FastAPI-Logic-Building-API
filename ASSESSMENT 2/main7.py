
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional, List
 
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

#--------------------------------------------------------------------------------------------------#

#Query Filters in URL -----------> QUESTION 1
@app.get('/products/filters')
def filter_products(min_price : int = Query(None,description='Minimum Price'),
    max_price:int = Query(None,description="Maximum Price")):
    result = []
    for product in products:
        if(min_price is not None and product['price']<min_price):
            continue
        if(max_price is not None and product['price']>max_price):
            continue
        result.append(product)
    return {'Filtered Products':result,'Count of Filtered Products':len(result)}
    
#--------------------------------------------------------------------------------------------------#

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

#--------------------------------------------------------------------------------------------------#

# QUESTION 4
# Product Summary
@app.get('/products/summary')
def get_product_summary():
    cheapest = min(products, key=lambda p: p["price"]) 
    most_expensive = max(products, key=lambda p: p["price"]) 
    in_stock = 0
    total_products = len(products)
    list_category=[]
    for product in products:
        if(product['category'] not in list_category):
            list_category.append(product['category'])
        if(product['in_stock']==True):
            in_stock+=1
    return {'Total Products':total_products,'In stock count':in_stock,'Out of stock count':total_products-in_stock,'Most Expensive':{'name':most_expensive['name'],'price':most_expensive['price']},"Cheapest":{'name':cheapest['name'],'price':cheapest['price']},'Categories':list_category}

#--------------------------------------------------------------------------------------------------#

# ── Endpoint 3 — Return one product by its ID ──────────────────
@app.get('/products/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}

#--------------------------------------------------------------------------------------------------#

# Get name and price only from dynamic product id ---> QUESTION 2
@app.get('/products/{product_id}/price')
def get_name_price(product_id:int):
    for product in products:
        if(product['id']==product_id):
            return {'name':product['name'],'price':product['price']}
    return {'error': 'Product not found'}

#--------------------------------------------------------------------------------------------------#


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

#--------------------------------------------------------------------------------------------------#    

# QUESTION 3
# POST Customer_Feedback
class Customer_Feedback(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    product_id:   int = Field(..., gt=0)
    rating:       int = Field(..., ge=1, le=5)
    comment:      Optional[str]  = Field(None, max_length=300)

feedback = []

@app.post("/feedback")
def submit_feedback(data: Customer_Feedback):
    feedback.append(data.model_dump())
    return {
        "message": "Feedback submitted successfully",
        "feedback": data.model_dump(),
        "total_feedback": len(feedback),
    }

#--------------------------------------------------------------------------------------------------#

# QUESTIION 5
# POST Bulk Order and Order Item
class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity:   int = Field(..., gt=0, le=50)

class BulkOrder(BaseModel):
    company_name:  str= Field(..., min_length=2)
    contact_email: str= Field(..., min_length=5)
    items: List[OrderItem] = Field(..., min_items=1)

@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):
    confirmed, failed, grand_total = [], [], 0
    for item in order.items:
        product = next((p for p in products if p["id"] == item.product_id), None)
        if not product:
            failed.append({"product_id": item.product_id, "reason": "Product not found"})
        elif not product["in_stock"]:
            failed.append({"product_id": item.product_id, "reason": f"{product['name']} is out of stock"})
        else:
            subtotal = product["price"] * item.quantity
            grand_total += subtotal
            confirmed.append({"product": product["name"], "qty": item.quantity, "subtotal": subtotal})
    return {"company": order.company_name, "confirmed": confirmed,
            "failed": failed, "grand_total": grand_total}

#--------------------------------------------------------------------------------------------------#
#Bonus
orders = []

@app.post("/orders")
def create_order(order: dict):

    order_id = len(orders) + 1

    new_order = {
        "id": order_id,
        "items": order["items"],
        "status": "pending"
    }

    orders.append(new_order)

    return new_order


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["id"] == order_id:
            return {"order": order}
    return {"error": "Order not found"}


@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):
    for order in orders:
        if order["id"] == order_id:
            order["status"] = "confirmed"
            return {"message": "Order confirmed", "order": order}
    return {"error": "Order not found"}
