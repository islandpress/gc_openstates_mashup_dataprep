"""
This script is for pulling climate change bill data from OpenStates and 
writing it to a spreadsheet.

As a prerequisite, get an Open States API key and set it in environment
variable: OPEN_STATES_API_KEY

For more details about Open States, see
    http://docs.openstates.org/en/latest/api/bills.html#bill-search
    http://docs.openstates.org/en/latest/api/committees.html#committees
"""

import os
import json
import urllib
import argparse
import pandas as pd
import requests
import re


def cleanup_bills(df_bills):
    def cb_subs(x):
        if isinstance(x, list):
            vs = [v.strip() for v in x]
            return '; '.join(vs)
        if isinstance(x, str):
            vs = re.sub("'", "", x.strip('[]')).split(',')
            vs = [v.strip() for v in vs]
            return '; '.join(vs)
        else:
            return None
    df_bills['state'] = df_bills['state'].apply(lambda x: x.upper())
    df_bills['subjects'] = df_bills['subjects'].apply(cb_subs)
    df_bills['type'] = df_bills['type'].apply(cb_subs)
    return df_bills


def do_open_states(out_fn):
    apikey = os.getenv("OPEN_STATES_API_KEY")

    q = "climate change"

    url = "https://openstates.org/api/v1/bills/?q={}&apikey={}".format(urllib.parse.quote(q), apikey)
    df_bills = pd.DataFrame(requests.get(url).json())
    out = cleanup_bills(df_bills)
    out.to_csv(out_fn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('out_fn', type=str,
                        help='Filename of excel file to write, e.g., "os.csv"')
    args = parser.parse_args()
    do_open_states(args.out_fn)
