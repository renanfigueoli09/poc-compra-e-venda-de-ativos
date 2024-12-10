import pandas as pd
import os
import time
import math
from binance.client import Client
from binance.enums import *
from src.util.minutes_to_seconds import time_string_to_seconds
from src.util.balances import (
    get_usdt_balance,
    convert_usdt_to_btc,
    synchronize_binance_time,
)
from src.util.nums import (
    truncate_to_first_significant_digit,
    create_num_witg_zero,
)
from src.config.flask_app import celery
import requests
from dotenv import load_dotenv
load_dotenv()
@celery.task()
def start():
    from src.config.flask_app import celery
    response = requests.get("https://api.ipify.org?format=json")
    ip = response.json()["ip"]
    print(f"Seu IP público de origem é: {ip}")

    api_key = os.getenv("API_KEY")
    secret_key = os.getenv("API_SECRET")
    client_binance = Client(api_key, secret_key)
    synchronize_binance_time(client_binance)

    symbol_info = client_binance.get_symbol_info("BTCUSDT")
    lot_size_filter = next(
        f for f in symbol_info["filters"] if f["filterType"] == "LOT_SIZE"
    )
    min_qty = float(lot_size_filter["minQty"])
    max_qty = float(lot_size_filter["maxQty"])
    step_size = float(lot_size_filter["stepSize"])

    print(lot_size_filter, min_qty, max_qty, step_size)

    active_code_ = "BTCUSDT"
    active_operated_ = "BTC"
    purchase_currency = "USDT"
    period_candle = Client.KLINE_INTERVAL_3MINUTE
    usdt_balance = get_usdt_balance(
        client_binance=client_binance, active_operated=purchase_currency
    )
    print(f" {purchase_currency}: {usdt_balance}")
    qaunt_active = convert_usdt_to_btc(
        usdt_balance=usdt_balance, client_binance=client_binance, symbol=active_code_
    )
    qaunt_active = truncate_to_first_significant_digit(qaunt_active)
    print(f" {active_operated_}: {qaunt_active}")


    def get_data(codigo, intervalo):

        candles = client_binance.get_klines(symbol=codigo, interval=intervalo, limit=1000)
        price = pd.DataFrame(candles)
        price.columns = [
            "tempo_abertura",
            "abertura",
            "maxima",
            "minima",
            "fechamento",
            "volume",
            "tempo_fechamento",
            "moedas_negociadas",
            "numero_trades",
            "volume_ativo_base_compra",
            "volume_ativo_cotação",
            "-",
        ]
        price = price[["fechamento", "tempo_fechamento"]]
        price["tempo_fechamento"] = pd.to_datetime(
            price["tempo_fechamento"], unit="ms"
        ).dt.tz_localize("UTC")
        price["tempo_fechamento"] = price["tempo_fechamento"].dt.tz_convert(
            "America/Sao_Paulo"
        )

        return price


    def commercial_strategy(data, active_code, active_operated, quant, position):

        data["media_rapida"] = data["fechamento"].rolling(window=7).mean()
        data["media_devagar"] = data["fechamento"].rolling(window=40).mean()

        fast_media_slow = data["media_rapida"].iloc[-1]
        last_media_slow = data["media_devagar"].iloc[-1]

        print(
            f"Última Média Rápida: {fast_media_slow} | Última Média Devagar: {last_media_slow}"
        )

        account = client_binance.get_account()

        for ativo in account["balances"]:

            if ativo["asset"] == active_operated:

                quantidade_atual = float(ativo["free"])
        if fast_media_slow > last_media_slow:
            if position == False:

                order = client_binance.create_order(
                    symbol=active_code,
                    side=SIDE_BUY,
                    type=ORDER_TYPE_MARKET,
                    quantity=quant,
                )

                print(order)
                print("COMPROU O ATIVO")

                position = True

        elif fast_media_slow < last_media_slow:

            if position == True:
                q = create_num_witg_zero(num=float(qaunt_active))
                quantity = int(quantidade_atual * q) / q
                quantity = "{:.{}f}".format(quantity, 4)
                print(quantity)
                order = client_binance.create_order(
                    symbol=active_code,
                    side=SIDE_SELL,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity,
                )
                print(order)
                print("VENDER O ATIVO")

                position = False

        return position


    current_position = False

    while True:

        dados_atualizados = get_data(codigo=active_code_, intervalo=period_candle)
        current_position = commercial_strategy(
            dados_atualizados,
            active_code=active_code_,
            active_operated=active_operated_,
            quant=qaunt_active,
            position=current_position,
        )
        print(f"aguardando proximo ciclo.... {period_candle}")
        time.sleep(time_string_to_seconds(time_string=period_candle))
