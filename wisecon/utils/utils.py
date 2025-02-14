from typing import Iterable


__all__ = [
    "is_notebook",
    "tqdm_progress_bar",
]


def is_notebook():
    try:
        from IPython import get_ipython
        return 'IPKernelApp' in get_ipython().config
    except Exception:
        return False


def tqdm_progress_bar(iterable: Iterable, **kwargs):
    """"""
    if is_notebook():
        from tqdm.notebook import tqdm
        return tqdm(iterable, **kwargs)
    else:
        from tqdm import tqdm
        return tqdm(iterable, **kwargs)
