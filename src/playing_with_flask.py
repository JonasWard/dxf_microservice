from flask import Flask, jsonify, send_file
app = Flask(__name__)

@app.route('/test')
def hello_world():
    return "hello world!"

@app.route('/json')
def return_json():
    data = ["hello world!","with a json!"]
    return jsonify(data)

@app.route('/image')
def return_image():
    filename = "images/an_ugly_building.png"
    # filepath = "images/an_ugly_building.png"
    return send_file(filename) # , mimetype=filepath)

if __name__ == "__main__":
    app.run()