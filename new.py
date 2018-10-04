# reviewed hasnain code
from flask import Flask,request,jsonify

app = Flask(__name__)

def inverse(f):
    def wrapper():
        data = request.json
        jsondic = {}
        op = data["op"]
        if op == "+":
            answer = data["op1"]-data["op2"]

        if op == "-":
            answer = data["op1"]+data["op2"]
        
        jsondic["res"] = answer

        return jsonify(jsondic)
    return wrapper
        
@app.route("/calc", methods=['POST'])
@inverse
def cal():
   data = request.json
   print(data)
   op = data["op"]
   op1 = data["op1"]
   op2 = data["op2"]

   reply = {}
   ans = None
   if op == "+":
     ans = op1+op2
   
   reply["result"] = ans
   return jsonify(reply)

if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)
