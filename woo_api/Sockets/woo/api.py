from woocommerce import API
import datetime, os
import requests
import sys


globals()
#After response 
#r.status_code
#r.headers['content-type']
#r.encoding
#r.text
#r.json()

wcapi = API(
    url=woocommerceURL,
    consumer_key=woocommerceConsumerKey,
    consumer_secret=woocommerceConsumerSecret,
    wp_api=True,
    version="wc/v2")

#get_request = 'orders'
#r = wcapi.get("orders?status=processing&page=1000")
r = wcapi.get("orders?status=processing")
#re = r.status_code
#print(len(r.json()))

#exit()
#r = r.json()["correios_tracking_code"]


#===========================================
def check_obj(order_object):
    '''Check if is proccessing and if the RSO is showing shipped'''
    sro = order_object['correios_tracking_code']
    print("Now is " + order_object['status'])

    if sro == "":
        return False
    if "," in sro:
        sro = sro.split(",")[-1]

    print("The Last Traking Code is :" + sro)

    if order_object['status'] == "processing":
        r = requests.get(
            "http://portalpostal.com.br/sro.jsp?sro={}".format(sro))
        print("Requisition in correios recive: " + str(r.status_code))
        soup = BeautifulSoup(r.text, 'html.parser')
        print(soup.prettify())
        l = soup.table.find_all('font')

        for i in l:
            if 'Objeto entregue ao destinatário' in i:
                return order_object['id']

        return False
#check_obj(r)


#===========================================
def change_to_completed(order_number, add_note=True):
    '''Write a Document to preserve data colected'''
    if order_number == False:
        print("***This order was not Shipped, it will stay Precessing!")
        return False
    
    data = {"status": "completed"}
    response = wcapi.put("orders/{}".format(order_number), data).status_code
    if response == 200:
        print("***Status Was Changed to Complete!")
    
    if response == 200 and add_note:
        data = {"note": "Modificado para concluido via Automatização!"}
        note_response = wcapi.post(
            "orders/{}/notes".format(order_number), data).status_code
        
        #print(note_response)
        if note_response == 201:
            print("Note Added")
        else:
            print("note Didn't Add")
#change_to_completed('25975')


#===========================================
def Archive_debug_open(archive_extension=""):
    now_t = datetime.datetime.now()
    dir_path = "colected-data/debug/{}/{}".format(now_t.year, now_t.month)
    archive_path = "colected-data/debug/{}/{}/{}{}-{}-{}.txt".format(
        now_t.year, now_t.month, archive_extension + "-", now_t.day, now_t.hour, now_t.minute)

    #write
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return open(archive_path, "a+")


#===========================================
def write(content):
    '''Write a Document to preserve data colected'''

    #get dime
    now_t = datetime.datetime.now()
    dir_path = "colected-data/{}/{}".format(now_t.year, now_t.month)
    archive_path = "colected-data/{}/{}/woocommerce-{}-{}-{}-{}-response.json".format(
        now_t.year, now_t.month, now_t.day, now_t.hour, now_t.minute, now_t.second)
    
    #write
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file = open(archive_path,"w")
    file.write(str(r))
    file.close()
    print("Created: "+archive_path)
#write(r)


#sys.stdout = open("file.xt", "w+")
#===========================================
def processing_all_to_completed(debug_archive=False):
    '''Put all it in Action'''
    #r = wcapi.get("orders?status=processing&page={}".format(this_times))
    
    if debug_archive == True:
        sys.stdout = Archive_debug_open("processing_Completed")

    print("\n\n\n\n============================================")
    print("New Request to Turn orders to Completed")
    print(datetime.datetime.now().date())
    print(datetime.datetime.now().time())
    print("============================================\n\n")

    page = 1
    request = wcapi.get("orders?status=processing&page={}".format(page))
    while len(request.json()):
        #all we need to do
        r_json = request.json()
        for i in r_json:
            print("Order #" + str(i["id"]))
            change_to_completed(check_obj(i))
            print("-------------\n")
            
            print("Finished on the number 1")
            exit()
        
        page += 1
        request = wcapi.get("orders?status=processing&page={}".format(page))


#Check OBJ in csv
#===========================================
def consult(number="0, 0"):
    if number == "0, 0":
        print("put some numbers in 'function consult()!'")
        return
    
    arrayIds = number.split(", ")
    for id in arrayIds:
        try:
            print(id)
            product = wcapi.get("products/"+id).json()
        except IOError as e:
            print('UM ERRO OCORREU: {} : {}'.format(e.errno, e.strerror))
        else:
            title = product["name"]
            desc = product["description"]
            link = product['permalink']
            estado = "novo"
            price = "BRL " + product['sale_price'].replace('.', ',')
            estoque = "em estoque" if product["in_stock"] == True else "Em Falta"
            img = product["images"][0]["src"]
            editora = ""
            for att in product["attributes"]:
                if att['name'] == "Editora":
                    editora = (att['options'][0])
            
            isbn = ""
            for att in product["attributes"]:
                if att['name'] == "ISBN":
                    isbn = (att['options'][0])

            print("'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','784'".format(
                id, title, title, link, estado, price, estoque, img, editora, isbn))
            print()


#data={
#    "correios_tracking_code":"PPMALAKOYBR"
#}
#Coloca rastreador no Pedido
#product = wcapi.put("orders/30189", data).json()
#print(product)
#consult("16116, 9291, 14173, 9391, 16001, 12590, 6552, 14622, 16114, 15735, 6816, 8668, 9697, 9396, 2637, 15878, 8552, 346, 15557, 14273, 17583, 9386, 13442, 9398, 8731, 23184, 9387, 58, 12601, 9397, 9393, 23048, 8741, 2531, 11962, 2565, 7447, 23497, 9624, 2626, 13984, 9394, 7419, 2548, 18394, 16032, 16796, 5860, 2583, 2584, 2540, 267, 16058, 7412, 12776, 9385, 2622, 2572, 9389, 2505, 12775, 2613, 431, 21343, 9390, 9302, 8720, 22748, 18389, 11990, 6735, 6627, 2496, 16990, 8296, 2553, 9384, 8535, 7382, 6337, 6217, 2602, 2591, 2559, 22500, 7269, 2598, 84, 21534, 19659, 16459, 16027, 8509, 2593, 26508, 23986, 20629, 18360, 15541, 12771, 10395, 7842, 7820, 6630, 5897, 2629, 2550, 2510, 6628, 6311, 2614, 2621, 2571, 2551, 27197, 19706, 15893, 2560, 2474, 1200, 26974, 25261, 12074, 20648, 20645, 18289, 2896, 2524, 16943, 6629, 2616, 2558, 256, 21827, 12065, 9583, 128, 26684, 25701, 19547, 15429, 15051, 10378, 10369, 5981, 16024, 14591, 8530, 3520, 2640, 2530, 24998, 19739, 9152, 9022, 6723, 6037, 2589, 2534, 2545, 23203, 21345, 15055, 14182, 9459, 8734, 7670, 2628, 2618, 2631, 2600, 2529, 2508, 144, 30467, 9975, 23013, 18699, 16204, 15581, 14643, 9699, 9395, 9392, 2619, 2611, 2536, 353, 345, 309, 136, 30474, 23989, 16237, 15800, 14180, 8529, 8533, 8257, 8254, 6172, 3183, 2620, 2562, 2533, 2506, 2503, 87, 28858, 23330, 19502, 14669, 12010, 9926, 7832, 6379, 5861, 5157, 2595, 2552, 2513, 391, 23981, 19320")


print(r.text)
print("i was runned")