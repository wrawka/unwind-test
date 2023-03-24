from typing import Any, List
from dataclasses import dataclass
import pandas as pd
from datetime import date

from utils.online import read_currency_value


@dataclass
class OrderLineData:
    line_no: int
    order_no: int
    value_usd: int
    due_date: date
    value_rub: float


def make_dataframe(data: List[List[Any]]) -> pd.DataFrame:
    """Puts `data` into dataframe adding RUB cost header."""
    if not data:
        return pd.DataFrame()

    usd_header = 'стоимость,$'
    rub_header = 'стоимость в руб.'
    exchange_rate = read_currency_value()

    df = pd.DataFrame(data=data[1:], columns=data[0])
    df[rub_header] = df[usd_header].astype(int) * exchange_rate
    df['срок поставки'] = pd.to_datetime(df['срок поставки'], format='%d.%m.%Y')

    return df
