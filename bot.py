import logging
from aiogram import Bot, Dispatcher, executor, types
from parse import get_btc_price, get_dollar_price, get_eth_xmr_zec_price

# Для клавиатуры
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = ''
# Задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

WALLETS = { # список валют
    'BTC':'Bitcoin',
    'ETH':'Ethereum',
    'XMR':'Monero',
    'ZEC':'Zcash',
    'USD':'Dollar',
}
# Создаем клавиатуру
kb = InlineKeyboardMarkup()

for key in WALLETS:
    kb.add(InlineKeyboardButton(WALLETS[key], callback_data=key))

# Команды
@dp.message_handler(commands=['start', 'currencies'])
async def start_message(message: types.Message):
    await message.reply('Курс какой валюты хотите узнать?', reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data in WALLETS)
async def process_callback_wallets(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    wal = callback_query.data
    if wal == 'USD':
        price = get_dollar_price()
        response = 'USD: \n {0}€ \n{1}₽'.format(price['EUR'], price['RUB'])
    elif wal == 'BTC':
        price = get_btc_price()      
        USD = price['USD']
        EUR = price['EUR']
        RUB = round(price['USD'] * get_dollar_price()['RUB'],2)
        response = '{0}: \n {1}$ \n {2}€ \n{3}₽'.format(WALLETS[wal],USD, EUR, RUB)
    else:
        price = get_eth_xmr_zec_price()
        USD = price[wal]
        USD_curse = get_dollar_price()
        EUR = round(USD_curse['EUR'] * USD,2)
        RUB = round(USD_curse['RUB'] * USD,2)
        response = '{0}: \n {1}$ \n {2}€ \n{3}₽'.format(WALLETS[wal],USD, EUR, RUB)

    await bot.send_message(callback_query.from_user.id, response)
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
