#! /usr/bin/env python3

import sys
import json
from . import json_print_available, csv_print_available, get_available_tlds, get_tld_list, filter_second_lvl, filter_max_len

def main():
    argv = sys.argv
    printer = csv_print_available
    filters = [filter_second_lvl]

    if '--all' in argv:
        index = argv.index('--all')
        argv = argv[:index] + argv[index + 1:]
        filters.remove(filter_second_lvl)

    if '--maxlen' in argv:
        index = argv.index('--maxlen')
        maxlen = int(argv[index + 1])
        argv = argv[:index] + argv[index + 2:]
        filters.append(lambda x: filter_max_len(x, maxlen))

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
        printer = json_print_available
        index = argv.index('--json')
        argv = argv[:index] + argv[index + 1:]

    if '-h' in argv or '--help' in argv or len(argv) < 2:
        print('%s [--list-tld] [--json] [--all] [-h/--help] [--maxlen] domain1 [domain2...domainN]\nList TLDs available for registration for a specified name, and their price at OVH as a CSV\n\t-h/--help: display this help\n\t--json: format output as json\n\t--all: show all available, not only second level registrations\n\t--maxlen: specify maximum length of TLDs to consider\n\t--list-tld: list TLDs' % argv[0])
        return 0

    printer(get_available_tlds(argv[1:], tld_list))

if __name__ == '__main__':
    exit(main())
