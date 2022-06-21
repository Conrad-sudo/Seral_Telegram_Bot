''''
 a Telegram bot to track the balances of all the spot accounts on the different exchanges
RESOURCES: https://www.geeksforgeeks.org/create-a-telegram-bot-using-python/
'''
import os
import json
from requests import post,Session,Request
import time
import urllib.parse
import hashlib
import hmac
import base64
import coinbasepro as cb
from bitfinex import ClientV1 as Client

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters


#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Set the port number to listen in for the webhook
PORT = int(os.environ.get('PORT', 443))

#Set the telegram token
#telegram_token_old="5242786798:AAHKk0kaOH20Gjm9n9XuvU6PeyIa2Yi9qqk"
#telegram_token='5443455569:AAGBppH5PrjRMh5leSglLhwvuUy3Un3PrzM'
telegram_token=os.getenv('BOTAPIKEY')

test_group_chat_id='-651490861'
seral_hesablar_chat_id='-716644286'

global job_handler

user_whitelist=[850770583,426124495]

#Set up the connection with the bot API
updater = Updater(telegram_token,use_context=True)

job = updater.job_queue
job2 = updater.job_queue

#Step 1: defining functions for the bot
def start(update: Update, context: CallbackContext):
	update.message.reply_text('Başlatmak için "başla <dakika>" yazın \nDurdurmak için "/dur" yazın\nYardım için "/yardim" yazın')




def help(update: Update, context: CallbackContext):
	update.message.reply_text('Başlatmak için "başla <dakika>" yazın.\nÖrnek: "başla 15"  ')




# get balances of Coinbase wallets
def get_coinbase():

    key = '092ee44fa1ac029b9cbc2cd48b8fc29a'
    secret = 'fixJ49IzJJsHNkpdwNx/qNpdI6rCyuCVXM8TGlE0frLyidoszSKtS8luUm1mqqknD2gxsPV7cwbRm9N14uPqFQ=='
    passphrase = 'zz0uurpv3v'

    auth_client = cb.AuthenticatedClient(key,secret,passphrase)
    usd_id = 'befd9f09-ec2d-43d8-ba29-faa3f81ffc12'
    usdc_id = 'f8c40622-7ca9-4b5f-ab2e-aae64d81f979'
    usdt_id = '8bb7272c-441d-40aa-b39d-9f29afd93b9d'

    usd_total = int(float(auth_client.get_account(account_id=usd_id)['balance']))
    usdc_total = int(float(auth_client.get_account(account_id=usdc_id)['balance']))
    usdt_total = int(float(auth_client.get_account(account_id=usdt_id)['balance']))


    #Get the powers to round off the numbers

    if usdt_total % 1 == usdt_total:
        usdt_power = 1
    if usdt_total % 10 < usdt_total:
        usdt_power = 0
    if usdt_total % 100 < usdt_total:
        usdt_power = -1
    if usdt_total % 1000 < usdt_total:
        usdt_power = -2
    if usdt_total % 10000 < usdt_total:
        usdt_power = -3
    if usdt_total % 100000 < usdt_total:
        usdt_power = -4
    if usdt_total % 1000000 < usdt_total:
        usdt_power = -5

    if usd_total % 1 == usd_total:
        usd_power = 1
    if usd_total % 10 < usd_total:
        usd_power = 0
    if usd_total % 100 < usd_total:
        usd_power = -1
    if usd_total % 1000 < usd_total:
        usd_power = -2
    if usd_total % 10000 < usd_total:
        usd_power = -3
    if usd_total % 100000 < usd_total:
        usd_power = -4
    if usd_total % 1000000 < usd_total:
        usd_power = -5

    if usdc_total % 1 == usdc_total:
        usdc_power = 1
    if usdc_total % 10 < usdc_total:
        usdc_power = 0
    if usdc_total % 100 < usdc_total:
        usdc_power = -1
    if usdc_total % 1000 < usdc_total:
        usdc_power = -2
    if usdc_total % 10000 < usdc_total:
        usdc_power = -3
    if usdc_total % 100000 < usdc_total:
        usdc_power = -4
    if usdc_total % 1000000 < usdc_total:
        usdc_power = -5

    usd_formated='{0:,}'.format(round(usd_total,usd_power))
    usdt_formated='{0:,}'.format(round(usdt_total,usdt_power))
    usdc_formated='{0:,}'.format(round(usdc_total,usdc_power))

    output = f'***Coinbase Hesabı***\nUSD: {usd_formated}\nUSDT: {usdt_formated}\nUSDC: {usdc_formated}'

    book= {'USD':usd_total,'USDT':usdt_total,'USDC': usdc_total, 'message':output}
    return book




# get balances of FTX wallets WORKING
def get_ftx():

    api_key= 'jM3JLiq6uYd-vBC2zr17Y5vdzibatg92lCKXPaGU'
    api_sec= '2aXxPQ38x0qacwMkTNJxChIBQmdGL-an3I4XUIfb'
    s = Session()

    #Declare the books for each account
    main_book={}
    btc_book={}
    eth_book={}
    sol_book={}
    tether_book={}
    yedek_book={}

    #Declare the total variables
    usdt_total = 0
    usd_total = 0
    usdc_total = 0



    #Make API request
    ts = int(time.time() * 1000)
    request = Request('GET', 'https://ftx.com/api/wallet/all_balances')
    prepared = request.prepare()
    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'
    if prepared.body:
        signature_payload += prepared.body
    signature_payload = signature_payload.encode()
    signature = hmac.new(api_sec.encode(), signature_payload, 'sha256').hexdigest()

    prepared.headers['FTX-KEY'] = api_key
    prepared.headers['FTX-SIGN'] = signature
    prepared.headers['FTX-TS'] = str(ts)
    #Get the object
    response = s.send(prepared)
    #Convert object to json
    obj = json.loads(response.content)

    accounts= obj['result']

    #Seperate the accounts
    main_account= accounts['main']
    btc_account=accounts['BTC']
    eth_account=accounts['ETH']
    sol_account=accounts['SOL']
    tether_account=accounts['Tether']
    yedek_account=accounts['Yedek']

    #Filter out the desired coins in each account and add the to the accoun books
    for wallet in main_account:
        if 'USD' == wallet['coin']  or 'USDT' == wallet['coin'] or 'USDC' == wallet['coin'] :
            wallet_name = wallet['coin']
            total = wallet['total']
            main_book.update({wallet_name:total})
    #main= f'***Main Account***\nUSD: {main_book["USD"]} \nUSDT: {main_book["USDT"]} \nUSDC: {main_book["USDC"]} '

    for wallet in btc_account:
        if 'USD' == wallet['coin'] or 'USDT' == wallet['coin'] or 'USDC' == wallet['coin']:
            wallet_name = wallet['coin']
            total = wallet['total']
            btc_book.update({wallet_name: total})
    #btc = f'***BTC Accounts***\nUSD: {btc_book["USD"]} \nUSDT: {btc_book["USDT"]} \nUSDC: {btc_book["USDC"]} '

    for wallet in eth_account:
        if 'USD' == wallet['coin'] or 'USDT' == wallet['coin'] or 'USDC' == wallet['coin']:
            wallet_name = wallet['coin']
            total = wallet['total']
            eth_book.update({wallet_name: total})
    #eth = f'***ETH Accounts***\nUSD: {eth_book["USD"]} \nUSDT: {eth_book["USDT"]} \nUSDC: {eth_book["USDC"]} '

    for wallet in sol_account:
        if 'USD' == wallet['coin'] or 'USDT' == wallet['coin'] or 'USDC' == wallet['coin']:
            wallet_name = wallet['coin']
            total = wallet['total']
            sol_book.update({wallet_name: total})
    #sol = f'***SOL Accounts***\nUSD: {sol_book["USD"]} \nUSDT: {sol_book["USDT"]} \nUSDC: {sol_book["USDC"]} '

    for wallet in tether_account:
        if 'USD' == wallet['coin'] or 'USDT' == wallet['coin'] or 'USDC' == wallet['coin']:
            wallet_name = wallet['coin']
            total = wallet['total']
            tether_book.update({wallet_name: total})
    #tether = f'***Tether Accounts***\nUSD: {tether_book["USD"]} \nUSDT: {tether_book["USDT"]} \nUSDC: {tether_book["USDC"]} '

    for wallet in yedek_account:
        if 'USD' == wallet['coin'] or 'USDT' == wallet['coin'] or 'USDC' == wallet['coin']:
            wallet_name = wallet['coin']
            total = wallet['total']
            yedek_book.update({wallet_name: total})



    #Iterate through each book and calculate total
    for pair in main_book:
        if pair == 'USD':
            usd_total+=int(float(main_book[pair]))
        elif pair == 'USDT':
            usdt_total +=int(float(main_book[pair]))
        elif pair == 'USDC':
            usdc_total += int(float(main_book[pair]))

    for pair in btc_book:
        if pair == 'USD':
            usd_total+=int(float(btc_book[pair]))
        elif pair == 'USDT':
            usdt_total +=int(float(btc_book[pair]))
        elif pair == 'USDC':
            usdc_total += int(float(btc_book[pair]))

    for pair in eth_book:
        if pair == 'USD':
            usd_total+=int(float(eth_book[pair]))
        elif pair == 'USDT':
            usdt_total +=int(float(eth_book[pair]))
        elif pair == 'USDC':
            usdc_total += int(float(eth_book[pair]))

    for pair in sol_book:
        if pair == 'USD':
            usd_total+=int(float(sol_book[pair]))
        elif pair == 'USDT':
            usdt_total +=int(float(sol_book[pair]))
        elif pair == 'USDC':
            usdc_total += int(float(sol_book[pair]))

    for pair in tether_book:
        if pair == 'USD':
            usd_total+=int(float(tether_book[pair]))
        elif pair == 'USDT':
            usdt_total +=int(float(tether_book[pair]))
        elif pair == 'USDC':
            usdc_total += int(float(tether_book[pair]))

    yedek_book_mock = {}
    for pair in yedek_book:
        if pair == 'USD':
            yedek_book_mock.update({pair: int(float(yedek_book[pair]))})
        elif pair == 'USDT':
            yedek_book_mock.update({pair: int(float(yedek_book[pair]))})
        elif pair == 'USDC':
            yedek_book_mock.update({pair: int(float(yedek_book[pair]))})

    #Iterate specifically for Yedek account

    for pair in yedek_book:
        if pair == 'USD':
            yedek_usd_total=int(float(yedek_book[pair]))
        elif pair == 'USDT':
            yedek_usdt_total =int(float(yedek_book[pair]))
        elif pair == 'USDC':
            yedek_usdc_total = int(float(yedek_book[pair]))



    #Get the powers to round off the numbers

    if usdt_total % 1 == usdt_total:
        usdt_power = 1
    if usdt_total % 10 < usdt_total:
        usdt_power = 0
    if usdt_total % 100 < usdt_total:
        usdt_power = -1
    if usdt_total % 1000 < usdt_total:
        usdt_power = -2
    if usdt_total % 10000 < usdt_total:
        usdt_power = -3
    if usdt_total % 100000 < usdt_total:
        usdt_power = -4
    if usdt_total % 1000000 < usdt_total:
        usdt_power = -5


    if usd_total % 1 == usd_total:
        usd_power = 1
    if usd_total % 10 < usd_total:
        usd_power = 0
    if usd_total % 100 < usd_total:
        usd_power = -1
    if usd_total % 1000 < usd_total:
        usd_power = -2
    if usd_total % 10000 < usd_total:
        usd_power = -3
    if usd_total % 100000 < usd_total:
        usd_power = -4
    if usd_total % 1000000 < usd_total:
        usd_power = -5


    if usdc_total % 1 == usdc_total:
        usdc_power = 1
    if usdc_total % 10 < usdc_total:
        usdc_power = 0
    if usdc_total % 100 < usdc_total:
        usdc_power = -1
    if usdc_total % 1000 < usdc_total:
        usdc_power = -2
    if usdc_total % 10000 < usdc_total:
        usdc_power = -3
    if usdc_total % 100000 < usdc_total:
        usdc_power = -4
    if usdc_total % 1000000 < usdc_total:
        usdc_power = -5

    # Get powers just for YEDEk
    if yedek_usdt_total % 1 == yedek_usdt_total:
        yedek_usdt_power = 1
    if yedek_usdt_total % 10 < yedek_usdt_total:
        yedek_usdt_power = 0
    if yedek_usdt_total % 100 < yedek_usdt_total:
        yedek_usdt_power = -1
    if yedek_usdt_total % 1000 < yedek_usdt_total:
        yedek_usdt_power = -2
    if yedek_usdt_total % 10000 < yedek_usdt_total:
        yedek_usdt_power = -3
    if yedek_usdt_total % 100000 < yedek_usdt_total:
        yedek_usdt_power = -4
    if yedek_usdt_total % 1000000 < yedek_usdt_total:
        yedek_usdt_power = -5

    if yedek_usd_total % 1 == yedek_usd_total:
        yedek_usd_power = 1
    if yedek_usd_total % 10 < yedek_usd_total:
        yedek_usd_power = 0
    if yedek_usd_total % 100 < yedek_usd_total:
        yedek_usd_power = -1
    if yedek_usd_total % 1000 < yedek_usd_total:
        yedek_usd_power = -2
    if yedek_usd_total % 10000 < yedek_usd_total:
        yedek_usd_power = -3
    if yedek_usd_total % 100000 < yedek_usd_total:
        yedek_usd_power = -4
    if yedek_usd_total % 1000000 < yedek_usd_total:
        yedek_usd_power = -5

    if yedek_usdc_total % 1 == yedek_usdc_total:
        yedek_usdc_power = 1
    if yedek_usdc_total % 10 < yedek_usdc_total:
        yedek_usdc_power = 0
    if yedek_usdc_total % 100 < yedek_usdc_total:
        yedek_usdc_power = -1
    if yedek_usdc_total % 1000 < yedek_usdc_total:
        yedek_usdc_power = -2
    if yedek_usdc_total % 10000 < yedek_usdc_total:
        yedek_usdc_power = -3
    if yedek_usdc_total % 100000 < yedek_usdc_total:
        yedek_usdc_power = -4
    if yedek_usdc_total % 1000000 < yedek_usdc_total:
        yedek_usdc_power = -5



    usd_formated = '{0:,}'.format(round(usd_total, usd_power))
    usdt_formated = '{0:,}'.format(round(usdt_total, usdt_power))
    usdc_formated = '{0:,}'.format(round(usdc_total, usdc_power))

    yedek_usd_formated = '{0:,}'.format(round(yedek_usd_total, yedek_usd_power))
    yedek_usdt_formated = '{0:,}'.format(round(yedek_usdt_total, yedek_usdt_power))
    yedek_usdc_formated = '{0:,}'.format(round(yedek_usdc_total, yedek_usdc_power))


    output = f'***FTX Hesabı***\nUSD: {usd_formated}\nUSDT: {usdt_formated}\nUSDC: {usdc_formated}\n**Yedek**\nUSD:{yedek_usd_formated}\nUSDT:{yedek_usdt_formated}\nUSDC:{yedek_usdc_formated}'

    book= {'USD':usd_total,'USDT':usdt_total,'USDC': usdc_total, 'message':output,'yedek':yedek_book_mock}
    return book



def get_kraken_signature(urlpath, data, secret):

    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()



def kraken_request(uri_path, data, api_key, api_sec):
    api_url = "https://api.kraken.com"
    headers = {}
    headers['API-Key'] = api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)
    req = post((api_url + uri_path), headers=headers, data=data)
    return req



# get balances for Kraken WORKING
def get_kraken():
    book={}
    api_key = 'XcClvhb24aLmg0brDebRQJEF0Gy9pZix8/XQbd1kcMvc8cAgHypdIpUi'
    api_sec = 'yKShvSpLCNZ7OwCybWhgHNPyvvvpOocSZ9XokZCPBm9VaNadXfw0HBOY8QH7pqdzfFgOM6JjHzB8jyprl+PuVg=='
    resp = kraken_request('/0/private/Balance', {"nonce": str(int(1000 * time.time()))}, api_key, api_sec)
    resp=json.loads(resp.content)

    for pair in resp['result']:
        if 'USD' in pair:
            book.update({pair:resp['result'][pair]})

    usd_total = int(float(book["ZUSD"]))+int(float(book["USD.M"]))
    zusd_total=int(float(book["ZUSD"]))
    usdm_total=int(float(book["USD.M"]))
    usdc_total= int(float(book["USDC"]))
    usdt_total=int(float(book["USDT"]))



    # Get the powers to round off the numbers

    if usdt_total % 1 == usdt_total:
        usdt_power = 1
    if usdt_total % 10 < usdt_total:
        usdt_power = 0
    if usdt_total % 100 < usdt_total:
        usdt_power = -1
    if usdt_total % 1000 < usdt_total:
        usdt_power = -2
    if usdt_total % 10000 < usdt_total:
        usdt_power = -3
    if usdt_total % 100000 < usdt_total:
        usdt_power = -4
    if usdt_total % 1000000 < usdt_total:
        usdt_power = -5

    if usdm_total % 1 == usdm_total:
        usdm_power = 1
    if usdm_total % 10 < usdm_total:
        usdm_power = 0
    if usdm_total % 100 < usdm_total:
        usdm_power = -1
    if usdm_total % 1000 < usdm_total:
        usdm_power = -2
    if usdm_total % 10000 < usdm_total:
        usdm_power = -3
    if usdm_total % 100000 < usdm_total:
        usdm_power = -4
    if usdm_total % 1000000 < usdm_total:
        usdm_power = -5

    if zusd_total % 1 == zusd_total:
        zusd_power = 1
    if zusd_total % 10 < zusd_total:
        zusd_power = 0
    if zusd_total % 100 < zusd_total:
        zusd_power = -1
    if zusd_total % 1000 < zusd_total:
        zusd_power = -2
    if zusd_total % 10000 < zusd_total:
        zusd_power = -3
    if zusd_total % 100000 < zusd_total:
        zusd_power = -4
    if zusd_total % 1000000 < zusd_total:
        zusd_power = -5


    if usdc_total % 1 == usdc_total:
        usdc_power = 1
    if usdc_total % 10 < usdc_total:
        usdc_power = 0
    if usdc_total % 100 < usdc_total:
        usdc_power = -1
    if usdc_total % 1000 < usdc_total:
        usdc_power = -2
    if usdc_total % 10000 < usdc_total:
        usdc_power = -3
    if usdc_total % 100000 < usdc_total:
        usdc_power = -4
    if usdc_total % 1000000 < usdc_total:
        usdc_power = -5

    usdm_formated = '{0:,}'.format(round(usdm_total, usdm_power))
    zusd_formated = '{0:,}'.format(round(zusd_total, zusd_power))
    usdt_formated = '{0:,}'.format(round(usdt_total, usdt_power))
    usdc_formated = '{0:,}'.format(round(usdc_total, usdc_power))



    output = f'***Kraken Hesab***\nstaked USD: {usdm_formated}\nspot USD: {zusd_formated}\nUSDT: {usdt_formated}\nUSDC: {usdc_formated}'

    book = {'USD': usd_total, 'USDT': usdt_total, 'USDC': usdc_total, 'message': output}

    return book




# get balances for bitfinex
def get_bitfinex():
    bitfinex_book = {}
    API_KEY = 'yWN7wjCI21sTPe6HYsCqfZ6TyKPq89GHdjmoNZ9m4Zs'
    API_SECRET = 'Xn6maslKlmmFqxEmo41gT49TvpSHEIe0h8wYU9LdhSn'

    client = Client(key=API_KEY, secret=API_SECRET, nonce_multiplier=1.0)

    wallets = client.balances()

    for wallet in wallets:

        if wallet['currency'] == 'usd' and wallet['type'] == 'deposit':
            funding_usd = int(float(wallet['amount']))
        elif wallet['currency'] == 'usd' and wallet['type'] == 'exchange':
            exchange_usd = int(float(wallet['amount']))
        elif wallet['currency'] == 'ust' and wallet['type'] == 'exchange':
            exchange_usdt = int(float(wallet['amount']))

    usd_total = exchange_usd + funding_usd

    exchange_usdt_power=0
    exchange_usd_power=0
    funding_usd_power=0


    # Get the rounding off powers for the amounts
    if exchange_usd % 1 == exchange_usd:
        exchange_usd_power = 1
    if exchange_usd % 10 < exchange_usd:
        exchange_usd_power = 0
    if exchange_usd % 100 < exchange_usd:
        exchange_usd_power = -1
    if exchange_usd % 1000 < exchange_usd:
        exchange_usd_power = -2
    if exchange_usd % 10000 < exchange_usd:
        exchange_usd_power = -3
    if exchange_usd % 100000 < exchange_usd:
        exchange_usd_power = -4
    if exchange_usd % 1000000 < exchange_usd:
        exchange_usd_power = -5

    if exchange_usdt % 1 == exchange_usdt:
        exchange_usdt_power = 1
    if exchange_usdt % 10 < exchange_usdt:
        exchange_usdt_power = 0
    if exchange_usdt % 100 < exchange_usdt:
        exchange_usdt_power = -1
    if exchange_usdt % 1000 < exchange_usdt:
        exchange_usdt_power = -2
    if exchange_usdt % 10000 < exchange_usdt:
        exchange_usdt_power = -3
    if exchange_usdt % 100000 < exchange_usdt:
        exchange_usdt_power = -4
    if exchange_usdt % 1000000 < exchange_usdt:
        exchange_usdt_power = -5



    if funding_usd % 1 == funding_usd:
        funding_usd_power = 1
    if funding_usd % 10 < funding_usd:
        funding_usd_power = 0
    if funding_usd % 100 < funding_usd:
        funding_usd_power = -1
    if funding_usd % 1000 < funding_usd:
        funding_usd_power = -2
    if funding_usd % 10000 < funding_usd:
        funding_usd_power = -3
    if funding_usd % 100000 < funding_usd:
        funding_usd_power = -4
    if funding_usd % 1000000 < funding_usd:
        funding_usd_power = -5





    exchange_usd_formated = '{0:,}'.format(round(exchange_usd, exchange_usd_power))
    exchange_usdt_formated = '{0:,}'.format(round(exchange_usdt, exchange_usdt_power))
    funding_usd_formated = '{0:,}'.format(round(funding_usd, funding_usd_power))
    output = f'***Bitfinex Hesabı***\nexchange USD:{exchange_usd_formated}\nfunding USD:{funding_usd_formated}\nUSDT:{exchange_usdt_formated}'

    # compose the book

    bitfinex_book.update({'USD': usd_total,'USDT':exchange_usdt, 'message': output})

    return bitfinex_book




#Help on job que can be found at https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-JobQueue
def get_balances( context: CallbackContext):



    kraken = get_kraken()
    ftx = get_ftx()
    coinbase = get_coinbase()
    bitfinex = get_bitfinex()


    usd_total = 0
    usdt_total = 0
    usdc_total = 0

    # Loop through each book and add the total
    for wallet in kraken:
        if wallet == 'USD':
            usd_total += kraken[wallet]
        elif wallet == 'USDT':
            usdt_total += kraken[wallet]
        elif wallet == 'USDC':
            usdc_total += kraken[wallet]

    for wallet in ftx:
        if wallet == 'USD':
            usd_total += ftx[wallet]
        elif wallet == 'USDT':
            usdt_total += ftx[wallet]
        elif wallet == 'USDC':
            usdc_total += ftx[wallet]

    for wallet in ftx['yedek']:
        if wallet == 'USD':
            usd_total += ftx['yedek'][wallet]
        elif wallet == 'USDT':
            usdt_total += ftx['yedek'][wallet]
        elif wallet == 'USDC':
            usdc_total += ftx['yedek'][wallet]

    for wallet in coinbase:
        if wallet == 'USD':
            usd_total += coinbase[wallet]
        elif wallet == 'USDT':
            usdt_total += coinbase[wallet]
        elif wallet == 'USDC':
            usdc_total += coinbase[wallet]

    #For bitfinex
    usd_total +=bitfinex['USD']
    usdt_total +=bitfinex['USDT']

    if usdt_total % 1 == usdt_total:
        usdt_power = 1
    if usdt_total % 10 < usdt_total:
        usdt_power = 0
    if usdt_total % 100 < usdt_total:
        usdt_power = -1
    if usdt_total % 1000 < usdt_total:
        usdt_power = -2
    if usdt_total % 10000 < usdt_total:
        usdt_power = -3
    if usdt_total % 100000 < usdt_total:
        usdt_power = -4
    if usdt_total % 1000000 < usdt_total:
        usdt_power = -5

    if usd_total % 1 == usd_total:
        usd_power = 1
    if usd_total % 10 < usd_total:
        usd_power = 0
    if usd_total % 100 < usd_total:
        usd_power = -1
    if usd_total % 1000 < usd_total:
        usd_power = -2
    if usd_total % 10000 < usd_total:
        usd_power = -3
    if usd_total % 100000 < usd_total:
        usd_power = -4
    if usd_total % 1000000 < usd_total:
        usd_power = -5

    if usdc_total % 1 == usdc_total:
        usdc_power = 1
    if usdc_total % 10 < usdc_total:
        usdc_power = 0
    if usdc_total % 100 < usdc_total:
        usdc_power = -1
    if usdc_total % 1000 < usdc_total:
        usdc_power = -2
    if usdc_total % 10000 < usdc_total:
        usdc_power = -3
    if usdc_total % 100000 < usdc_total:
        usdc_power = -4
    if usdc_total % 1000000 < usdc_total:
        usdc_power = -5

    usd_formated = '{0:,}'.format(round(usd_total, usd_power))
    usdt_formated = '{0:,}'.format(round(usdt_total, usdt_power))
    usdc_formated = '{0:,}'.format(round(usdc_total, usdc_power))

    total_output = f'Total USD: {usd_formated}\nTotal USDT: {usdt_formated}\nTotal USDC: {usdc_formated}'


    context.bot.send_message(text=f'{total_output}\n\n{ftx["message"]}\n\n{kraken["message"]}\n\n{coinbase["message"]}\n\n{bitfinex["message"]}', chat_id=test_group_chat_id)
    #update.message.reply_text(f'{ftx["message"]}\n\n{kraken["message"]}\n\n{coinbase["message"]}\n\n{total_output}')



def init(update, context:CallbackContext):


    user_id= update.message.chat_id

    if user_id in user_whitelist:
        global job_handler
        user_input = update.message.text

        try:
            if 'başla' in user_input:
                interval = int(float(user_input.split('başla')[1]))
            else:
                interval = int(float(user_input.split('Başla')[1]))
            seconds = interval * 60
            job_handler = job.run_repeating( get_balances, interval=seconds, first=2)
            update.message.reply_text(f'Mesajlar her {interval} dakika gönderilecek ')

        except (ValueError, IndexError):
            update.message.reply_text('Lütfen "başla <dakika>" yazın')
    else:
        update.message.reply_text(' Sınırlı erişim ')




def pause(update, context:CallbackContext):
    user_id = update.message.chat_id
    global job_handler
    if user_id in user_whitelist:

        job_handler.enabled=False
        update.message.reply_text(' Mesajlaşma durduruldu ')

    else:
        update.message.reply_text(' Sınırlı erişim ')



def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry I can't recognize you , you said '%s'" % update.message.text)



def unknown(update: Update, context: CallbackContext):
    update.message.reply_text( "Sorry '%s' is not a valid command" % update.message.text)




#Step 2: Adding the Handlers to handle our messages and commands
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('dur', pause))
updater.dispatcher.add_handler(CommandHandler('yardim', help))

updater.dispatcher.add_handler(MessageHandler(Filters.text, init))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
# Filters out unknown commands
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))


#Step 3: Run the bot

updater.start_polling()
#updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=telegram_token,webhook_url='https://guarded-dawn-21918.herokuapp.com/' + telegram_token)
updater.idle()