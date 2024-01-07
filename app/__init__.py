from flask import Flask
from app.routes import api

app = Flask(__name__)
app.register_blueprint(api)
