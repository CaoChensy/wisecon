import numpy as np
import pandas as pd
from scipy.stats import rankdata
from typing import Literal, Optional


__all__ = [
    "Operator",
]


class Operator:
    """"""
    normalized: Optional[Literal["z-score", "min-max"]]

    def normalized_data(self, data: pd.DataFrame,) -> pd.DataFrame:
        """"""
        if self.normalized == "z-score":
            return (data - data.mean()) / data.std()
        elif self.normalized == "min-max":
            return (data - data.min()) / (data.max() - data.min())
        else:
            raise ValueError("Invalid normalization method")

    def sign(self, data: pd.DataFrame) -> pd.DataFrame:
        """"""
        return data.apply(np.sign)

    def sign_pow(self, data: pd.DataFrame, power: pd.DataFrame) -> pd.DataFrame:
        """"""
        return data.apply(np.sign) * data.pow(power).abs()

    def log(self, data: pd.DataFrame) -> pd.DataFrame:
        """"""
        return data.apply(np.log)

    def sma(self, data: pd.DataFrame, period: int) -> pd.DataFrame:
        """"""
        return data.rolling(window=period).mean()

    def delay(self, data: pd.DataFrame, period: int) -> pd.DataFrame:
        """"""
        return data.shift(periods=period)

    def delta(self, data: pd.DataFrame, period: int) -> pd.DataFrame:
        """"""
        return data.diff(periods=period)

    def rank(self, data: pd.DataFrame, ) -> pd.DataFrame:
        """"""
        return data.rank(axis=1, pct=True)

    def stddev(self, data: pd.DataFrame, window: int) -> pd.DataFrame:
        """"""
        return data.rolling(window=window).std()

    def product(self, data: pd.DataFrame, window: int = 10) -> pd.DataFrame:
        """"""
        return data.rolling(window=window).apply(lambda x: np.prod(x))

    def ts_max(
            self,
            data: pd.DataFrame,
            window: int,
    ):
        """"""
        return data.rolling(window=window).max()

    def ts_min(
            self,
            data: pd.DataFrame,
            window: int,
    ):
        """"""
        return data.rolling(window=window).min()

    def ts_sum(
            self,
            data: pd.DataFrame,
            window: int,
    ):
        """"""
        return data.rolling(window=window).sum()

    def correlation(self, x: pd.DataFrame, y: pd.DataFrame, window: int) -> pd.DataFrame:
        """"""
        return x.rolling(window=window).corr(y)

    def covariance(self, x: pd.DataFrame, y: pd.DataFrame, window: int) -> pd.DataFrame:
        """"""
        return x.rolling(window=window).cov(y)

    def scale(self, data: pd.DataFrame, k: int = 1) -> pd.DataFrame:
        """"""
        return data.mul(k).div(data.abs().sum())

    def ts_rank(
            self,
            data: pd.DataFrame,
            window: int,
            method: Literal["average", "min", "max", "first", "dense"] = "average",
    ) -> pd.DataFrame:
        """"""
        return data.rolling(window=window).apply(
            # lambda x: pd.Series(x).rank(method=method).iloc[-1], raw=False
            lambda x: rankdata(x)[-1], raw=True
        )

    def ts_argmax(
            self,
            data: pd.DataFrame,
            window: int,
    ) -> pd.DataFrame:
        """"""
        return data.rolling(window=window).apply(
            lambda x: np.argmax(x), raw=True
        )

    def ts_argmin(
            self,
            data: pd.DataFrame,
            window: int,
    ) -> pd.DataFrame:
        """"""
        return data.rolling(window=window).apply(
            lambda x: np.argmin(x), raw=True
        )

    def decay_linear(self, data: pd.DataFrame, window: int = 10) -> pd.DataFrame:
        """"""
        weights = np.arange(1, window + 1)
        def _decay(window):
            return (window * weights).sum() / weights.sum()
        return data.rolling(window, min_periods=window).apply(_decay, raw=True)

    def indneutralize(self, data: pd.DataFrame, ind_mapping: dict):
        """
        Args:
            data: 因子 DataFrame，index 为日期，columns 为股票代码
            ind_mapping: 股票代码 -> 行业 的字典映射

        Returns: 行业中性化后的因子 DataFrame
        """
        stock_industry = pd.Series(ind_mapping, name="industry")
        long = data.stack().reset_index()
        long.columns = ["time", "code", "value"]
        long = long.merge(
            stock_industry, left_on="code", right_index=True, how="left"
        )
        long.dropna(subset=["value", "industry"], inplace=True)

        def zscore(group):
            return (group - group.mean()) / group.std() if len(group) > 1 else pd.Series([0] * len(group), index=group.index)

        long['alpha'] = long.groupby(['time', 'industry'])['value'].transform(zscore)
        neutralized = long.pivot(index='time', columns='code', values='alpha')
        neutralized = neutralized.reindex(columns=data.columns, index=data.index)
        return neutralized
