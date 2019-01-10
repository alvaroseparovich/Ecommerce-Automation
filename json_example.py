import json

docs = {
    "Data": "09-10-2018",
    "Qtd": 3,
    "Processed":2,
    "Erros_Founded":1,
    "Indice":{111,112,113},
    "Orders":{
        111:{
            "Nome":"joao carlos pereira",
            "CPF":"000.000.000-11",
            "Tel":{1:"(14) 1414-1414"},
            "Email":"141414@hotmail.com",
            "NFE":"",
            "Status":"Processando",
            "Envio":{
                "Empresa":"Mandae",
                "Metodo_selecionado": "Rápido",
                "Code": "123456789",
                "Entregue":True,
                "Codigo_no_site": False,
                "Bling_selected":False,
            },
            "Qtd":1,
            "Primeira_compra":True,
            "Payment_method":"card",
            "Valor":185.45 ,
            "Parcelas":3,
            "Tested":True,
            "Telefone_error": "Doesn't Exist",
            "Secure_score": 0,
            "Itens":{
                "1":{
                    "Nome":"Dicionário Bíblico Wycliffe",
                    "REF": "9788526308091",
                    "Preco": 160.00,
                    "Qtd":1
                }

            }

        },
        112:{
            "Nome":"joao donato",
            "CPF":"000.000.000-11",
            "Tel":{1:"(14) 1414-1414"},
            "Email":"141414@hotmail.com",
            "NFE":"",
            "Status":"Processando",
            "Envio":{
                "Empresa":"Mandae",
                "Metodo_selecionado": "Rápido",
                "Code": "123456789",
                "Entregue":True,
                "Codigo_no_site": False,
                "Bling_selected":False,
            },
            "Qtd":2,
            "Primeira_compra":False,
            "Payment_method":"boleto",
            "Valor":245.45,
            "Parcelas":1,
            "Tested":True,
            "Telefone_error": "",
            "Secure_score": 5,
            "Itens":{
                "1":{
                    "Nome":"Dicionário Bíblico Wycliffe",
                    "REF": "9788526308091",
                    "Preco": 160.00,
                    "Qtd":1
                },
                "2":{
                    "Nome":"Picles",
                    "REF": "9788526308092",
                    "Preco": 60.00,
                    "Qtd":1
                }

            }

        },
        113:{
            "Nome":"mark pereira",
            "CPF":"000.000.000-11",
            "Tel":{1:"(14) 1414-1414"},
            "Email":"141414@hotmail.com",
            "NFE":"",
            "Status":"Processando",
            "Envio":{
                "Empresa":"Mandae",
                "Metodo_selecionado": "Rápido",
                "Code": "123456789",
                "Entregue":True,
                "Codigo_no_site": False,
                "Bling_selected":False,
            },
            "Qtd":2,
            "Primeira_compra":False,
            "Payment_method":"boleto",
            "Valor":200.45,
            "Parcelas":1,
            "Tested":False,
            "Telefone_error": "",
            "Secure_score": 0,
            "Itens":{
                "1":{
                    "Nome":"Pey the bill",
                    "REF": "9788526355548",
                    "Preco": 180.00,
                    "Qtd":2
                }

            }

        }
    }
}