from WebZulu.celery import app
from .common.layers import parse_layers


@app.task
def import_zulu_data():
    parse_layers()
