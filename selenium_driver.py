from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from bling import Get_Bling as gb
from secret_inf as inf



class Selenium_drive(object):

    def __init__(self):
        self.driver = webdriver.Chrome("./chromedriver")
    
    def login(self):
        self.driver.get("https://www.bling.com.br/login")
        username = self.driver.find_element_by_name("username")
        password = self.driver.find_element_by_name("senha")

        username.send_keys(inf.b_user())
        password.send_keys(inf.b_pass())
        password.send_keys(Keys.RETURN)
        self.until_it_apear("#menu_novo")
        self.close_pop()
        return

    def process(self,order_id):
        self.open_order(order_id)
        if self.order_shipping_select() ==  "interrompe":
            return
        self.until_be_clickable("#botaoSalvar")
        self.driver.execute_script("salvar();return false;")
        self.prepare_order_invoice(order_id)

    def process_all(self):
        self.driver.get("https://www.bling.com.br/vendas.php#list")
        print("-Aguardando listagem...")
        time.sleep(3)
        try:
            order_id = self.driver.execute_script("return document.querySelector('.linhaItem').id;")
        except:
            print("-Não há mais nenhum pedido!")
            return False
        else:
            print("-Começando a Processar o pedido!")
            order_id = self.driver.execute_script("return document.querySelector('.linhaItem').id;")
            print(order_id)
            self.process(order_id)
            print("\n=======================================\n Pedido Processado corretamente \n=======================================")

            self.process_all()
            return True

    def process_all_mandae(self):
        self.bling_api = bg()
        self.driver.get("https://www.bling.com.br/vendas.php#list")
        print("-Aguardando listagem...")
        time.sleep(3)
        
        ids = self.find_all(".linhaItem>td:nth-child(2)")
        #for id_compra in ids:

    def do_all_invoice_fast(self):
        self.driver.get("https://www.bling.com.br/vendas.php#list")
        print("-Aguardando listagem...")
        time.sleep(2)
        self.click("#link-pesquisa")
        time.sleep(0.5)
        self.select_option("#lojasVinculadas","El Shaddai web")
        time.sleep(1)
        try:
            print("Yeah it runed!")
            self.click("#checkAllVendas")
            self.close_pop()
            print("Yeah it runed!")
            hover = ActionChains(driver).move_to_element(self.find(".ui-state-default.ui-corner-top.ui-tabs-active.ui-state-active"))
            hover.perform()
            self.click(".ui-state-default.ui-corner-top.ui-tabs-active.ui-state-active")
            print("Yeah it runed!")
            return True
            #self.click(".act-gerar-notas.ico-xls")
        except:
            print("-Não há mais nenhum pedido!")
            return False
        else:
            print("-Começando a Processar o pedido!")
            return True

    #==========================================
    #Shipping Area-----------------------------
    def select_all_orders_shipping(self):
        '''This Method Is Not Completed!'''
        self.driver.get("https://www.bling.com.br/vendas.php#list")
        self.driver.refresh()
        time.sleep(2)

        orders = self.drive.find_elements_by_css_selector("tr.linhaItem")

        print("function not completed")
        return "function not completed"

    def order_shipping_select(self,order_id=""):
        '''select the shipping method acording to the order's comment'''
        self.until_it_apear('#observacoes')
        time.sleep(0.5)
        comment = self.driver.execute_script("window.document.querySelector('#observacoes').select(); return window.getSelection().toString();")
        
        #Select Services-----------------
        if "Econômico" in comment:
            self.select_shipping("Mandaê", "Econômico")
        elif "Rápido" in comment:
            self.select_shipping("Mandaê", "Rápido")
        elif "Tipo de Frete: PAC" in comment:
            #return "interrompe"
            self.select_shipping("Correios", "PAC CONTRATO AGENCIA")
            
        elif "Tipo de Frete: SEDEX" in comment:
            #return "interrompe"
            self.select_shipping("Correios", "SEDEX CONTRATO AGENCIA")
            
        elif "Tipo de Frete: SEDEX 10" in comment:
            #return "interrompe"
            self.select_shipping("Correios", "SEDEX 10")
            
        elif "MÓDICO" in comment:
            #return "interrompe"
            print("Módico selecionado! ...")
            shipping_code = input("Bipe a etiqueta no campo de entrega válida!\n\n")

            print("\n\nMÓDICO registrado, inutilize a etiqueta!\n\n")


        elif "RETIRAR NA LOJA FÍSICA" in comment:
            print("--Retirada na loja--")
            return True
        else:
            print("-Nenhum método válido foi encontrado! :(")
            return False
        
        return True

    def select_shipping(self, company, service, code=None):
        '''Select shipping acording to company and service recived'''

        self.select_option('#integracaoLogistica', company)
        self.until_it_apear("select[name='servicosLogistica[]'")
        time.sleep(0.2)
        self.select_option("select[name='servicosLogistica[]'", service)

        if not code == None :
            self.find("[name='trackings[]']").send_keys(code)


    #==========================================
    #Invoice-----------------------------------
    def correct_all_invoice_fields(self):
        self.wait_apear("#tItensNota .linhaItemNota")
        itens = self.find_all("#tItensNota .linhaItemNota")
        i=0
        for item in itens:
            print("processando - " + self.find("td:nth-child(1)", item ).find_element_by_css_selector("p").text)
            time.sleep(1)
            self.click("#item"+str(i))
            self.wait_apear("#edCf")
            time.sleep(0.2)
            self.find("#gtin").clear()
            self.find("#gtinEmbalagem").clear()
            if not self.js_ex("window.document.querySelector('#edUn').select(); return window.getSelection().toString();") == "UN":
                self.find("#edUn").send_keys("UN")
            if self.js_ex("window.document.querySelector('#edCf').select(); return window.getSelection().toString();") == "":
                self.find("#edCf").send_keys("4901.99.00")
            time.sleep(0.2)
            self.find("#link_aba_icms").click()
            self.wait_apear("#edOrigem")
            self.select_option( "#edOrigem", "0 - Nacional, exceto as indicadas nos códigos 3, 4, 5 e 8" )
            #Finish and Save that Product
            self.driver.execute_script("salvarItemEdicao()")
            time.sleep(0.3)
            i=i+1
        inf = self.js_ex("window.document.querySelector('#contato').select(); return window.getSelection().toString();")   
        print("Nota do Cliente -  " + inf + " - CONCLUIDA!")
        return

    def prepare_order_invoice(self, order_id):
        self.driver.get("https://www.bling.com.br/notas.fiscais.php?idOrigem="+order_id)
        self.correct_all_invoice_fields()
        if self.there_is("select[name='servicosLogistica[]'"):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.click_when_possible("#controls>#botaoSalvar")
            return True
        else:
            print("Não á metodo selecionado!")
            return False
        

    #==========================================
    #Order Area------------------------------
    def open_order(self, order_id):
        self.driver.get("https://www.bling.com.br/vendas.php#edit/"+order_id)
        self.driver.refresh()
        self.until_be_clickable("#botaoSalvar")
        return
    

    #==========================================
    #Product Area------------------------------
    def add_ncm(self,product_number=0, ncm="4901.99.00"):
        
        if not self.is_that_url("https://www.bling.com.br/produtos.php#edit/"+product_number):
            self.driver.get("https://www.bling.com.br/produtos.php")
            self.close_pop()
        
        self.driver.get("https://www.bling.com.br/produtos.php#edit/"+product_number)
        self.driver.refresh()
        time.sleep(2)           
        
        self.driver.find_element_by_css_selector("li[data-tab=div_tributacao]>a").click()
        ncm_form = self.driver.find_element_by_css_selector("#cf")
        ncm_form.send_keys(ncm)
        
        return 


    #==========================================
    #Helpers ----------------------------------
    def is_that_url(self, URL=""):
        if self.driver.current_url == URL :
            return True
        else:
            return False

    def there_is(self, selector_css):
        try:
            self.driver.find_element_by_css_selector(selector_css)
        except:
            return False
        else:
            return True

    def until_it_apear(self, selector_css):
        try:
            element = wdw(self.driver, 0.1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector_css))
            )
        finally:
            return True

    def until_be_clickable(self, selector_css):
        try:
            element = wdw(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector_css))
            )
            #print("try - until_be_clickable")
        finally:
            #print("finally")
            return True

    def wait_apear(self, selector_css):
        try:
            self.find(selector_css)
        except:
            self.wait_apear(selector_css)
        else:
            return True

    def click_when_possible(self, selector_css):
        try:
            self.click(selector_css)
        except:
            self.click_when_possible(selector_css)
        else:
            return True

    def close_pop(self):
        try:
            time.sleep(2)
            self.find(".hopscotch-bubble-close.hopscotch-close").click()
        except:
            pass
        try:
            self.find(".useful-info-warning.footer-message>div>i").click()
        except:
            pass

    def select_option(self, selector_css, option_text):
        '''Recive a CssSelector and chose a option'''

        select_element = self.driver.find_element_by_css_selector(selector_css)
        for option in select_element.find_elements_by_tag_name('option'):
            if option.text == option_text:
                option.click()
                return True
        return False

    def click(self, selector_css):
        self.driver.find_element_by_css_selector(selector_css).click()

    def find(self, selector_css, here=0):
        if here is 0:
            return self.driver.find_element_by_css_selector(selector_css)
        else:
            return here.find_element_by_css_selector(selector_css)
    
    def find_all(self, selector_css, here=0):
        if here is 0:
            return self.driver.find_elements_by_css_selector(selector_css)
        else:
            return here.find_elements_by_css_selector(selector_css)

    def js_ex(self, code):
        return self.driver.execute_script(code) 


if __name__ == "__main__":
    chrome = Selenium_drive()
    chrome.login()
    chrome.find("#menu-container")
    print("--------------------------\n Começando a processar os pedidos \n--------------------------")
    #chrome.process_all()
    chrome.do_all_invoice_fast()
    #chrome.driver.close()



