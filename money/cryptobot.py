from aiocryptopay import AioCryptoPay, Networks
from user_data import CR_TOKEN

class CryptoPay:
    def __init__(self):
        self.crypto = None

    async def initialize(self):
        self.crypto = AioCryptoPay(token=CR_TOKEN, network=Networks.MAIN_NET)
        print('cryptobot init')

    async def cleanup(self):
        await self.crypto.close()
        print('cryptobot off')

    async def get_my_info(self):
        responce = await self.crypto.get_me()
        data = responce.json()
        return data
    
    async def get_my_balance(self):
        responce = await self.crypto.get_balance()
        data = responce
        return data
    
    async def get_invoice(self, sum):
        invoice = await self.crypto.create_invoice(asset="USDT", amount=sum)
        data = invoice
        return data
    
    async def get_invoice_data(self, id):
        data = await self.crypto.get_invoices(invoice_ids=id)
        return data
