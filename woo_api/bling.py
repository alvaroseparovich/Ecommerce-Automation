#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json, logging, datetime, os

now_t = datetime.datetime.now()
past_t = now_t + datetime.timedelta(days=-1)

# curl -X GET "https://bling.com.br/Api/v2/pedidos/json/" -G -d "apikey=KEY"
#----------------------------------------------------
# curl -X GET "https://bling.com.br/Api/v2/pedidos/json/" 
#   -G 
#   -d "apikey=KEY"

BlingApiKey = 'KEY'
URLget = "https://bling.com.br/Api/v2/pedidos/json/&apikey="+BlingApiKey

request_init_date = "{}/{}/{}".format(past_t.day-1, past_t.month, past_t.year)
request_end_date = "{}/{}/{}".format(now_t.day, now_t.month, now_t.year)
get_request = "filters=dataEmissao[{} TO {}]".format(
    request_init_date, request_end_date)

request = requests.get(
    URLget, get_request)

statuscode = request.status_code
jsonResponse = json.loads(request.content)
j = jsonResponse
# Acessing a order j['retorno']['pedidos'][0]['pedido']

#----------------------------
dir_path = "colected-data/{}/{}".format(now_t.year , now_t.month)
archive_path = "colected-data/{}/{}/{}-{}-{}-{}-response.json".format(now_t.year , now_t.month , now_t.day , now_t.hour , now_t.minute , now_t.second)

if not os.path.exists(dir_path):
    os.makedirs(dir_path)
#file = open(archive_path,"w")
text_archive = []
for i in j['retorno']['pedidos']:
    i = i['pedido']
    if "tipoIntegracao" in i and i["tipoIntegracao"] == "WooCommerceWH":
        #print(i['transporte'])
        resume_item = {   
            'num_lj':           i['loja'],
            'numero_woo':       i['numeroPedidoLoja'].split("_")[0],
            'numero_bling':     i['numero'],
            'rastreio':         None if 'codigosRastreamento' not in i else i['codigosRastreamento']['codigoRastreamento'],
            'previsao_entrega': None if 'volumes' not in i['transporte'] else i['transporte']['volumes'][0]['volume']['prazoEntregaPrevisto'],
            'servico':          None if 'volumes' not in i['transporte'] else i['transporte']['volumes'][0]['volume']['servico']
        }
        #print(resume_item)
        text_archive.append(resume_item)
print(text_archive[0])
#file.write(str(text_archive))
#file.close()
#print("file writed")
exit()
#ps = j[0]
#print(j['retorno']['pedidos'][0]['pedido'])
ps = j['retorno']['pedidos']

pWoo = []

for i in ps:
    i = i['pedido']
    if "tipoIntegracao" in i and i["tipoIntegracao"] == "WooCommerceWH":
        pWoo.append(i)

for i in ps:
    p = i
    i = i['pedido']
    if 'codigosRastreamento' in i and "codigoRastreamento" not in i['codigosRastreamento']:
        print(type(p))


print("ps tem " + str(len(ps)) +" itens")
print("pWoo tem " + str(len(pWoo)) + " itens")