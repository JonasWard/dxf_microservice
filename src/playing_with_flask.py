from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/test')
def hello_world():
    return "hello world!"

@app.route('/json')
def return_json():
    data = ["hello world!","with a json!"]
    return jsonify(data)
    

if __name__ == "__main__":
    app.run()