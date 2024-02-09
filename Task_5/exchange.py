import aiohttp
import asyncio
import json
from datetime import datetime, timedelta
import sys

async def get_exchange_rate(date):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date.strftime('%d.%m.%Y')}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.text()
                else:
                    print(f"Error status: {resp.status} for {url}")
                    
            return json.loads(data)
        except aiohttp.client_exceptions.ClientConnectorError as err:
            print(f'Connection error: {url}', str(err))
            
    
    

def process_data(data):
    date = data['date']
    rates = data['exchangeRate']
    result = {}
    for rate in rates:
        if 'currency' in rate and rate['currency'] in ['EUR', 'USD']:
            result[rate['currency']] = {
                'sale': rate['saleRate'],
                'purchase': rate['purchaseRateNB']
            }
    return {date: result}

async def main(days):
    
    if days > 1:
        if days > 10:
            print('Reached max amount of days')
            days = 10  # Default max days
    else:
        days = 1  # Default 
    tasks = []
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        tasks.append(get_exchange_rate(date))
    results = await asyncio.gather(*tasks)
    try:
        for result in results:
            print(process_data(result))
    except TypeError as e:
        print(e)
        


if __name__ == "__main__":
    days = int(sys.argv[1])
    asyncio.run(main(days))
