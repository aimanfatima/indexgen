from flask import Flask
import logging
import sys
from app.routes import api

app = Flask(__name__)
app.register_blueprint(api)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
