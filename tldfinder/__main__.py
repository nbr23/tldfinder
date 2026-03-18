#! /usr/bin/env python3

import sys
import json
from . import json_print_available, csv_print_available, csv_write, json_write, get_available_tlds, get_tld_list, filter_second_lvl, filter_max_len

def main():
    argv = sys.argv
    printer = csv_print_available
    filters = [filter_second_lvl]
    use_json = False
    output = None

    if '--all' in argv:
        index = argv.index('--all')
        argv = argv[:index] + argv[index + 1:]
        filters.remove(filter_second_lvl)

    if '--maxlen' in argv:
        index = argv.index('--maxlen')
        maxlen = int(argv[index + 1])
        argv = argv[:index] + argv[index + 2:]
        filters.append(lambda x: filter_max_len(x, maxlen))

    if '--tlds' in argv:
        index = argv.index('--tlds')
        tld_list = argv[index + 1].split(',')
        argv = argv[:index] + argv[index + 2:]
    else:
        tld_list = get_tld_list()

    for fn in filters:
        tld_list = fn(tld_list)

    if '--list-tld' in argv:
        if '--json' in argv:
            print(json.dumps(tld_list))
        else:
            for tld in tld_list:
                print(tld)
        return 0

    if '--json' in argv:
        use_json = True
        printer = json_print_available
        index = argv.index('--json')
        argv = argv[:index] + argv[index + 1:]

    if '--output' in argv:
        index = argv.index('--output')
        output = argv[index + 1]
        argv = argv[:index] + argv[index + 2:]

    if '-h' in argv or '--help' in argv or len(argv) < 2:
        print('%s [--list-tld] [--json] [--all] [-h/--help] [--maxlen LEN] [--tlds TLD1,TLD2...] [--output FILE] domain1 [domain2...domainN]\nList TLDs available for registration for a specified name, and their price at OVH as a CSV\n\t-h/--help: display this help\n\t--json: format output as json\n\t--all: show all available, not only second level registrations\n\t--maxlen: specify maximum length of TLDs to consider\n\t--list-tld: list TLDs\n\t--tlds: coma separated tld list to look up\n\t--output: write output to FILE instead of per-domain files' % argv[0])
        return 0

    domains = argv[1:]
    ext = 'json' if use_json else 'csv'
    writer = json_write if use_json else csv_write

    if output:
        writer(get_available_tlds(domains, tld_list), output)
    else:
        for domain in domains:
            writer(get_available_tlds([domain], tld_list), '%s.%s' % (domain, ext))

if __name__ == '__main__':
    exit(main())
