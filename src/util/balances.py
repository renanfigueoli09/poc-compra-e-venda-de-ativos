from datetime import datetime, timedelta, timezone

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


import time
from binance.client import BinanceAPIException
def synchronize_binance_time(client):
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
        else:
            print("Horário local está sincronizado com o servidor Binance.")
    except BinanceAPIException as e:
        print(f"Erro ao sincronizar com o servidor Binance: {e}")