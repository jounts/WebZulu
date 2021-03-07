"""
Module retrieving published projects and layers on zulu server
"""

from xml.etree import ElementTree

import requests

from WebZulu.settings import GIS_SERVER


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
