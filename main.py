import requests
import csv
import sys
import argparse
from urllib.parse import urlencode

def flatten_dict(dd, separator='_', prefix=''):
    return { prefix + separator + k if prefix else k : v
             for kk, vv in dd.items()
             for k, v in flatten_dict(vv, separator, kk).items()
             } if isinstance(dd, dict) else { prefix : dd }

def main(initial_month, initial_year, update_month, update_year, price):
    base_url = "https://www.aasp.org.br/calculator"
    params = {
        "action": "calculator",
        "initial_month": initial_month,
        "initial_year": initial_year,
        "update_month": update_month,
        "update_year": update_year,
        "price": price,
    }
    
    response = requests.get(base_url, params=params)
    response_json = response.json()
    flat_json = flatten_dict(response_json)

    with open("AASP.csv", "w", newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(flat_json.keys())
        writer.writerow(flat_json.values())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--initial_month", required=True)
    parser.add_argument("--initial_year", required=True)
    parser.add_argument("--update_month", required=True)
    parser.add_argument("--update_year", required=True)
    parser.add_argument("--price", required=True)
    
    args = parser.parse_args()
    
    main(args.initial_month, args.initial_year, args.update_month, args.update_year, args.price)
