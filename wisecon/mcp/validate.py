import pandas as pd
from typing import Union


__all__ = [
    "validate_response_data"
]


def validate_response_data(data: Union[dict, list, pd.DataFrame], max_len: int = 50) -> str:
    """"""
    if len(data) == 0:
        return "No data found."
    prefix = ""
    if len(data) > max_len:
        prefix = f"Data too large with {len(data)} items, showing first 50 items:\n\n"

    if isinstance(data, list):
        data = str(data[:max_len])
    elif isinstance(data, pd.DataFrame):
        data = data.head(max_len).to_markdown(index=False)
    elif isinstance(data, dict):
        data = str({k: v for k, v in list(data.items())[:max_len]})
    data = f"{prefix}{data}"
    return data
