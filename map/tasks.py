from WebZulu.celery import app
from .common.layers import write_layers


@app.task
def import_zulu_data_task():
    write_layers()
