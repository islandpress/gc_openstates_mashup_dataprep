"""
This script is for pulling organization name and address data from
the Green Commons and writing it to a spreadsheet.

The script also writes out a spreadsheet for all state names and abbreviations.

For more details about the Green Commons API, see
    https://github.com/greencommons/commons/blob/master/API.md
"""

import requests
import pandas as pd
import argparse
import usaddress
import us


def form_url(host='https://greencommons.net', page=1, per=200):
    return '{}/api/v1/search?q=&filters[resource_types]='\
             'profiles&filters[model_types]=resources&page={}&per={}'.format(
                host, page, per)

def get_num_pages():
    url = form_url()
    r = requests.get(url)
    j = r.json()
    return 1 + int(j['links']['last'].split('&page')[1].split('&')[0].strip('='))


def get_data(verbose=True):
    data = []
    num_pages = get_num_pages()
    for p in range(0, num_pages + 1):
        url = form_url(page=p)
        r = requests.get(url)
        if r.ok:
            data.extend(r.json().get('data'))
        if verbose:
            print("page: {}; data size: {}".format(p, len(data)))
    return data


def filter_data_for_usa(data):
    select = []
    for ind, d in enumerate(data):
        address = d.get('attributes', {}).get('metadata', {}).get('address', '')
        if any(usa in address.lower() for usa in ['u.s.', 'united states']):
            select.append(d)
    return select


def do_greencommons(out_fn):
    data = get_data()
    data = filter_data_for_usa(data)
    select = []
    for d in data:
        select.append(dict(title=d.get('attributes').get('title'),
                           address=d.get('attributes').get('metadata').get('address'),
                           description=d.get('attributes').get('short_content'),
                           url=d.get('attributes').get('resource_url')))
    df = pd.DataFrame(select)
    df['state'] = df['address'].apply(lambda x: {v:k for k,v in usaddress.parse(x)}.get('StateName'))

    state_names = [s.name.lower() for s in us.STATES]
    state_abbrs = [s.abbr.lower() for s in us.STATES]
    def custom_parse(row):
        if row['state'] and row['state'] in state_abbrs:
            return row['state'].upper()
        x = row['address'].lower() + ' ' + row['title'].lower()
        for s in state_names:
            if s in x:
                return us.states.lookup(s).abbr.upper()
        x = x.split()
        for s in state_abbrs:
            if s in x:
                return s.upper()
    df['state'] = df.apply(custom_parse, axis=1)
    df.to_csv(out_fn)


def do_state_lookup(out_fn):
    data = [dict(name=s.name, abbr=s.abbr.upper()) for s in us.STATES]
    df = pd.DataFrame(data)
    df.to_csv(out_fn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('gc_out_fn', type=str,
                        help='Filename of Green Commons excel file to write, e.g., "gc.csv"')
    parser.add_argument('lu_out_fn', type=str,
                        help='Filename of State lookup excel file to write, e.g., "lu.csv"')
    args = parser.parse_args()
    do_greencommons(args.gc_out_fn)
    do_state_lookup(args.lu_out_fn)
