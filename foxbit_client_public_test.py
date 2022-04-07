#!/usr/bin/env python3.7
from api_descriptors import RotatingQueue
from queue import Empty
from datetime import datetime, timedelta
from foxbit_client import FoxBitClient
from colorama import Fore, Style

OK =     "[" + Fore.GREEN + "  OK  " + Style.RESET_ALL + "]"
FAILED = "[" + Fore.RED   + "FAILED" + Style.RESET_ALL + "]"

def get_response(q: RotatingQueue, timeout=30):
    response = None
    try:
        response = q.get(block=True, timeout=timeout)
    except Empty:
        print("Timed out")
    return response

def test_sequence():
    print(Fore.CYAN + "FoxBit Client - API Public endpoints" + Style.RESET_ALL)
    print(Fore.CYAN + "FoxBit Client - Requests" + Style.RESET_ALL)
    client = FoxBitClient(enableConnLog=True)
    omsId = 1

    print("{0:<30}".format("connect()"), end='')
    response = client.connect()
    if response and client.isConnected():
        print(OK)
    else:
        print(FAILED)

    print("{0:<30}".format("getInstruments()"), end='')
    response = client.getInstruments(omsId)
    if response is not None:
        print(OK)
    else:
        print(FAILED)

    print("{0:<30}".format("getInstrument()"), end='')
    response = client.getInstrument(omsId, instrumentId=1)
    if response is not None and response["InstrumentId"] == 1:
        print(OK)
    else:
        print(FAILED)    

    print("{0:<30}".format("getProducts()"), end='')
    response = client.getProducts(omsId)
    if response is not None:
        print(OK)
    else:
        print(FAILED)

    # Removed
    # print("{0:<30}".format("getProduct()"), end='')
    # response = client.getProduct(omsId, productId=1)
    # if response is not None and response["ProductId"] == 1:
    #     print(OK)
    # else:
    #     print(FAILED)

    print("{0:<30}".format("getL2Snapshot()"), end='')
    response = client.getL2Snapshot(omsId, instrumentId=1)
    if response is not None:
        print(OK)
    else:
        print(FAILED)

    print("{0:<30}".format("getTickerHistory()"), end='')
    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    fromDate = now - timedelta(days=21)
    toDate = now - timedelta(days=20)
    response = client.getTickerHistory(omsId, instrumentId=1, fromDate=fromDate, toDate=toDate)
    if response is not None:
        print(OK)
    else:
        print(FAILED)

    print("{0:<30}".format("logOut()"), end='')
    response = client.logOut()
    if response and not client.isConnected():
        print(OK)
    else:
        print(FAILED)

    print("{0:<30}".format("connect() (reconnect)"), end='')
    response = client.connect()
    if response and client.isConnected():
        print(OK)
    else:
        print(FAILED)

    print(Fore.CYAN + "FoxBit Client - Subscription events" + Style.RESET_ALL)
    print("{0:<30}".format("subscribeLevel1()"), end='')
    response_queue = client.subscribeLevel1(omsId, instrumentIdOrSymbol=1)
    response1 = get_response(response_queue, timeout=200)
    response2 = get_response(response_queue, timeout=200)
    if response1 is not None and response2 is not None:
        print(OK)
    else:
        print(FAILED)

    print("{0:<30}".format("unsubscribeLevel1()"), end='')
    response = client.unsubscribeLevel1(omsId, instrumentId=1)
    if response:
        print(OK)
    else:
        print(FAILED)

    print("{0:<30}".format("subscribeLevel2()"), end='')
    response_queue = client.subscribeLevel2(omsId, instrumentIdOrSymbol=1)
    response1 = get_response(response_queue, timeout=200)
    response2 = get_response(response_queue, timeout=200)
    if response1 is not None and response2 is not None:
        print(OK)
    else:
        print(FAILED)

    print("{0:<30}".format("unsubscribeLevel2()"), end='')
    response = client.unsubscribeLevel2(omsId, instrumentId=1)
    if response:
        print(OK)
    else:
        print(FAILED)

    print("{0:<30}".format("subscribeTicker()"), end='')
    response_queue = client.subscribeTicker(omsId, instrumentId=1, interval=60, includeLastCount=1)
    response1 = get_response(response_queue, timeout=200)
    response2 = get_response(response_queue, timeout=200)
    if response1 is not None and response2 is not None:
        print(OK)
    else:
        print(FAILED)

    print("{0:<30}".format("unsubscribeTicker()"), end='')
    response = client.unsubscribeTicker(omsId, instrumentId=1)
    if response:
        print(OK)
    else:
        print(FAILED)

    print("{0:<30}".format("subscribeTrades()"), end='')
    response_queue = client.subscribeTrades(omsId, instrumentId=1, includeLastCount=100)
    response1 = get_response(response_queue, timeout=200)
    if response1 is not None and len(response1) == 100:
        print(OK)
    else:
        print(FAILED)

    print("{0:<30}".format("unsubscribeTrades()"), end='')
    response = client.unsubscribeTrades(omsId, instrumentId=1)
    if response:
        print(OK)
    else:
        print(FAILED)

if __name__ == "__main__":
    test_sequence()