import secret_inf.Woocommerce_local as inf

global_arg = {
        "woocommerceConsumerKey":       inf.woocommerceConsumerKey(),
        "woocommerceConsumerSecret":    inf.woocommerceConsumerSecret(),
        "woocommerceURL":               inf.woocommerceURL()
    }
#run api code?
if True :
    exec(open('./Sockets/woo/api.py').read(), global_arg)
