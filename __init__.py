import os

from flask import Flask


def create_app():

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # register blueprints
    from api import import_blueprint
    from api import export_blueprint
    app.register_blueprint(import_blueprint)
    app.register_blueprint(export_blueprint)

    return app


if __name__ == "__main__":
    print("I started a server")
    app = create_app()

    @app.route('/')
    def hello_world():
        return """<html>
   <body>
      <form action = "http://localhost:5000/data/import" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>   
   </body>
</html>"""

    app.run()