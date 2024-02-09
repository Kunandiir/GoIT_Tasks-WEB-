import asyncio
import logging
import websockets
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
import exchange
import aiohttp
import json
from datetime import datetime, timedelta

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

async def start_exchange(days):
    
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
        return [process_data(result) for result in results]
    except TypeError as e:
        print(e)
        
logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            for client in self.clients:
                if client != ws:
                    split_message = message.split()
                    if split_message[0] == 'exchange' and len(split_message) > 1:
                        days = int(split_message[1])  
                        results = await start_exchange(days)  # Use 'await' to call the async function
                        
                        result = ','.join(str(result) for result in results) 
                        await client.send(result)
                    await client.send(f"{ws.remote_address}: {message}")


async def main():
    server = Server()

    async with websockets.serve(server.ws_handler, "localhost", 8765) as server:
        await server.server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown")
