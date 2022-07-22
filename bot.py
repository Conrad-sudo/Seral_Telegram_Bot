''''
RESOURCES: https://www.geeksforgeeks.org/create-a-telegram-bot-using-python/
'''

import ccxt as cx
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters




#Set the telegram token
#telegram_token_old="<Your_telegram_token>"



group_chat_id='<your_chat_ID>'


global job_handler
on=False

#Create a whitelist to restrict access to bot
user_whitelist=[]

#Set up the connection with the bot API
updater = Updater(telegram_token,use_context=True)

job = updater.job_queue


#Step 1: defining functions for the bot
def start(update: Update, context: CallbackContext):
	update.message.reply_text('Başlatmak için "başla <dakika>" yazın \nDurdurmak için "/dur" yazın\nYardım için "/yardim" yazın')




def help(update: Update, context: CallbackContext):
	update.message.reply_text('Başlatmak için "başla <dakika>" yazın.\nÖrnek: "başla 15"  ')




# get balances of Coinbase wallets
def get_coinbase():

    key = '<Your_key>'
    secret = 'Your_secret'
    passphrase = '<Your_pasphrase>'

    coinbase = cx.coinbasepro({
        "apiKey": key,
        "secret": secret,
        "password": passphrase,
        "enableRateLimit": True
    })

    balances = coinbase.fetch_balance()['info']

    for coin in balances:
        if coin['currency']=='USD':
            usd_total=int(float(coin['balance']))
        elif coin['currency']=='USDC':
            usdc_total = int(float(coin['balance']))
        elif coin['currency'] == 'USDT':
            usdt_total = int(float(coin['balance']))



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

    output = f'***Coinbase Account***\nUSD: {usd_formated}\nUSDT: {usdt_formated}\nUSDC: {usdc_formated}'

    book= {'USD':usd_total,'USDT':usdt_total,'USDC': usdc_total, 'message':output}
    return book




def update_ftx_addresses(subaccount):

    

    elif subaccount == 'main':
        # fetch the subaccount
        ftx_subaccount = cx.ftx({
            'apiKey': api_key,
            'secret': api_sec,
            'enableRateLimit': True,
            #'headers': {'FTX-SUBACCOUNT': subaccount},  # uncomment line if using subaccount
        })

    

    return balances





# get balances of FTX wallets WORKING
def get_ftx():
	

    api_key = '<Your_key>'
    api_sec = 'Your_secret'

        # fetch the subaccount
    ftx = cx.ftx({
            'apiKey': api_key,
            'secret': api_sec,
            'enableRateLimit': True,
            #'headers': {'FTX-SUBACCOUNT': subaccount},  # uncomment line if using subaccount
        })
	
    
	
    #Declare the book 
    main_book={}
   
    #Declare the total variables
    usdt_total = 0
    usd_total = 0
    usdc_total = 0



    #Seperate the accounts
    #get the balances of all coins in the account
    main_account = ftx.fetch_balance()['info']['result']
    

    #Filter out the desired coins in each account and add the to the accoun books
    for wallet in main_account:
        if 'USD' == wallet['coin']  or 'USDT' == wallet['coin'] or 'USDC' == wallet['coin'] :
            wallet_name = wallet['coin']
            total = wallet['total']
            main_book.update({wallet_name:total})
    #main= f'***Main Account***\nUSD: {main_book["USD"]} \nUSDT: {main_book["USDT"]} \nUSDC: {main_book["USDC"]} '


    #Iterate through each book and calculate total
    for pair in main_book:
        if pair == 'USD':
            usd_total+=int(float(main_book[pair]))
        elif pair == 'USDT':
            usdt_total +=int(float(main_book[pair]))
        elif pair == 'USDC':
            usdc_total += int(float(main_book[pair]))



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

   

    usd_formated = '{0:,}'.format(round(usd_total, usd_power))
    usdt_formated = '{0:,}'.format(round(usdt_total, usdt_power))
    usdc_formated = '{0:,}'.format(round(usdc_total, usdc_power))

   


    output = f'***FTX Account***\nUSD: {usd_formated}\nUSDT: {usdt_formated}\nUSDC: {usdc_formated}\n**Yedek**\nUSD:{yedek_usd_formated}\nUSDT:{yedek_usdt_formated}\nUSDC:{yedek_usdc_formated}'

    book= {'USD':usd_total,'USDT':usdt_total,'USDC': usdc_total, 'message':output,'yedek':yedek_book_mock}
    return book




# get balances for Kraken W
def get_kraken():
    book={}

    kraken = cx.kraken({
        'apiKey': "<your_Key>",
        'secret': "Your_secret",
        'verbose': False,  # switch it to False if you don't want the HTTP log
    })

    balances = kraken.fetch_balance()['info']['result']
    for pair in balances:
        if 'USD' in pair:
            book.update({pair: balances[pair]})

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



    output = f'***Kraken Account***\nstaked USD: {usdm_formated}\nspot USD: {zusd_formated}\nUSDT: {usdt_formated}\nUSDC: {usdc_formated}'

    book = {'USD': usd_total, 'USDT': usdt_total, 'USDC': usdc_total, 'message': output}

    return book




# get balances for bitfinex
def get_bitfinex():
    bitfinex_book = {}

    bitfinex = cx.bitfinex({
        'apiKey': '<Your_Key>',
        'secret': 'Your_Secret',
    })

    wallets = bitfinex.fetch_balance()['info']

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
    output = f'***Bitfinex Account***\nexchange USD:{exchange_usd_formated}\nfunding USD:{funding_usd_formated}\nUSDT:{exchange_usdt_formated}'

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


    context.bot.send_message(text=f'{total_output}\n\n{ftx["message"]}\n\n{kraken["message"]}\n\n{coinbase["message"]}\n\n{bitfinex["message"]}', chat_id=group_chat_id)
    #update.message.reply_text(f'{ftx["message"]}\n\n{kraken["message"]}\n\n{coinbase["message"]}\n\n{total_output}')



def init(update, context:CallbackContext):


    user_id= update.message.chat_id
    context.bot.send_message(text=user_id, chat_id=group_chat_id)
    global on
    global job_handler

    if user_id in user_whitelist and on == False:

        user_input = update.message.text

        try:
            if 'start' in user_input:
                interval = int(float(user_input.split('start')[1]))
            else:
                interval = int(float(user_input.split('start')[1]))
            seconds = interval * 60
            job_handler = job.run_repeating( get_balances, interval=seconds, first=2)
            update.message.reply_text(f'Messages will be send every {interval} minute(s) ')
            on=True

        except (ValueError, IndexError):
            update.message.reply_text('Please enter <minute>" ')

    elif user_id in user_whitelist and on == True:
        update.message.reply_text(f'Messages have already been started.\n First write "/pause"')

    else:
        update.message.reply_text(' Sınırlı erişim ')




def pause(update, context:CallbackContext):
    user_id = update.message.chat_id
    global job_handler
    global on
    if user_id in user_whitelist and on == True:

        job_handler.enabled=False
        update.message.reply_text(' Messages have been pasued ')
        on=False

    else:
        update.message.reply_text(' Restricted access ')



def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry I can't recognize you , you said '%s'" % update.message.text)



def unknown(update: Update, context: CallbackContext):
    update.message.reply_text( "Sorry '%s' is not a valid command" % update.message.text)




#Step 2: Adding the Handlers to handle our messages and commands
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('pause', pause))
updater.dispatcher.add_handler(CommandHandler('help', help))

updater.dispatcher.add_handler(MessageHandler(Filters.text, init))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
# Filters out unknown commands
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))


#Step 3: Run the bot

updater.start_polling()
updater.idle()
