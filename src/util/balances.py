from datetime import datetime, timedelta, timezone
from binance.client import Client, BinanceAPIException
import time
def get_usdt_balance(client_binance,active_operated):
    """
    Consulta o saldo de operador ativo na conta da Binance.
    """
    try:
        account_info = client_binance.get_account()
        for balance in account_info['balances']:
            if balance['asset'] == active_operated:
                 return float(balance['free'])
        return 0.0 
    except Exception as e:
        print(f"Erro ao consultar o saldo {active_operated}: {e}")
        return 0.0
    
def convert_usdt_to_btc(usdt_balance, client_binance, symbol):
    """
    Converte o saldo em symbol(ex:USDT para BTC) usando o preço atual do mercado.
    """
    try:
        # Obter o preço atual do par BTC/USDT
        btc_usdt_price = float(client_binance.get_symbol_ticker(symbol=symbol)["price"])
        print(btc_usdt_price)
        btc_balance = usdt_balance / btc_usdt_price
        return float(btc_balance)
    except Exception as e:
        print(f"Erro ao obter o preço BTC/USDT: {e}")
        return None


def synchronize_binance_time(client: Client):
    try:
        # Obtém o horário do servidor da Binance (em UTC)
        server_time = client.get_server_time()["serverTime"]  # Em milissegundos
        local_time = int(time.time() * 1000)
        
        # Calcula a diferença
        time_difference = server_time - local_time
        print(f"Desvio de horário detectado: {time_difference}ms")

        if abs(time_difference) > 1000:
            # Ajustar para o horário local com offset de fuso horário (ex.: UTC-3)
            local_offset = -3  # Fuso horário em horas
            adjusted_time = datetime.fromtimestamp(server_time / 1000, tz=timezone.utc) + timedelta(hours=local_offset)
            print(f"Horário ajustado (sincronizado): {adjusted_time.strftime('%Y-%m-%d %H:%M:%S')}")
            return adjusted_time
        else:
            print("Horário local está sincronizado com o servidor Binance.")
            return None  # Nenhuma alteração no horário
    except BinanceAPIException as e:
        print(f"Erro ao sincronizar com o servidor Binance: {e}")
        
def is_usdt_balance_greater(client: Client) -> bool:
    """
    Compara o saldo em USDT com o saldo em BTC na conta Binance e 
    retorna True se o saldo em USDT for maior que o equivalente em BTC, False caso contrário.

    Args:
        client (Client): Instância autenticada do cliente Binance.
    
    Returns:
        bool: True se o saldo em USDT for maior, False caso contrário.
    """
    try:
        # Obtém o saldo da conta
        account_info = client.get_account()
        balances = {item['asset']: float(item['free']) for item in account_info['balances']}

        # Saldo de USDT e BTC
        usdt_balance = balances.get('USDT', 0.0)
        btc_balance = balances.get('BTC', 0.0)

        # Pega o preço atual do BTC em USDT
        btc_price = float(client.get_symbol_ticker(symbol="BTCUSDT")['price'])

        # Converte o saldo de BTC para o equivalente em USDT
        btc_in_usdt = btc_balance * btc_price

        print(f"Saldo em USDT: {usdt_balance}")
        print(f"Saldo em BTC (em USDT): {btc_in_usdt}")

        # Compara os saldos
        return usdt_balance < btc_in_usdt

    except BinanceAPIException as e:
        print(f"Erro ao obter os saldos ou preços: {e}")
        return False
