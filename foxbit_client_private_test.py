#!/usr/bin/env python3.7
import os
from api_descriptors import RotatingQueue
from queue import Empty
from datetime import datetime, timedelta
from foxbit_client import FoxBitClient
from message_enums import ProductType
from colorama import Fore, Back, Style

# Get environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
USERID = os.getenv("FOXBIT_USERID")
USERNAME = os.getenv("FOXBIT_USERNAME")
PASSWORD = os.getenv("FOXBIT_PASSWORD")

OK =     "[" + Fore.GREEN + "  OK  " + Style.RESET_ALL + "]"
FAILED = "[" + Fore.RED   + "FAILED" + Style.RESET_ALL + "]"

def get_response(q: RotatingQueue, timeout=30):
    response = None
    try:
        response = q.get(block=True, timeout=timeout)
    except Empty:
        print("Timed out")
    return response

def test_sequence(debug=False):
    print(Fore.CYAN + "FoxBit Client - API Private endpoints" + Style.RESET_ALL)
    print(Fore.CYAN + "FoxBit Client - Requests" + Style.RESET_ALL)
    client = FoxBitClient(enableLog=False)
    omsId = 1

    print("{0:<30}".format("connect()"), end='')
    response = client.connect()
    if response and client.isConnected():
        print(OK)
    else:
        print(FAILED)

    if USERNAME and PASSWORD:
        code = input(Fore.CYAN + "Insert 2FA auth code: " + Fore.RESET)
        print("{0:<30}".format("webAuthenticateUser()"), end='')
        response = client.webAuthenticateUser(username=USERNAME, password=PASSWORD)
        if response:
            print(OK)
        else:
            print(FAILED)

        print("{0:<30}".format("authenticate2FA()"), end='')
        response = client.authenticate2FA(code=code)
        if response:
            print(OK)
            if debug:
                print(Fore.LIGHTGREEN_EX + "User ID: {:d}".format(client.userId))
                print("Session Token: {:s}".format(client.sessionToken) + Fore.RESET)
        else:
            print(FAILED)

    # This is the preferred method of authentication, one must know the userId beforehand though
    if USERID or client.userId is not None and API_KEY and API_SECRET:
        print("{0:<30}".format("authenticateUser()"), end='')
        userId = int(USERID) if USERID else client.userId
        response = client.authenticateUser(apiKey=API_KEY, apiSecret=API_SECRET, userId=userId)
        if response:
            print(OK)
        else:
            print(FAILED)

    print("{0:<30}".format("getUserConfig()"), end='')
    response = client.getUserConfig()
    if response is not None and isinstance(response, list) or isinstance(response, dict):
        print(OK)
    else:
        print(FAILED)

    print("{0:<30}".format("getUserInfo()"), end='')
    response = client.getUserInfo()
    if response and isinstance(response, dict) and "AccountId" in response:
        print(OK)
    else:
        print(FAILED)

    print("{0:<30}".format("getUserPermissions()"), end='')
    response = client.getUserPermissions(userId=client.userId)
    if response is not None and isinstance(response, list):
        print(OK)
        if debug:
            print(Fore.LIGHTGREEN_EX + "Permissions: {}".format(response) + Fore.RESET)
    else:
        print(FAILED)

    # setUserConfig() will not be tested
    # cancelAllOrders() will not be tested

    print("{0:<30}".format("getAccountInfo()"), end='')
    response = client.getAccountInfo(omsId=omsId, accountId=client.userId)
    if response and isinstance(response, dict) and "AccountId" in response:
        print(OK)
    else:
        print(FAILED)

    print("{0:<30}".format("getAccountPositions()"), end='')
    response = client.getAccountPositions(accountId=client.userId, omsId=omsId)
    if response is not None and isinstance(response, list):
        print(OK)
        if debug:
            for item in response:
                print(Fore.LIGHTGREEN_EX + "{:<9}: {}".format(item["ProductSymbol"], item["Amount"]) + Fore.RESET)
    else:
        print(FAILED)

    print("{0:<30}".format("getAccountTrades()"), end='')
    response = client.getAccountTrades(accountId=client.userId, omsId=omsId, startIndex=0, count=10)
    if response is not None and isinstance(response, list):
        print(OK)
        if debug:
            for item in response:
                print(Fore.LIGHTGREEN_EX + \
                    "{:<3}, {:<4}: {}, {}".format(item["InstrumentId"], item["Side"], item["Price"], item["Value"]) + \
                    Fore.RESET)
    else:
        print(FAILED)

    print("{0:<30}".format("getAccountTransactions()"), end='')
    response = client.getAccountTransactions(accountId=client.userId, omsId=omsId, depth=10)
    if response is not None and isinstance(response, list):
        print(OK)
        if debug:
            for item in response:
                print(Fore.LIGHTGREEN_EX + \
                    "{:<3}, {:<7}: {:>6}".format(item["TransactionId"], item["TransactionType"], item["Balance"]) + \
                    Fore.RESET)
    else:
        print(FAILED)

    print("{0:<30}".format("getOpenOrders()"), end='')
    response = client.getOpenOrders(accountId=client.userId, omsId=omsId)
    if response is not None and isinstance(response, list):
        print(OK)
    else:
        print(FAILED)

    # sendOrder() will not be tested
    # getOrderFee() will not be tested

    print("{0:<30}".format("getOrderHistory()"), end='')
    response = client.getOrderHistory(accountId=client.userId, omsId=omsId)
    if response is not None and isinstance(response, list):
        print(OK)
        if debug:
            for item in response:
                print(Fore.LIGHTGREEN_EX + \
                    "{:<5}, {:<4}: {}".format(item["Instrument"], item["Side"], item["OrderType"]) + \
                    Fore.RESET)
    else:
        print(FAILED)

    print("{0:<30}".format("getDepositTickets()"), end='')
    response = client.getDepositTickets(omsId=omsId, operatorId = 1, accountId=client.userId)
    if response is not None and isinstance(response, list):
        print(OK)
        if debug:
            for item in response:
                print(Fore.LIGHTGREEN_EX + \
                    "{:<4}{:6.2f}: {:}".format(item["AssetName"], item["Amount"], item["TicketNumber"]) + Fore.RESET)
    else:
        print(FAILED)

    print("{0:<30}".format("getWithdrawTickets()"), end='')
    response = client.getWithdrawTickets(omsId=omsId, operatorId = 1, accountId=client.userId)
    if response is not None and isinstance(response, list):
        print(OK)
        if debug:
            for item in response:
                print(Fore.LIGHTGREEN_EX + \
                    "{:<4}{:6.2f}: {:}".format(item["AssetName"], item["Amount"], item["TicketNumber"]) + Fore.RESET)
    else:
        print(FAILED)

    print("{0:<30}".format("logOut()"), end='')
    response = client.logOut()
    if response and not client.isConnected():
        print(OK)
    else:
        print(FAILED)

    # Removed
    # print("{0:<30}".format("getAccountFees()"), end='')
    # response = client.getAccountFees(accountId=client.userId, omsId=omsId)
    # if response and isinstance(response, dict):
    #     print(OK)
    #     # print(response)
    # else:
    #     print(FAILED)

if __name__ == "__main__":
    test_sequence()