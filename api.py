import requests


class API:
    async def check_supported_currencies():
        result = []
        res = requests.get('https://v6.exchangerate-api.com/v6/26f924a3100b291193b17249/codes').json()
        for i in res['supported_codes']:
            result.append(i[0])
        return result

    async def convert_currency(cur1: str, cur2: str, quantity: int):
        res = requests.get(f'https://v6.exchangerate-api.com/v6/26f924a3100b291193b17249/pair/{cur1}/{cur2}').json()
        res = res['conversion_rate']
        return res * quantity







