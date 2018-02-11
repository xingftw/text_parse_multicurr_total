# encoding: utf-8

import sys
# from workflow import Workflow, ICON_WEB, ICON_ERROR, web
# import string
import coinmarketcap

# USD 0.00  EUR 254.60 BTC 0.03087498  XRP 0.00000000 LTC 0.00000000  ETH 0.30000000 BCH 0.00000000

def convert_to(curr, value, to_curr="usd"):
    if lower(curr) == to_curr:
        return (curr,value)
    else:
        coinmarketcap = Market()
        json = coinmarketcap.ticker(curr, limit = 3, convert = to_curr)
        print(json)
    return (curr, to_curr_value)

def parse_text(curr_str):
    # sting.replace(curr_str, "  ", "\n")
    curr_list = curr_str.split("  ")
    for curr in curr_list:
        kv_curr = curr.split(" ")
        convert_to_usd()

def format_strings_from_quote(ticker, quote_data):
    data = quote_data["RAW"][ticker.upper()]["USD"]
    price = "{:,.2f}".format(data["PRICE"])
    high = "{:,.2f}".format(data["HIGH24HOUR"])
    low = "{:,.2f}".format(data["LOW24HOUR"])
    change = "{:,.2f}".format(data["CHANGEPCT24HOUR"])
    formatted = {}
    formatted['title'] = ticker.upper() + ': $' + price + ' (' + change + '%)'
    formatted['subtitle'] = '24hr High: $' + high + ' 24hr low $' + low
    return formatted


def main(wf):
    # Get query from Alfred
    if len(wf.args):
        query = wf.args[0]
    else:
        query = None

    if query:
        url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + \
            query.upper() + '&tsyms=USD'
        r = web.get(url)
        # throw an error if request failed
        # Workflow will catch this and show it to the user
        r.raise_for_status()
        result = r.json()
        try:
            formatted = format_strings_from_quote(query, result)
            wf.add_item(title=formatted['title'],
                        subtitle=formatted['subtitle'],
                        arg='https://www.cryptocompare.com/coins/' + query + '/overview/USD',
                        valid=True,
                        icon=ICON_WEB)
        except:
            wf.add_item(title='Couldn\'t find a quote for that symbol.',
                        subtitle='Please try again.',
                        icon=ICON_ERROR)
    else:
        url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,LTC,BCH&tsyms=USD'
        r = web.get(url)
        # throw an error if request failed
        # Workflow will catch this and show it to the user
        r.raise_for_status()
        result = r.json()
        formatted = format_strings_from_quote('BTC', result)
        wf.add_item(title=formatted['title'],
                    subtitle=formatted['subtitle'],
                    arg='https://www.cryptocompare.com/',
                    valid=True,
                    icon='icon/btc.png')

        formatted = format_strings_from_quote('ETH', result)
        wf.add_item(title=formatted['title'],
                    subtitle=formatted['subtitle'],
                    arg='https://www.cryptocompare.com/',
                    valid=True,
                    icon='icon/eth.png')

        formatted = format_strings_from_quote('LTC', result)
        wf.add_item(title=formatted['title'],
                    subtitle=formatted['subtitle'],
                    arg='https://www.cryptocompare.com/',
                    valid=True,
                    icon='icon/ltc.png')

        formatted = format_strings_from_quote('BCH', result)
        wf.add_item(title=formatted['title'],
                    subtitle=formatted['subtitle'],
                    arg='https://www.cryptocompare.com/',
                    valid=True,
                    icon='icon/bch.png')

    # Send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))

tot_curr_value = convert_to("eur", 254.60)
print(tot_curr_value)
