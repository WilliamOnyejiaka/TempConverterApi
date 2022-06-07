from flask import request,Blueprint,jsonify
from src.modules.Pagination import Pagination
from src.modules.Serializer import Serializer
from src.config import MONGODB_URI
from pymongo import MongoClient
from src.modules.TempConverter import TempConverter
from bson.objectid import ObjectId
from typing import List,Dict
from datetime import datetime

crd = Blueprint('crd', __name__ , url_prefix="/api/crd")
client = MongoClient(MONGODB_URI)
db = client.tempconverter_db.db


@crd.post("/")
def convert():
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR',request.remote_addr)
    from_unit = request.get_json().get('from_unit',None)
    to_unit = request.get_json().get('to_unit',None)
    value = request.get_json().get('value',None)

    if not from_unit:
        return jsonify({'error':True,'message':"from_unit needed"}),400
    if not to_unit:
        return jsonify({'error': True, 'message': "to_unit needed"}), 400
    if value == None:
        return jsonify({'error': True, 'message': "value needed"}), 400
    

    try:
        value = float(value)
    except:
        return jsonify({'error':True,'message':"value must be a number"}),400
    
    result:float or None = TempConverter({'unit':from_unit,'value':value},to_unit).get_result()

    if not result:
        return jsonify({'error':True,'message':"invalid unit,units reqiured - fahrenheit, kelvin, celsius"}),400
    
    db_response = db.insert_one({
        'ip_address': ip_addr,
        'from_unit':from_unit,
        'to_unit':to_unit,
        'value':value,
        'result':result,
        'created_at':datetime.utcnow()
    })

    if db_response.inserted_id:
        return jsonify({'error': False, 'result': f"{result}"}), 200
    return jsonify({'error': True,'message': f"{ip_addr}"}),500

@crd.get("/")
def get_all():
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except:
        return jsonify({'error':True,'message':"page and limit must be numbers"}),400
    
    query = list(db.find({'ip_address': ip_addr}).sort('_id'))
    data = Serializer(['_id','ip_address','from_unit','to_unit','value','result','created_at']).dump(query)
    pagination_results:Dict = Pagination(data,page,limit).meta_data()

    return jsonify({'error': False, 'data': pagination_results}), 200


@crd.delete("/")
def clear():
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    query = list(db.find({'ip_address':ip_addr}))

    if query:
        result:List = Serializer(['_id']).dump(query)
        for index in range(len(result)):
            db.find_one_and_delete({'_id':ObjectId(result[index]['_id'])})
        return jsonify({'error':False,'message':"user data deleted successfully"}),200

    return jsonify({'error':False,'message':"nothing to delete"}),400
