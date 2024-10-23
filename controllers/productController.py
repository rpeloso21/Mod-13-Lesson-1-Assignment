from flask import request, jsonify
from models.schemas.productSchema import product_schema, products_schema
from marshmallow import ValidationError
from services import productService
from caching import cache

def save():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    product_save = productService.save(product_data)
    if product_save is not None:
        return product_schema.jsonify(product_save), 201
    else:
        return jsonify({"message": "Fallback method error activated","body":product_data}), 400

@cache.cached(timeout=60)
def find_all():
    products = productService.find_all()
    return products_schema.jsonify(products), 200