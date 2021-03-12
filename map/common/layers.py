"""
Module retrieving published projects and layers on zulu server
"""

from xml.etree import ElementTree

import requests

from WebZulu.settings import GIS_SERVER
from map.common.zulu_auth import get_credentials


def get_layers() -> dict:
    """
    collect data to dict from zulu server
    :return: dict
    """
    return parse_data(get_source_data())


def get_source_data() -> str:
    """
    request GetLayerList from zulu server
    :return: str
    """

    xml = '''<?xml version="1.0" encoding="UTF-8"?>
        <zulu-server service='zws' version='1.0.0'>
            <Command>
                <GetLayerList></GetLayerList>
            </Command>
        </zulu-server>'''.encode('utf-8')

    response = requests.post(url=GIS_SERVER, data=xml)

    return response.text


def parse_data(data: str) -> dict:
    """
    parse source data from zulu server
    :param data: str
    :return: dict
    """
    parsed_data = dict()

    root = ElementTree.fromstring(data)

    for element in root[0]:
        if element.tag == 'Layer' and len(element):
            project = element[0].text[:element[0].text.find(':')]
            if project not in parsed_data.keys():
                parsed_data[project] = []
            parsed_data[project].append(
                {'fullname': element[0].text,
                 'name': element[0].text[element[0].text.find(':') + 1:],
                 'title': element[1].text}
            )

    return parsed_data


def get_source_bounds(full_layer_name: str) -> str:
    """
    Requests GetLayerBounds from zulu server
    :param full_layer_name: str
    :return: str
    """
    xml = f"""<zulu-server service="zws" version="1.0.0">
<Command>
<GetLayerBounds>
<Layer>{full_layer_name}</Layer>
</GetLayerBounds>
</Command>
</zulu-server>""".encode('utf-8')

    headers = {'Authorization': 'Basic ' + get_credentials()}

    response = requests.post(url=GIS_SERVER, headers=headers, data=xml)

    return response.text


def parse_bounds(source_data: str) -> dict:
    """
    Parsing layer bounds from xml string
    :param source_data: str
    :return: dict
    """
    parsed_bounds = dict()

    root = ElementTree.fromstring(source_data)

    for element in list(root[0][0]):
        if element.attrib['CRS'] == 'EPSG:4326':
            return element.attrib


def get_centre_map(layer_list: list) -> tuple:
    """

    :param layer_list: list
    :return: tuple (lon, lat)
    """
    lat_list = []
    lon_list = []

    for layer in layer_list:
        bounds = parse_bounds(get_source_bounds(layer))

        if bounds is not None:
            lat_list.append((float(bounds['minx']) + float(bounds['maxx'])) / 2)
            lon_list.append((float(bounds['miny']) + float(bounds['maxy'])) / 2)

    if lat_list and lon_list:
        return [round(sum(lon_list) / len(lon_list), 6), round(sum(lat_list) / len(lat_list), 6)]
    else:
        return [0, 0]


if __name__ == '__main__':
    print(get_centre_map(layer_list = ['test:vs', 'test:ts']))
