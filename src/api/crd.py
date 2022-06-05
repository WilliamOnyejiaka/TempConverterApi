from flask import request,Blueprint,jsonify
from src.config import MONGODB_URI
from pymongo import MongoClient

crd = Blueprint('crd', __name__ , url_prefix="/api/crd")

client = MongoClient(MONGODB_URI)
db = client.tempconverter_db.db


@crd.post("/")
def convert():
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR',request.remote_addr)
    db.insert_one({'name': 'just a test'})
    return jsonify({'error': False,'message': f"{ip_addr}"}),200