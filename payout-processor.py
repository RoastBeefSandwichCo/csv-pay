#!/usr/bin/env python2.7
import sys
import subprocess
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Send payments using CSV database')
    parser.add_argument('daemon', metavar='daemon', type=str,
                       help='use this *coind')
    parser.add_argument('-f', '--infile', metavar='filename', type=str,
                       help='CSV to read')
    parser.add_argument('-a', '--amount', metavar='amount', type=float,
                       help='payout amount')    
    parser.add_argument('-i', '--index', metavar='pos', type=int,
                       help='column number of the address')
    parser.add_argument('--debug', metavar='debug', type=bool,
                       help='just print some stuff')
    
    #args = parser.parse_args()
    return parser.parse_args()
    #print "args:", args
    #print args.accumulate(args.integers)

def parse_csv(csv_line, index):
    print ("csv line", csv_line)
    #print "split:", csv_line.split(",")
    address = csv_line.split(",")[index].strip('"')
    return address


def send_payout(daemon, address, amount):
    tx_id = ""
    tx_id = subprocess.check_output([daemon, "sendtoaddress", str(address), str(amount), "faucet test" ]).strip()
    print "address", address, "output:", tx_id
    return tx_id


def main():
    args = parse_args()
    print "args:", args
    daemon = args.daemon
    print "daemon:", daemon
    input_filename = args.infile
    print "infile:", input_filename
    string_pieces = input_filename.partition(".")
    output_filename = string_pieces[0] + "-PAID-COMPLETE" + string_pieces[1] + string_pieces[2] #creates a new csv plus txid column
    print "output file:", output_filename
    amount = args.amount
    print "amount:", amount
    index_of_address = args.index
    print "index of address:", index_of_address
    print "debugging:", args.debug
    if args.debug==True:
        sys.exit()
    #sys.exit()

    print "Reading " + input_filename
    print "Writing to: " + output_filename
    print "Address position: " + str(index_of_address)
    print "Send amount: " + str(amount)

    with open (input_filename, 'r') as pending_payouts:
        counter = 0  #(used only for skipping line 0)
        for each in pending_payouts.readlines():
            each = each.strip()
            counter += 1
            if counter < 2:  #Line zero. Add the paid out column
                payout_log_string =  each + ',"payout_txid"\r\n'
                print "new columns:", payout_log_string 
                with open (output_filename, 'w') as completed_payouts:
                    completed_payouts.write(payout_log_string)
                continue

            tx_id = send_payout(daemon, parse_csv(each, index_of_address), amount) #send the payout, get txid
            payout_log_string = each + ',"' + tx_id + '"\r\n'#create new Row string
            with open (output_filename, 'a') as completed_payouts:
                completed_payouts.write(payout_log_string) #log it to the new csv
                print "payout log string: ", payout_log_string


if __name__ == '__main__':
    main()
