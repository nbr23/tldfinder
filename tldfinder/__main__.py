#! /usr/bin/env python3

import sys
from . import json_print_available, csv_print_available, get_available_tlds, get_tld_list

def main(argv):
    printer = csv_print_available
    second_only = True
    if '--json' in argv:
        printer = json_print_available
        index = argv.index('--json')
        argv = argv[:index] + argv[index + 1:]

    if '--all' in argv:
        second_only = False
        index = argv.index('--all')
        argv = argv[:index] + argv[index + 1:]

    if '--list-tld' in argv:
        for tld in get_tld_list():
            if second_only and '.' in tld:
                continue
            print(tld)
        return 0

    if '-h' in argv or len(argv) < 2:
        print('%s [--json] [--all] [-h] domain1 [domain2...domainN]\nList TLDs available for registration for a specified name, and their price at OVH as a CSV\n\t-h: display this help\n\t--json: format output as json\n\t--all: show all available, not only second level registrations' % argv[0])
        return 0

    printer(get_available_tlds(argv[1:], second_only))

if __name__ == '__main__':
    exit(main(sys.argv))
