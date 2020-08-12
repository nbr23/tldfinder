import requests
import json

def get_tld_list():
    return json.loads(requests.get('https://www.ovh.com/engine/apiv6/domain/data/extension').text)

def get_cart_id():
    r = requests.post('https://www.ovh.com/engine/apiv6/order/cart',
            data='{"description":"_ovhcom_legacy_order_cart_", "ovhSubsidiary":"FR"}')
    return json.loads(r.text)['cartId']

def get_prices_string(prices):
    pricelist = {price['label']: price['price']['text'] for price in prices}
    return pricelist

def get_available_tlds(domains, second_only):
    cart_id = get_cart_id()
    all_tlds = get_tld_list()
    for domain in domains:
        domain = domain.split('.', 1)
        tldlist = [domain[1]] if len(domain) > 1 else all_tlds
        for tld in tldlist:
            if second_only and '.' in tld:
                continue
            results = json.loads(requests.get('https://www.ovh.com/engine/apiv6/order/cart/%s/domain?domain=%s.%s' % (cart_id, domain[0], tld)).text)
            for elt in results:
                if 'action' in elt and elt['action'] == 'create':
                    elt.update(get_prices_string(elt['prices']))
                    elt['domain'] = '%s.%s' % (domain[0], tld)
                    del elt['prices']
                    yield elt

def json_format(tlds):
    return json.dumps(list(tlds))

def json_print_available(tlds):
    print(json_format(tlds))

def csv_format(tlds):
    yield 'domain;price new;price renew'
    for elt in tlds:
        yield '%s;%s;%s' % (elt['domain'], elt['TOTAL'], elt['RENEW'])

def csv_print_available(tlds):
    for line in csv_format(tlds):
        print(line)
