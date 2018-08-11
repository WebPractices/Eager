from app import create_app
from app.config import flask_config

app = create_app(flask_config)
app.run(host='localhost', port=5000)
