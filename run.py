import os
from os.path import join, dirname

from app import create_app


config_name = os.getenv('FLASK_CONFIG')
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0",port="81", debug=True)
