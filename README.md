# tldfinder

## Summary
This tool will list all TLDs available for registration for a specific domain
name, as well as pricing at ovh.com.

## Usage

```
tldfinder [--list-tld] [--json] [--all] [-h/--help] [--maxlen LEN] [--maxprice PRICE] [--newratio RATIO] [--anynew] [--tlds TLD1,TLD2...] [--output FILE] domain1 [domain2...domainN]
List TLDs available for registration for a specified name, and their price at OVH as a CSV
	-h/--help: display this help
	--json: format output as json
	--all: show all available, not only second level registrations
	--maxlen: specify maximum length of TLDs to consider
	--maxprice: keep only results with renewal price <= PRICE (and new price <= PRICE * newratio)
	--newratio: multiplier applied to --maxprice for the new-price cap (default 2.0)
	--anynew: disable the new-price cap entirely (accept any new price)
	--list-tld: list TLDs
	--tlds: coma separated tld list to look up
	--output: write output to FILE instead of per-domain files
```
