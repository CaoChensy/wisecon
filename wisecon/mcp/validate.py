import pandas as pd
from typing import Union


__all__ = [
    "validate_response_data"
]


def validate_response_data(data: Union[list, pd.DataFrame]) -> str:
    """"""
    if len(data) == 0:
        return "No data found."
    prefix = ""
    if len(data) > 50:
        prefix = "Data too large, showing first 50 rows:\n\n"

    if isinstance(data, list):
        data = str(data[:50])
    elif isinstance(data, pd.DataFrame):
        data = data.head(50).to_markdown(index=False)
    data = f"{prefix}{data}"
    return data
