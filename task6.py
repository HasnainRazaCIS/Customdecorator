#Reviewejjjjjjjjjjjjjjhjjd

from flask import Flask,json
from flask import request,jsonify
from functools import wraps
from bson.json_util import dumps
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

mycol = mydb["operations"]
last = mydb["last_operations"]

app = Flask(__name__)

def inverse(f):
	@wraps(f)
	def wrapperfunc(*args,**kwargs):
		req_data=request.get_json()
		op=req_data["op"]
		if op=='+':
	    		request.json["op"]="-"
		elif op=='-':
			request.json["op"]="+"
		elif op=='*':
			request.json["op"]="/"
		elif op=='/':
			request.json["op"]=="*"
		return f(*args,**kwargs)

	return wrapperfunc


@app.route('/calc',methods=['POST'])

@inverse	

def calculator():
    req_data=request.json
    op1=req_data["op1"]
    op2=req_data["op2"]
    op=req_data["op"]
    if op=='+':
        res=op1+op2
    elif op=='-':
        res=op1-op2
    elif op=='*':
        res=op1*op2
    elif op=='/':
        if op2==0:
            error='undefined'
            return jsonify(error)
        else:
            res=op1/op2
    mydict = {"op1": op1, "op2": op2, "op":op, "Request":res}
    x = mycol.insert_one(mydict)

    calc = mycol.find()
    mylist = []
    for doc in calc:
        mylist.append(doc)

@app.route('/last',methods=['GET'])
def lastoperations():
    add = list ( mycol.find({"op": "+"},{"_id": 1, "op": 1, "op1": 1, "op2": 1, "result": 1}).sort('_id', -1).limit(4))
    sub = list ( mycol.find({"op": "-"},{"_id": 1, "op": 1, "op1": 1, "op2": 1, "result": 1}).sort('_id', -1).limit(4))
    mul = list ( mycol.find({"op": "*"},{"_id": 1, "op": 1, "op1": 1, "op2": 1, "result": 1}).sort('_id', -1).limit(4))
    div = list ( mycol.find({"op": "/"},{"_id": 1, "op": 1, "op1": 1, "op2": 1, "result": 1}).sort('_id', -1).limit(4))
    
    last.delete_many({})

    for x in add:
        last.insert_one(x)
    for x in sub:
        last.insert_one(x) 
    for x in mul:
        last.insert_one(x)
    for x in div:
        last.insert_one(x)
    
    l = []
    allops = last.find({})
    for d in allops:
        l.append(d)
    return dumps(l)

        #return jsonify(result=x.inserted_ids)
if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000)
