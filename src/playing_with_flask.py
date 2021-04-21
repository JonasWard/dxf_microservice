from flask import Flask, json
app = Flask(__name__)

@app.route('/test')
def hello_world():
    return "hello world!"

@app.route('/json')
def return_json():
    data = ["hello world!","with a json!"]

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        # mimetype='application/json'
    )
    return response
    

if __name__ == "__main__":
    app.run()