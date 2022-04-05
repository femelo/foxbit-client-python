import json
from datetime import datetime, timezone
from typing import List
from numbers import Number

def jsonStringify(input_dict: dict) -> str:
    return_dict = dict()
    for key, value in input_dict.items():
        if isinstance(value, dict):
            return_dict[key] = jsonStringify(value)
        else:
            return_dict[key] = value
    return json.dumps(return_dict)

def formatTicks(ticks: List[List[Number]]) -> List[dict]:
  formattedTicks = []
  for tick in ticks:
    formattedTicks.append(
      {
        "TickerDate": datetime.fromtimestamp(int(tick[0]) / 1e3, tz=timezone.utc),
        "High": float(tick[1]),
        "Low": float(tick[2]),
        "Open": float(tick[3]),
        "Close": float(tick[4]),
        "Volume": float(tick[5]),
        "BidPrice": float(tick[6]),
        "AskPrice": float(tick[7]),
        "InstrumentId": int(tick[8]),
      }
    )
  return formattedTicks

def formatL2Snapshots(snapshots: List[List[Number]]) -> List[dict]:
  formattedSnapshots = []
  for snapshot in snapshots:
    formattedSnapshots.append(
      {
        "MDUpdateID": int(snapshot[0]),
        "Accounts": int(snapshot[1]),
        "ActionDateTime": datetime.fromtimestamp(int(snapshot[2]) / 1e3, tz=timezone.utc),
        "ActionType": int(snapshot[3]),
        "LastTradePrice": int(snapshot[4]),
        "Orders": int(snapshot[5]),
        "Price": float(snapshot[6]),
        "ProductPairCode": int(snapshot[7]),
        "Quantity": float(snapshot[8]),
        "Side": int(snapshot[9])
      }
    )
  return formattedSnapshots

def formatTrades(trades: List[List[Number]]) -> List[dict]:
  formattedTrades = []
  for trade in trades:
    trades.append(
      {
        "TradeId": int(trade[0]),
        "InstrumentId": int(trade[1]),
        "Quantity": float(trade[2]),
        "Price": float(trade[3]),
        "Order1": int(trade[4]),
        "Order2": int(trade[5]),
        "Tradetime": datetime.fromtimestamp(int(trade[6]) / 1e3, tz=timezone.utc),
        "Direction": trade[7],
        "TakerSide": trade[8],
        "BlockTrade": bool(trade[9]),
        "Order1or2ClientId": int(trade[10])
      }
    )
  return formattedTrades
