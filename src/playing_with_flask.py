from flask import Flask
app = Flask(__name__)

@app.route('/test')
def hello_world():
    return "hello world!"

@app.route('/json')
def return_json():
    

if __name__ == "__main__":
    app.run()