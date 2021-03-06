#-*- coding: utf-8 -*-
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, Compose, MapCompose, Identity
import re

def return_first(value):
    return value and value[0] or u''

def flight_status_handler(value):
    for idx, item in enumerate(value):
        item = item.strip().lower()
        if item == u'отправлен':
            value[idx] = u'вылетел'
        elif item in (u'прибыл', u'позднее прибытие', u'приземлился'):
            value[idx] = u'прилетел'
        else:
            value[idx] = item
    return value

def title(value):
    return value[0].title()

def flight_handler(value):
    flight = re.findall(r'^(.+)', value[0], re.U) 
    value[0] = flight and flight[0].strip() or value[0]
    return value

def airline_handler(value):
    for idx, item in enumerate(value):
        item = item.strip()
        if item.endswith(u'Российские авиалинии'):
            value[idx] = item.split()[0]
        else:
            value[idx] = item
    return value

class TimetableLoader(XPathItemLoader):
   default_output_processor = Join()
   default_input_processor = MapCompose(unicode.strip)
   flight_in = Compose(flight_handler)
   flight_type_in = Identity()
   flight_type_out = Compose(return_first)
   flight_status_in = Compose(flight_status_handler)
   flight_status_out = Compose(return_first)
   city_of_departure_out = Compose(title)
   city_of_arrival_out = Compose(title)
   airport_of_departure_out = Compose(title)
   airport_of_arrival_out = Compose(title)
   airline_in = Compose(airline_handler)
   airline_out = Compose(title)
