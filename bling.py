#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json, logging, datetime, os, pprint

now_t = datetime.datetime.now()

past_t = now_t + datetime.timedelta(days=-1)

# Acessing a order j['retorno']['pedidos'][0]['pedido']

class Get_Bling(object):

    def __init__(self):
        self.BlingApiKey = 'a87348cb0e356da1d3ef13ceffb230727a8def0d00463ffb48970891dfe5391f1a8721a9'
        self.URL = "https://bling.com.br/Api/v2/"
        self.URLget = "https://bling.com.br/Api/v2/pedidos/json/&apikey="+self.BlingApiKey


    #=============================
    #Orders---------------------

    def last_orders(self, number_to_show=None):
        request_init_date = "{}/{}/{}".format(past_t.day, past_t.month, past_t.year)
        request_end_date = "{}/{}/{}".format(now_t.day, now_t.month, now_t.year)
        get_request = "filters=dataEmissao[{} TO {}]".format(
            request_init_date, request_end_date)

        request = requests.get(
            self.URLget, get_request)

        jsonResponse = json.loads(request.content)

        return jsonResponse

    def print_last_orders(self):
        print(self.last_orders())
        return 1

    def resume_last_orders(self, number_to_show=None):
        text_archive = []
        for i in self.last_orders()['retorno']['pedidos']:
            i = i['pedido']
            #print(i['transporte'])
            resume_item = {   
                'num_lj':           None if 'loja' not in i else i['loja'],
                'numero_woo':       None if 'numeroPedidoLoja' not in i else i['numeroPedidoLoja'].split("_")[0],
                'numero_bling':     i['numero'],
                'nome':             i['cliente']['nome'],
                'rastreio':         None if 'codigosRastreamento' not in i else i['codigosRastreamento']['codigoRastreamento'],
                'previsao_entrega': None if 'volumes' not in i['transporte'] else i['transporte']['volumes'][0]['volume']['prazoEntregaPrevisto'],
                'servico':          None if 'volumes' not in i['transporte'] else i['transporte']['volumes'][0]['volume']['servico']
                }
            #print(resume_item)
            text_archive.append(resume_item)

        if number_to_show == None:
            print(text_archive)
            return text_archive
        else:
            result = text_archive[-number_to_show:]
            print(result)
            return result

    def get_order(self, bling_order_number):
        request_url = self.URL+"/pedido/{}/json/".format(bling_order_number)
        data = {'apikey':self.BlingApiKey}
        r = requests.get(request_url, data)
        print("\n")
        return r.content


    #=============================
    #Invoice---------------------
    def do_invoice(self, order_number):
        order = self.get_order(order_number)['retorno']['pedidos'][0]['pedido']
        
        cr = self.create_xml_element
        
        inv = cr('?xml version="1.0" encoding="UTF-8"?',model="<")
        inv += cr("pedido", model="<")

        #Do Client part ----------------------------------------------------
        inv += self.xml_client(order)
        #Start Transporte process-------------------------------------------
        inv += self.xml_transport(order)
        #itens Process -----------------------------------------------------
        inv += self.xml_itens(order)


        inv += cr("pedido", model=">")
    
    def xml_client(self, order):
        client = order['cliente']
        cr = self.create_xml_element

        #Start Client Process---------------------------------------------
        cl = cr("cliente", model="<")
        cl += cr("nome", client["nome"])
            #TipodePessoa-------------------
        cl += cr("cnpj", client["cnpj"])
            #ie_rg--------------------------
        cl += cr("endereco", client["endereco"])
        cl += cr("numero", client["numero"])
        cl += cr("complemento", client["complemento"])
        cl += cr("bairro", client["bairro"])
        cl += cr("cep", client["cep"])
        cl += cr("cidade", client["cidade"])
        cl += cr("uf", client["uf"])
        cl += cr("fone", client["fone"])
        cl += cr("email", client["email"])

        cl += cr("cliente", model=">")
        return cl

    def xml_transport(self, order):
        transporte = order["transporte"]
        cr = self.create_xml_element
        tr = cr("transporte", model="<")

        tr = cr("dados_etiqueta", model="<")
        tr_list = ["nome", "endereco", "numero","complemento", "municipio","uf","cep","bairro"]
        for n in tr_list:
            tr+= cr(n, transporte["dados_etiqueta"][n])
        tr += cr("dados_etiqueta", model=">")

        tr += "<volumes><volume><servico>{}</servico></volume></volumes>".format(self.chose_by_shipping_alias(order))
        tr += cr("transporte", model=">")
        return tr

    def xml_itens(self, order):
        itens = order["itens"]
        cr = self.create_xml_element

        xml = cr("itens", model="<")
        for item in itens[0]:
            xml+= cr("item", model="<")

            xml+= cr("codigo",item["codigo"])
            xml+= cr("descricao",item["descricao"])
            xml+= cr("un","UN")
            xml+= cr("qtde",item["quantidade"])
            xml+= cr("vlr_unit",item["valorunidade"])
            xml+= cr("tipo","P")
            xml+= cr("class_fiscal","4901.99.00")
            xml+= cr("origem","0")

            xml+= cr("item", model=">")

        xml += cr("itens", model=">")
        return xml


    #=============================
    #Shipping---------------------

    def chose_shipping_method_mandae(self, order_number):
        #prepare url
        request_url = self.URL+"logistica/rastreamento/pedido/{}/json/".format(order_number)
        
        order = self.get_order(order_number)
        order_comment = self.get_comment(order)

        xml_template = "<rastreamentos><rastreamento><id_servico>{}</id_servico><codigo></codigo></rastreamento></rastreamentos>"
        
        if "Econômico" in order_comment: 
            xml =  xml_template.format("2992972993")
        elif "Rápido" in order_comment: 
            xml =  xml_template.format("2992972996")
            
        data = {
            'apikey': self.BlingApiKey,
            'xml': xml
        }
        print(xml + "\n")
        r = requests.post(request_url, data=data)
        print(r.content)
        return "did"

    def add_modico(self,SRO):
        return '''
                <rastreamentos><rastreamento><id_servico>1142829997</id_servico>
                        <codigo>{}</codigo></rastreamento></rastreamentos>'''.format(SRO)
    
    def get_all_methods(self):

        request_url = self.URL+"logisticas/servicos/json/&apikey="+self.BlingApiKey
        
        r = requests.get(request_url)
        print(r.content)

    def get_comment(self, order):
        if type(order) == type(0):
            return False
        else:
            return json.loads(order)['retorno']['pedidos'][0]['pedido']['observacoes']

    def create_xml_element(self, element, content="", model="<>"):
        if model == "<>":
            return "<{e}>{c}</{e}>".format(e=element, c=content)
        elif model =="<":
            return "<{e}>{c}".format(e=element, c=content)
        elif model == ">":
            return "{c}</{e}>".format(e=element, c=content)

    def chose_by_shipping_alias(self, order):
        
        comment = self.get_comment(order)

        if "Rápido" in comment:
            return "Rápido"
        elif "Econômico" in comment:
            return "Econômico"
        elif "PAC" in comment:
            return "Pac"
        elif "SEDEX" in comment:
            return "SEDEX"
        elif "SEDEX 10" in comment:
            return "SEDEX 10"



if __name__ == "__main__"   :
    g = Get_Bling()
    #print(g.last_orders()['retorno']['pedidos'][-1:])
    
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(json.loads(g.get_order("13940")))
    print("\n\n\n")

    #print(g.chose_shipping_method("13950"))