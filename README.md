# csv-pay
crypto payouts from a csv file
##usage
usage: ``payout-processor.py <daemon> <filename> <amount> <csv address column #> <debugging>``

daemon is required, the name of the binary (evergreencoind, for example)
csv address columns are ZERO-INDEXED
setting debugging to any value enables it


Send payments using CSV database

positional arguments:
  daemon                use this *coind

optional arguments:
  -h, --help            show this help message and exit
  -f filename, --infile filename
                        CSV to read
  -a amount, --amount amount
                        payout amount
  -i pos, --index pos   column number of the address
  --debug debug         just print some stuff
