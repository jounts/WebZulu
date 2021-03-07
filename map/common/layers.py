from xml.etree import ElementTree

import requests

from WebZulu.settings import GIS_SERVER


def get_layer_list():

    layer_list = []

    url = GIS_SERVER

    xml = '''<?xml version="1.0" encoding="UTF-8"?>
        <zulu-server service='zws' version='1.0.0'>
            <Command>
                <GetLayerList></GetLayerList>
            </Command>
        </zulu-server>'''.encode('utf-8')

    response = requests.post(url=url, data=xml)

    root = ElementTree.fromstring(response.text)

    for elements in root[0]:
        if elements.tag == 'Layer':
            for element in elements:
                if element.tag == 'Name':
                    layer_list.append(element.tag)

    return layer_list
