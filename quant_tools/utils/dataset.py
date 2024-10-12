from typing import Dict, List, Optional


__all__ = [
    'filter_dict_by_key',
    'filter_str_by_mark',
]


def filter_dict_by_key(d: Dict, keys: List[str]) -> Dict:
    return {k: v for k, v in d.items() if k in keys}


def filter_str_by_mark(
        s: str,
        start: Optional[str] = "{",
        end: Optional[str] = "}",
        keep_mark: Optional[bool] = True
) -> str:
    start_id = s.find(start)
    end_id = s.rfind(end)
    if keep_mark:
        return s[start_id: end_id + len(end)]
    else:
        return s[start_id + len(start): end_id]
