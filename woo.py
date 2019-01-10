from woocommerce import API
from woo_credentials import *
import datetime, os
import requests
import sys


wcapi = API(
    url=wooURL(),
    consumer_key=wooConKey(),
    consumer_secret=wooConSecret(),
    wp_api=True,
    version="wc/v2")

class Orders(object):
    '''
    Orders
    ======

    this is the class that manage woocommerce orders
    ------------------------------------------------
    '''
    def get(self, order_number=0):
        if order_number == 0:
            response = wcapi.get("orders?status=processing")
        else:
            response = wcapi.get("orders/" + order_number)
        
        return response

    def add_note(self, order_number,message):
        return "result"

    def add_correios_shipping_code(self, order_number):
        return "result"

    def add_mandae_shipping_code(self, order_number):
        return "result"

    def change_to_processing(self, order_number):
        return "result"

    def change_to_clompleted(self, order_number):
        return "result"

    def verify_correios_shipping(self, order_number):
        return "result"

    def verify_mandae_shipping(self, order_number):
        return "result"


class Clients(object):
    '''
    Clients
    ======

    this is the class that manage woocommerce clients
    ------------------------------------------------
    '''
    def get(self, client_number):
        return "result"


if __name__ == "__main__" :
    o = Orders()
    print(o.get("77").text)