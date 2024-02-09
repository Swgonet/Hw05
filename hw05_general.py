import asyncio
import requests
import platform
import aiohttp
import sys
import json
from datetime import datetime, timedelta


async def get_days_list():
    args = sys.argv
    if len(args) >= 2:
        days = int(args[1])
    else:
        print('you should write number like 2')
        return None
    current_day = datetime.now()
    days_list = []
    for d in range(1, days+1):
        past_day = current_day - timedelta(days=d, weeks=104)
        days_list.append(datetime.strftime(past_day, '%d.%m.%Y'))
    return days_list

def get_data(url: str):
    response = requests.get(url=url)
    print(response.status_code)
    if response.status_code == 200:
        return response.json()
    


async def get_data_async(url, day):

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:

            print("Status:", response.status)
            dict_rate = {}
            dict_rate[day]={}
            data = await response.json()
            exchangeRate = data.get('exchangeRate')
            for rate in exchangeRate:
                currency = rate.get('currency')
                if currency == 'USD':
                    dict_rate[day]['USD']={
        'sale': rate.get('saleRate'),
        'purchase': rate.get('purchaseRate')
      }
                elif currency == 'EUR':
                    dict_rate[day]['EUR']={
        'sale': rate.get('saleRate'),
        'purchase': rate.get('purchaseRate')
      }
    return dict_rate
                


async def main():
    days_list = await get_days_list()
    if days_list is None:
        return
    exchange_rate = []
    for day in days_list:
        url = f'https://api.privatbank.ua/p24api/exchange_rates?date={day}'
        dict_rate = await get_data_async(url, day)
        exchange_rate.append(dict_rate)
    with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(exchange_rate, f, ensure_ascii=False, indent=4)
    return exchange_rate

if __name__ == "__main__":
    if platform.system() == 'Windows':
        result = asyncio.run(main())
        print(result)
        # result = main()
        # print(result)
        # url = 'https://api.privatbank.ua/p24api/exchange_rates?date=09.02.2024'
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        # asyncio.run(get_data_async(url))
        # result = get_data(url)
        # print(result)