from flask import Flask, request, jsonify

app = Flask(__name__)
_resources = [{"id":1,"name":"initial","type":"compute","size":"small"}]
_next_id = 2

@app.route("/api/login", methods=["POST"])
def login():
    d = request.get_json() or {}
    if d.get("username")=="user" and d.get("password")=="pass":
        return jsonify({"token":"fake-jwt"}),200
    return jsonify({"error":"invalid credentials"}),401

@app.route("/api/resources", methods=["GET"])
def list_resources():
    return jsonify(_resources),200

@app.route("/api/resources", methods=["POST"])
def create_resource():
    global _next_id
    d = request.get_json() or {}
    new = {"id":_next_id,"name":d.get("name",""),"type":d.get("type",""),"size":d.get("size","small")}
    _resources.append(new)
    _next_id+=1
    return jsonify(new),201

@app.route("/api/resources/<int:rid>/scale", methods=["POST"])
def scale(rid):
    d = request.get_json() or {}
    for r in _resources:
        if r["id"]==rid:
            r["size"] = d.get("size", r["size"])
            return jsonify(r),200
    return jsonify({"error":"not found"}),404

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
