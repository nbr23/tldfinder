import hashlib
import requests
import json
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

session = requests.Session()

def solve_challenge(challenge_url):
    id_param = parse_qs(urlparse(challenge_url).query)['id'][0]
    challenge_response = hashlib.sha256(id_param.encode('utf-8')).hexdigest()
    return {'X-Challenge-Payload': challenge_url, 'X-Challenge-Response': challenge_response}

def session_request(method, url, **kwargs):
    r = getattr(session, method)(url, **kwargs)
    data = json.loads(r.text)
    if isinstance(data, dict) and data.get('class') == 'Client::BadRequest::ChallengeRequired':
        body = data.get('body', {})
        if body.get('type') == 'url':
            challenge_url = body['payload']
            print('Challenge required:', challenge_url)
            headers = kwargs.pop('headers', {})
            headers.update(solve_challenge(challenge_url))
            r = getattr(session, method)(url, headers=headers, **kwargs)
            data = json.loads(r.text)
    return data

def get_tld_list():
    return session_request('get', 'https://order.eu.ovhcloud.com/engine/api/v1/domain/data/extension')

def get_cart_id():
    expire = (datetime.now().astimezone() + timedelta(hours=24)).isoformat(timespec='seconds')
    data = session_request('post', 'https://order.eu.ovhcloud.com/engine/api/v1/order/cart',
            data='{"expire":"%s","ovhSubsidiary":"FR"}' % expire)
    return data['cartId']

def get_prices_string(prices):
    pricelist = {price['label']: price['price']['text'] for price in prices}
    return pricelist

def filter_second_lvl(tld_list):
    return [tld for tld in tld_list if '.' not in tld]

def filter_max_len(tld_list, max_len):
    return [tld for tld in tld_list if len(tld) <= max_len]

def get_available_tlds(domains, tld_list):
    cart_id = get_cart_id()
    for domain in domains:
        parts = domain.split('.', 1)
        effective_tlds = [parts[1]] if len(parts) > 1 else tld_list
        total = len(effective_tlds)
        found = 0
        print('[%s] checking %d TLD%s' % (parts[0], total, 's' if total != 1 else ''))
        for i, tld in enumerate(effective_tlds):
            if total > 20 and i > 0 and i % 10 == 0:
                print('[%s] %d/%d (%.0f%%)' % (parts[0], i, total, 100 * i / total))
            results = session_request('get', f'https://order.eu.ovhcloud.com/engine/api/v1/order/cart/{cart_id}/domain?domain={parts[0]}.{tld}')
            for elt in results:
                if 'action' in elt and elt['action'] == 'create':
                    elt.update(get_prices_string(elt['prices']))
                    elt['domain'] = '%s.%s' % (parts[0], tld)
                    del elt['prices']
                    found += 1
                    yield elt
        print('[%s] done: %d available' % (parts[0], found))

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
