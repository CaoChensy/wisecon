import numpy as np
import pandas as pd
from typing import Dict, Union, Literal, Optional
from wisecon.types.alpha import AlphaKlineData
from .operator import Operator


__all__ = [
    "Alpha101"
]


class Alpha101(Operator):
    """"""

    def __init__(
            self,
            data: Optional[Union[AlphaKlineData, Dict[str, pd.DataFrame]]] = None,
            open: Optional[pd.DataFrame] = None,
            close: Optional[pd.DataFrame] = None,
            high: Optional[pd.DataFrame] = None,
            low: Optional[pd.DataFrame] = None,
            volume: Optional[pd.DataFrame] = None,
            turnover: Optional[pd.DataFrame] = None,
            cap: Optional[pd.DataFrame] = None,
            ind_mapping: Optional[Dict[str, str]] = None,
            normalized: Optional[Literal["z-score", "min-max"]] = None,
    ):
        """"""
        if isinstance(data, AlphaKlineData):
            data = data.model_dump()

        self.open = data.get("open", open)
        self.close = data.get("close", close)
        self.high = data.get("high", high)
        self.low = data.get("low", low)
        self.volume = data.get("volume", volume)
        self.turnover = data.get("turnover", turnover)
        self.cap = data.get("cap", cap)
        self.ind_mapping = ind_mapping
        self.vwap = self.turnover / self.volume
        self.normalized = normalized
        self._daily_returns = None

    @property
    def daily_returns(self) -> pd.DataFrame:
        """"""
        if self._daily_returns is None:
            returns = self.close.pct_change()
            # Replace infinite values with 0 while preserving NaN
            self._daily_returns = returns.replace([np.inf, -np.inf], 0)
        return self._daily_returns

    def alpha_001(
            self,
            window_return: int = 20,
            window_ts_argmax: int = 5,
    ) -> pd.DataFrame:
        """
        (
            rank(
                Ts_ArgMax(
                    SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.),
                    5
                )
            ) -0.5
        )

        Returns:

        """
        # 1. Calculate rolling standard deviation
        vol = self.daily_returns.rolling(window=window_return).std()
        # 2. Conditional value selection
        cond_value = pd.DataFrame(
            np.where(self.daily_returns < 0, vol, self.close),
            index=self.daily_returns.index,
            columns=self.daily_returns.columns,
        )

        # 3. Signed power calculation
        signed_power = np.sign(cond_value) * (cond_value ** 2)
        ts_argmax = self.ts_argmax(data=signed_power, window=window_ts_argmax)
        return self.rank(data=ts_argmax) - 0.5

    def alpha_002(
            self,
            window: int = 6,
    ) -> pd.DataFrame:
        """
        分析成交量变化与价格变化之间的关系来捕捉股票的短期动量或反转效应
        todo: 可能存在价格和成交量值域差距过大情况，考虑归一化处理，参考alpha_202

         (
            -1 *
            correlation(
                rank(
                    delta(
                        log(volume), 2
                    )
                ),
                rank(
                    ((close - open) / open)
                ),
                6
            )
        )
        Returns:

        """
        return -1 * self.correlation(
            self.rank(self.delta(self.log(self.volume), 2)),
            self.rank((self.close - self.open) / self.open),
            6
        )

    def alpha_202(
            self,
            window: int = 6,
    ) -> pd.DataFrame:
        """
        分析成交量变化与价格变化之间的关系来捕捉股票的短期动量或反转效应，是alpha_002的改进版本。

         (
            -1 *
            correlation(
                rank(
                    delta(
                        log(volume), 2
                    )
                ),
                rank(
                    ((close - open) / open)
                ),
                6
            )
        )
        Returns:

        """
        # 计算 log(volume) 的 2 日变化量
        delta_log_volume = self.volume.apply(np.log).diff(2)

        # 计算 (close - open) / open
        price_change_ratio = (self.close - self.open) / self.open

        # 对 delta_log_volume 和 price_change_ratio 进行排名
        rank_delta_log_volume = self.rank(delta_log_volume)
        rank_price_change_ratio = self.rank(price_change_ratio)

        if self.normalized:
            rank_delta_log_volume = self.normalized_data(rank_delta_log_volume)
            rank_price_change_ratio = self.normalized_data(rank_price_change_ratio)

        # 计算 6 日滚动相关性, 取负值
        alpha_002 = -1 * rank_delta_log_volume.rolling(window=window, axis=0).corr(rank_price_change_ratio)
        return alpha_002

    def alpha_003(
            self,
            window: int = 10,
    ) -> pd.DataFrame:
        """通过分析开盘价和成交量之间的关系来捕捉股票的短期动量或反转效应
        todo: 可能存在价格和成交量值域差距过大情况，考虑归一化处理，参考alpha_203

        (-1 * correlation(rank(open), rank(volume), 10))

        Returns:
        """
        return -1 * self.correlation(self.rank(self.open), self.rank(self.volume), window=window)

    def alpha_203(
            self,
            window: int = 10,
    ) -> pd.DataFrame:
        """通过分析开盘价和成交量之间的关系来捕捉股票的短期动量或反转效应，
        是alpha_003的改进版本，考虑了价格和成交量的归一化处理

        (-1 * correlation(rank(open), rank(volume), 10))

        Returns:
        """
        if self.normalized:
            _open = self.normalized_data(self.open)
            _volume = self.normalized_data(self.volume)
        else:
            _open = self.open
            _volume = self.volume

        # 计算开盘价和成交量的排名
        rank_open = self.rank(_open)
        rank_volume = self.rank(_volume)

        # 计算 10 日滚动相关性
        correlation = rank_open.rolling(window=window, axis=0).corr(rank_volume)

        # 取负值
        alpha_003 = -1 * correlation
        return alpha_003

    def alpha_004(
            self,
            window: int = 9,
    ):
        """
        (-1 * Ts_Rank(rank(low), 9))
        Returns:
        """
        # 计算最低价的排名
        rank_low = self.rank(self.low)

        # 计算 9 日滚动时间序列排名
        ts_rank_low = self.ts_rank(data=rank_low, window=window)

        # 返回结果，取负值
        return -1 * ts_rank_low

    def alpha_204(
            self,
            window: int = 9,
    ):
        """
        (-1 * Ts_Rank(rank(low), 9))
        Returns:
        """
        if self.normalized:
            _low = self.normalized_data(self.low)
        else:
            _low = self.low

        # 计算最低价的排名
        rank_low = self.rank(_low)

        # 计算 9 日滚动时间序列排名
        ts_rank_low = self.ts_rank(data=rank_low, window=window)

        # 返回结果，取负值
        return -1 * ts_rank_low

    def alpha_005(
            self,
            window: int = 10
    ):
        """
        (rank((open - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap)))))
        Returns:

        """
        # 计算过去 10 天的 VWAP 平均值
        vwap_mean = self.vwap.rolling(window=window).mean()

        # 计算因子的第一部分：开盘价与过去 10 天 VWAP 平均值的差值
        part1 = self.rank(self.open - vwap_mean)

        # 计算因子的第二部分：收盘价与当天 VWAP 的差值的绝对值
        part2 = -1 * (self.rank(self.close - self.vwap).abs())
        return part1 * part2


    def alpha_006(self):
        """
        (-1 * correlation(open, volume, 10))
        Returns:

        """
        return -1 * self.correlation(self.open, self.volume, window=10)

    def alpha_007(self):
        """
        ((adv20 < volume) ? ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))) : (-1* 1))
        Returns:

        """
        adv20 = self.sma(self.volume, 20)
        part_a = adv20 < self.volume
        part_b = -1 * self.ts_rank(self.delta(self.close, 7).abs(), 60) * self.sign(self.delta(self.close, 7))
        return part_b.where(part_a, -1)

    def alpha_008(self):
        """
        (-1 * rank(((sum(open, 5) * sum(returns, 5)) - delay((sum(open, 5) * sum(returns, 5)),10))))

        Returns:

        """
        rolling_open_sum = self.ts_sum(self.open, 5)
        rolling_returns_sum = self.ts_sum(self.daily_returns, 5)
        _product = rolling_open_sum * rolling_returns_sum
        _product_delay = self.delay(data=_product, period=10)
        return -1 * self.rank(data=(_product - _product_delay))

    def alpha_009(self):
        """
        ((0 < ts_min(delta(close, 1), 5)) ? delta(close, 1) : ((ts_max(delta(close, 1), 5) < 0) ?delta(close, 1) : (-1 * delta(close, 1))))
        Returns:

        """
        delta_close = self.delta(data=self.close, period=1)
        ts_min = self.ts_min(data=delta_close, window=5)
        ts_max = self.ts_max(data=delta_close, window=5)
        cond_1 = ts_min > 0
        cond_2 = ts_max < 0
        return delta_close.where(~cond_1 & ~cond_2, -1 * delta_close)

    def alpha_010(self):
        """
        rank(((0 < ts_min(delta(close, 1), 4)) ? delta(close, 1) : ((ts_max(delta(close, 1), 4) < 0)? delta(close, 1) : (-1 * delta(close, 1)))))
        Returns:

        """
        delta_close = self.delta(data=self.close, period=1)
        ts_min = self.ts_min(data=delta_close, window=4)
        ts_max = self.ts_max(data=delta_close, window=4)
        cond_1 = ts_min > 0
        cond_2 = ts_max < 0
        return self.rank(data=delta_close.where(~cond_1 & ~cond_2, -1 * delta_close))

    def alpha_011(self):
        """
        # Alpha#11	 ((rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3))) * rank(delta(volume, 3)))

        Returns:

        """
        ts_max = self.ts_max(self.vwap - self.close, window=3)
        ts_min = self.ts_min(self.vwap - self.close, window=3)
        vol_delta = self.delta(self.volume, period=3)
        return (self.rank(ts_max) + self.rank(ts_min)) * self.rank(vol_delta)

    def alpha_012(self):
        """
        # Alpha#12	 (sign(delta(volume, 1)) * (-1 * delta(close, 1)))

        Returns:

        """
        volume_delta = self.delta(self.volume, period=1)
        close_delta = self.delta(self.close, period=1)
        return np.sign(volume_delta) * (-1 * close_delta)

    def alpha_013(self):
        """
        # Alpha#13 (-1 * rank(covariance(rank(close), rank(volume), 5)))

        Returns:

        """
        cov_rank = self.covariance(self.rank(self.close), self.rank(self.volume), window=5)
        return -1 * self.rank(cov_rank)

    def alpha_014(self):
        """
        # Alpha#14	 ((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10))

        Returns:

        """
        delta_ret = self.delta(self.daily_returns, period=3)
        corr = self.correlation(self.open, self.volume, window=10)
        return (-1 * self.rank(delta_ret)) * corr

    def alpha_015(self):
        """
        # Alpha#15 (-1 * sum(rank(correlation(rank(high), rank(volume), 3)), 3))

        Returns:

        """
        corr = self.correlation(self.rank(self.high), self.rank(self.volume), window=3)
        return -1 * self.ts_sum(self.rank(corr), window=3)

    def alpha_016(self):
        """
        # Alpha#16	 (-1 * rank(covariance(rank(high), rank(volume), 5)))

        Returns:

        """
        cov_rank = self.covariance(self.rank(self.high), self.rank(self.volume), window=5)
        return -1 * self.rank(cov_rank)

    def alpha_017(self):
        """
        # Alpha#17	 (((-1 * rank(ts_rank(close, 10))) * rank(delta(delta(close, 1), 1))) *rank(ts_rank((volume / adv20), 5)))

        Returns:

        """
        adv20 = self.sma(data=self.volume, period=20)
        part_1 = -1 * self.rank(self.ts_rank(self.close, window=10))
        part_2 = self.rank(self.delta(self.delta(self.close, 1), 1))
        part_3 = self.rank(self.ts_rank((self.volume / adv20), window=5))
        return part_1 * part_2 * part_3

    def alpha_018(self):
        """
        # Alpha#18:
            (-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open,10))))

        Returns:

        """
        std = self.stddev((self.close - self.open).abs(), window=5)
        corr = self.correlation(self.close, self.open, window=10)
        return -1 * self.rank(std + self.close - self.open + corr)

    def alpha_019(self):
        """
        # Alpha#19	 ((-1 * sign(((close - delay(close, 7)) + delta(close, 7)))) * (1 + rank((1 + sum(returns,250)))))

        Returns:

        """
        delay_close = self.delay(self.close, 7)
        delta_close = self.delta(self.close, 7)
        ts_sum = self.ts_sum(self.daily_returns, window=250)
        return (-1 * (self.close - delay_close).apply(np.sign) + delta_close) * (1 + self.rank(1 + ts_sum))

    def alpha_020(self):
        """
        # Alpha#20	 (((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open -delay(low, 1))))

        Returns:

        """
        delay_heigh = self.delay(self.high, 1)
        delay_close = self.delay(self.close, 1)
        delay_low = self.delay(self.low, 1)
        return -1 * self.rank(self.open - delay_heigh) * self.rank(self.open - delay_close) * self.rank(self.open - delay_low)

    def alpha_021(self):
        """
        # Alpha#21
        (
            (((sum(close, 8) / 8) + stddev(close, 8)) < (sum(close, 2) / 2)) ? (-1 * 1) :
            (((sum(close,2) / 2) < ((sum(close, 8) / 8) - stddev(close, 8))) ? 1 :
            (((1 < (volume / adv20)) || ((volume / adv20) == 1)) ? 1 : (-1 * 1)))
        )

        Returns:

        """
        sma_close_2 = self.sma(self.close, 2)
        sma_close_8 = self.sma(self.close, 8)
        stddev_close_8 = self.stddev(self.close, 8)
        adv20 = self.sma(self.volume, 20)

        cond_1 = (sma_close_8 + stddev_close_8) < sma_close_2
        cond_2 = (~cond_1) & (sma_close_2 < (sma_close_8 - stddev_close_8))
        cond_3 = (~cond_1) & (~cond_2) & (self.volume >= adv20)

        alpha = pd.DataFrame(np.ones_like(self.close), index=self.close.index, columns=self.close.columns)
        alpha[cond_1] = -1
        alpha[cond_2] = 1
        alpha[cond_3] = 1
        alpha[~(cond_1 | cond_2 | cond_3)] = -1
        return alpha

    def alpha_022(self):
        """
        # Alpha#22	 (-1 * (delta(correlation(high, volume, 5), 5) * rank(stddev(close, 20))))

        Returns:

        """
        delta_corr = self.delta(self.correlation(self.high, self.volume, 5), 5)
        rank_stddev = self.rank(self.stddev(self.close, 20))
        return -1 * delta_corr * rank_stddev

    def alpha_023(self):
        """
        # Alpha#23	 (((sum(high, 20) / 20) < high) ? (-1 * delta(high, 2)) : 0)

        Returns:

        """
        cond = (self.sma(self.high, 20) < self.high)
        delta_high = -1 * self.delta(self.high, 2)
        return delta_high.where(cond, 0)

    def alpha_024(self):
        """
        # Alpha#24
        (
            (((delta((sum(close, 100) / 100), 100) / delay(close, 100)) < 0.05) ||
            ((delta((sum(close, 100) / 100), 100) / delay(close, 100)) == 0.05)) ?
            (-1 * (close - ts_min(close,100))) :
            (-1 * delta(close, 3))
        )

        Returns:

        """
        delta_sma_close = self.delta(self.sma(self.close, 100), 100)
        delay_close = self.delay(self.close, 100)
        ts_min_close = self.ts_min(self.close, 100)
        delta_close = -1 * self.delta(self.close, 3)

        cond = (delta_sma_close / delay_close <= 0.05)
        data = (-1 * (self.close - ts_min_close))
        return data.where(cond, delta_close)

    def alpha_025(self):
        """
            # Alpha#25	 rank(((((-1 * returns) * adv20) * vwap) * (high - close)))

        Returns:

        """
        return self.rank(-1 * self.daily_returns * self.sma(self.volume, 20) * self.vwap * (self.high - self.close))

    def alpha_026(self):
        """
            # Alpha#26 (-1 * ts_max(correlation(ts_rank(volume, 5), ts_rank(high, 5), 5), 3))

        Returns:

        """
        corr = self.correlation(
            self.ts_rank(self.volume, 5),
            self.ts_rank(self.high, 5),
            5
        )
        return -1 * self.ts_max(corr, 3)

    def alpha_027(self):
        """
            # Alpha#27	 ((0.5 < rank((sum(correlation(rank(volume), rank(vwap), 6), 2) / 2.0))) ? (-1 * 1) : 1)

        Returns:

        """
        corr = self.correlation(
            self.rank(self.volume),
            self.rank(self.vwap),
            6
        )
        cond = self.rank(self.sma(corr, 2)) > 0.5
        alpha = pd.DataFrame(np.ones_like(self.close), index=self.close.index, columns=self.close.columns)
        alpha = alpha.where(~cond, -1)
        return alpha

    def alpha_028(self):
        """
        # Alpha#28 scale(((correlation(adv20, low, 5) + ((high + low) / 2)) - close))

        Returns:

        """
        adv20 = self.sma(self.volume, 20)
        corr = self.correlation(adv20, self.low, 5)
        return self.scale(corr + ((self.high + self.low) / 2) - self.close)


    def alpha_029(self):
        """
        # Alpha#29
        (min(product(rank(rank(scale(log(sum(ts_min(rank(rank(
        (-1 * rank(delta((close - 1),5))))), 2), 1))))), 1), 5) +
        ts_rank(delay((-1 * returns), 6), 5))

        Returns:

        """
        part_a = self.ts_min(
            data=self.product(
                self.rank(
                    data=self.rank(
                        data=self.scale(
                            data=(
                                self.ts_sum(
                                    data=self.ts_min(
                                        data=self.rank(
                                            data=-1 * self.rank(
                                                data=self.delta(self.close - 1, 5)
                                            )
                                        ),
                                        window=2,
                                    ),
                                    window=1,
                                )
                            ).apply(np.log)
                        )
                    ),
                ),
                window=1,
            ),
            window=5,
        )
        part_b = self.ts_rank(data=self.delta(-1 * self.daily_returns, 6), window=5)
        return part_a + part_b

    def alpha_030(self):
        """
        # Alpha#30
        (((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) -
        delay(close, 2)))) +sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20))

        Returns:

        """
        delay_close_1 = self.delay(self.close, 1)
        delay_close_2 = self.delay(self.close, 2)
        delay_close_3 = self.delay(self.close, 3)
        rank_data = (
            (self.close - delay_close_1).apply(np.sign) +
            (delay_close_1 - delay_close_2).apply(np.sign) +
            (delay_close_2 - delay_close_3).apply(np.sign)
        )
        return (1 - self.rank(rank_data)) * self.ts_sum(self.volume, 5) / self.ts_sum(self.volume, 20)

    def alpha_031(self):
        """
        # Alpha#31
        ((rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10))))
        + rank((-1 *delta(close, 3)))) + sign(scale(correlation(adv20, low, 12))))

        Returns:

        """
        adv20 = self.sma(self.volume, 20)
        part_a = self.rank(self.rank(self.rank(
            self.decay_linear(
                -1 * self.rank(self.rank(self.delta(self.close, 10))),
                window=10,
            )
        )))
        part_b = self.rank(-1 * self.delta(self.close, 3))
        part_c = self.scale(self.correlation(adv20, self.low, 12)).apply(np.sign)
        return part_a + part_b + part_c

    def alpha_032(self):
        """
        # Alpha#32 (scale(((sum(close, 7) / 7) - close)) + (20 * scale(correlation(vwap, delay(close, 5),230))))

        Returns:

        """
        part_a = self.scale(self.sma(self.close, 7) - self.close)
        part_b = 20 * self.scale(self.correlation(self.vwap, self.delay(self.close, 5), 230))
        return part_a + part_b

    def alpha_033(self):
        """
        # Alpha#33 rank((-1 * ((1 - (open / close))^1)))

        Returns:
        """
        return self.rank(self.open / self.close - 1)

    def alpha_034(self):
        """
        # Alpha#34 rank(((1 - rank((stddev(returns, 2) / stddev(returns, 5)))) + (1 - rank(delta(close, 1)))))

        Returns:

        """
        rank_stddev = self.rank(self.stddev(self.daily_returns, 2) / self.stddev(self.daily_returns, 5))
        # part_b = self.rank(self.delta(self.close, 1))
        return self.rank(2 - rank_stddev - self.rank(self.delta(self.close, 1)))

    def alpha_035(self):
        """
        # Alpha#35 ((Ts_Rank(volume, 32) * (1 - Ts_Rank(((close + high) - low), 16))) * (1 -Ts_Rank(returns, 32)))

        Returns:

        """
        ts_rank_volume = self.ts_rank(self.volume, 32)
        ts_rank_mid = 1 - self.ts_rank(self.close + self.high - self.low, 16)
        ts_rank_bot = 1 - self.ts_rank(self.daily_returns, 32)
        return ts_rank_volume * ts_rank_mid * ts_rank_bot

    def alpha_036(self):
        """
        # Alpha#36 (((((2.21 * rank(correlation((close - open), delay(volume, 1), 15))) + (0.7 * rank((open- close)))) + (0.73 * rank(Ts_Rank(delay((-1 * returns), 6), 5)))) + rank(abs(correlation(vwap,adv20, 6)))) + (0.6 * rank((((sum(close, 200) / 200) - open) * (close - open)))))

        Returns:

        """
        adv20 = self.sma(self.volume, 20)
        part_a = 2.21 * self.rank(self.correlation(self.close - self.open, self.delay(self.volume, 1), 15))
        part_b = 0.7 * self.rank(self.open - self.close)
        part_c = 0.73 * self.rank(self.ts_rank(self.delay(-1 * self.daily_returns, 6), 5))
        part_d = self.rank(self.correlation(self.vwap, adv20, 6).abs())
        part_e = 0.6 * self.rank((self.sma(self.close, 200) - self.open) * (self.close - self.open))
        return part_a + part_b + part_c + part_d + part_e

    def alpha_037(self):
        """
        # Alpha#37 (rank(correlation(delay((open - close), 1), close, 200)) + rank((open - close)))

        Returns:

        """
        return self.rank(self.correlation(self.delay(self.open - self.close, 1), self.close, 200)) + self.rank(self.open - self.close)

    def alpha_038(self):
        """
        # Alpha#38	 ((-1 * rank(Ts_Rank(close, 10))) * rank((close / open)))

        Returns:

        """
        return -1 * self.rank(self.ts_rank(self.close, 10)) * self.rank(self.close / self.open)

    def alpha_039(self):
        """
        # Alpha#39
        ((-1 * rank((delta(close, 7) * (1 - rank(decay_linear((volume / adv20), 9)))))) * (1 +rank(sum(returns, 250))))

        Returns:

        """
        adv20 = self.sma(self.volume, 20)
        part_a = -1 * self.rank(self.delta(self.close, 7) * (1 - self.rank(self.decay_linear((self.volume / adv20), 9))))
        part_b = 1 + self.rank(self.ts_sum(self.daily_returns, 250))
        return part_a * part_b

    def alpha_040(self):
        """
        # Alpha#40
        ((-1 * rank(stddev(high, 10))) * correlation(high, volume, 10))

        Returns:

        """
        return -1 * self.rank(self.stddev(self.high, 10)) * self.correlation(self.high, self.volume, 10)

    def alpha_041(self):
        """
            # Alpha#41	 (((high * low)^0.5) - vwap)

        Returns:

        """
        return (self.high * self.low).pow(0.5) - self.vwap

    def alpha_042(self):
        """
        # Alpha#42	 (rank((vwap - close)) / rank((vwap + close)))

        Returns:

        """
        return self.rank(self.vwap - self.close) / self.rank(self.vwap + self.close)

    def alpha_043(self):
        """
        # Alpha#43	 (ts_rank((volume / adv20), 20) * ts_rank((-1 * delta(close, 7)), 8))

        Returns:

        """
        adv20 = self.sma(self.volume, 20)
        return self.ts_rank((self.volume / adv20), 20) * self.ts_rank((-1 * self.delta(self.close, 7)), 8)

    def alpha_044(self):
        """
        # Alpha#44 (-1 * correlation(high, rank(volume), 5))

        Returns:

        """
        return -1 * self.correlation(self.high, self.rank(self.volume), 5)

    def alpha_045(self):
        """
        # Alpha#45
        (
            -1 * (
                (rank( (sum(delay(close, 5), 20) / 20) ) *
                 correlation(close, volume, 2)
                )
                *
                rank( correlation( sum(close, 5), sum(close, 20), 2 ) )
            )
        )
        Returns:

        """
        part_a = self.rank(self.sma(self.delay(self.close, 5), 20))
        part_b = self.correlation(self.close, self.volume, 2)
        part_c = self.rank(self.correlation(self.ts_sum(self.close, 5), self.ts_sum(self.close, 20), 2))
        return -1 * (part_a * part_b * part_c)

    def alpha_046(self):
        """
        # Alpha#46
        ((0.25 < (((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10))) ?(-1 * 1) :
        (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < 0) ? 1 :
        ((-1 * 1) * (close - delay(close, 1)))))

        Returns:

        """
        part_a = ((self.delay(self.close, 20) - self.delay(self.close, 10)) / 10) - ((self.delay(self.close, 10) - self.close) / 10)
        part_b = -1 * (self.close - self.delay(self.close, 1))
        part_b.where(part_a < 0, 1, inplace=True)
        part_b.where(part_a > 0.25, -1, inplace=True)
        return part_b

    def alpha_047(self):
        """
        # Alpha#47
        (
            (
                (rank((1 / close)) * volume) / adv20
            ) *
            (
                high * rank((high - close)) / (sum(high, 5) / 5)
            )
        ) - rank((vwap - delay(vwap, 5)))
        Returns:

        """
        adv20 = self.sma(self.volume, 20)
        part_a = ((self.rank(1 / self.close) * self.volume) / adv20)
        part_b = (self.high * self.rank(self.high - self.close)) / self.sma(self.high, 5)
        part_c = self.rank(self.vwap - self.delay(self.vwap, 5))
        return part_a * part_b - part_c

    def alpha_048(self):
        """
        Alpha#48:
        (
            indneutralize(
                (
                    correlation(delta(close, 1), delta(delay(close, 1), 1), 250) *
                    delta(close, 1)
                ) / close,
                IndClass.subindustry
            )
        ) / sum(
            (delta(close, 1) / delay(close, 1)) ** 2,
            250
        )
        Returns:

        """
        part_a = (self.correlation(self.delta(self.close, 1), self.delta(self.delay(self.close, 1), 1), 250) * self.delta(self.close, 1)) / self.close
        part_b = self.ts_sum((self.delta(self.close, 1) / self.delay(self.close, 1)).pow(2), 250)
        return self.indneutralize(part_a, self.ind_mapping) / part_b

    def alpha_049(self):
        """
        # Alpha#49
        (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 *0.1)) ? 1 : ((-1 * 1) * (close - delay(close, 1))))

        Returns:

        """
        part_a = ((self.delay(self.close, 20) - self.delay(self.close, 10)) / 10) - ((self.delay(self.close, 10) - self.close) / 10)
        part_b = -1 * (self.close - self.delay(self.close, 1))
        alpha = part_b.where(part_a < -0.1, 1)
        return alpha

    def alpha_050(self):
        """
        # Alpha#50
        (-1 * ts_max(rank(correlation(rank(volume), rank(vwap), 5)), 5))

        Returns:

        """
        return -1 * self.ts_sum(self.rank(self.correlation(self.rank(self.volume), self.rank(self.vwap), 5)), 5)


    def alpha_051(self):
        """
        # Alpha#51
        (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 *0.05)) ? 1 : ((-1 * 1) * (close - delay(close, 1))))

        Returns:

        """
        part_a = ((self.delay(self.close, 20) - self.delay(self.close, 10)) / 10) - ((self.delay(self.close, 10) - self.close) / 10)
        part_b = -1 * (self.close - self.delay(self.close, 1))
        alpha = part_b.where(part_a < -0.05, 1)
        return alpha

    def alpha_052(self):
        """
        # Alpha#52	 ((((-1 * ts_min(low, 5)) + delay(ts_min(low, 5), 5)) * rank(((sum(returns, 240) -sum(returns, 20)) / 220))) * ts_rank(volume, 5))

        Returns:

        """
        return (((-1 * self.ts_min(self.low, 5)) + self.delay(self.ts_min(self.low, 5), 5)) * self.rank(((self.ts_sum(self.daily_returns, 240) - self.ts_sum(self.daily_returns, 20)) / 220))) * self.ts_rank(self.volume, 5)

    def alpha_053(self):
        """
        # Alpha#53	 (-1 * delta((((close - low) - (high - close)) / (close - low)), 9))

        Returns:

        """
        return -1 * self.delta((((self.close - self.low) - (self.high - self.close)) / (self.close - self.low)), 9)

    def alpha_054(self):
        """
        # Alpha#54	 ((-1 * ((low - close) * (open^5))) / ((low - high) * (close^5)))

        Returns:

        """
        return (-1 * (self.low - self.close) * self.open.pow(5)) / ((self.low - self.high) * self.close.pow(5))

    def alpha_055(self):
        """
        # Alpha#55	 (-1 * correlation(rank(((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low,12)))), rank(volume), 6))

        Returns:

        """
        part_a = self.correlation(
            self.rank((self.close - self.ts_min(self.low, 12)) / (self.ts_max(self.high, 12) - self.ts_min(self.low,12))),
            self.rank(self.volume), 6)
        return -1 * part_a

    def alpha_056(self):
        """
        # Alpha#56	 (0 - (1 * (rank((sum(returns, 10) / sum(sum(returns, 2), 3))) * rank((returns * cap)))))

        Returns:

        """
        return 0 - (1 * (self.rank((self.ts_sum(self.daily_returns, 10) / self.ts_sum(self.ts_sum(self.daily_returns, 2), 3))) * self.rank((self.daily_returns * self.cap))))

    def alpha_057(self):
        """
        # Alpha#57	 (0 - (1 * ((close - vwap) / decay_linear(rank(ts_argmax(close, 30)), 2))))

        Returns:

        """
        return 0 - (1 * ((self.close - self.vwap) / self.decay_linear(self.rank(self.ts_argmax(self.close, 30)), 2)))

    def alpha_058(self):
        """
        # Alpha#58	 (-1 * Ts_Rank(decay_linear(correlation(IndNeutralize(vwap, IndClass.sector), volume,3.92795), 7.89291), 5.50322))

        Returns:

        """
        return -1 * self.ts_rank(self.decay_linear(self.correlation(self.indneutralize(self.vwap, self.ind_mapping), self.volume, 4), 8), 6)

    def alpha_059(self):
        """
        # Alpha#59	 (-1 * Ts_Rank(decay_linear(correlation(IndNeutralize(((vwap * 0.728317) + (vwap *(1 - 0.728317))), IndClass.industry), volume, 4.25197), 16.2289), 8.19648))

        Returns:

        """
        return -1 * self.ts_rank(self.decay_linear(self.correlation(self.indneutralize((self.vwap * 0.728317) + (self.vwap * (1 - 0.728317)), self.ind_mapping), self.volume, 4), 16), 8)

    def alpha_060(self):
        """
        # Alpha#60
        (0 - (1 * ((2 * scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)))) -scale(rank(ts_argmax(close, 10))))))

        Returns:

        """
        return - ((2 * self.scale(self.rank((((self.close - self.low) - (self.high - self.close)) / (self.high - self.low)) * self.volume))) - self.scale(self.rank(self.ts_argmax(self.close, 10))))

    def alpha_061(self):
        """
        # Alpha#61	 (rank((vwap - ts_min(vwap, 16.1219))) < rank(correlation(vwap, adv180, 17.9282)))

        Returns:

        """
        adv180 = self.sma(self.volume, 180)
        return self.rank((self.vwap - self.ts_min(self.vwap, 16))) < self.rank(self.correlation(self.vwap, adv180, 18))

    def alpha_062(self):
        """
        # Alpha#62
        ((rank(correlation(vwap, sum(adv20, 22.4101), 9.91009)) < rank(((rank(open) +rank(open)) < (rank(((high + low) / 2)) + rank(high))))) * -1)

        Returns:

        """
        adv20 = self.sma(self.volume, 20)
        part_a = self.rank(self.correlation(self.vwap, self.ts_sum(adv20, 22), 10))
        part_b = self.rank((((self.rank(self.open) + self.rank(self.open)) < (self.rank(((self.high + self.low) / 2)) + self.rank(self.high)))))
        return (part_a < part_b) * -1

    def alpha_063(self):
        """
        # Alpha#63
        ((rank(decay_linear(delta(IndNeutralize(close, IndClass.industry), 2.25164), 8.22237))- rank(decay_linear(correlation(((vwap * 0.318108) + (open * (1 - 0.318108))), sum(adv180,37.2467), 13.557), 12.2883))) * -1)

        Returns:

        """
        adv180 = self.sma(self.volume, 180)
        part_a = self.rank(self.decay_linear(self.delta(self.indneutralize(self.close, self.ind_mapping), 2), 8))
        part_b = self.rank(self.decay_linear(self.correlation(((self.vwap * 0.318108) + (self.open * (1 - 0.318108))), self.ts_sum(adv180, 37), 14), 12))
        return (part_a - part_b) * -1

    def alpha_064(self):
        """
        # Alpha#64
        ((rank(correlation(sum(((open * 0.178404) + (low * (1 - 0.178404))), 12.7054),sum(adv120, 12.7054), 16.6208)) < rank(delta(((((high + low) / 2) * 0.178404) + (vwap * (1 -0.178404))), 3.69741))) * -1)

        Returns:

        """
        adv120 = self.sma(self.volume, 120)
        part_a = self.rank(self.correlation(self.ts_sum(((self.open * 0.178404) + (self.low * (1 - 0.178404))), 13), self.ts_sum(adv120, 13), 17))
        part_b = self.rank(self.delta(((self.high + self.low) / 2) * 0.178404 + self.vwap * (1 - 0.178404), 4))
        return (part_a - part_b) * -1

    def alpha_065(self):
        """
        # Alpha#65	 ((rank(correlation(((open * 0.00817205) + (vwap * (1 - 0.00817205))), sum(adv60,8.6911), 6.40374)) < rank((open - ts_min(open, 13.635)))) * -1)

        Returns:

        """
        adv60 = self.sma(self.volume, 60)
        part_a = self.rank(self.correlation(((self.open * 0.00817205) + (self.vwap * (1 - 0.00817205))), self.ts_sum(adv60, 9), 6))
        part_b = self.rank(self.ts_min(self.open, 14))
        return (part_a < part_b) * -1

    def alpha_066(self):
        """
        # Alpha#66
        ((rank(decay_linear(delta(vwap, 3.51013), 7.23052)) + Ts_Rank(decay_linear(((((low* 0.96633) + (low * (1 - 0.96633))) - vwap) / (open - ((high + low) / 2))), 11.4157), 6.72611)) * -1)

        Returns:

        """
        part_a = self.rank(self.decay_linear(self.delta(self.vwap, 4), 7))
        part_b = self.ts_rank(self.decay_linear(((((self.low * 0.96633) + (self.low * (1 - 0.96633))) - self.vwap) / (self.open - ((self.high + self.low) / 2))), 11), 7)
        return (part_a + part_b) * -1

    def alpha_067(self):
        """
        todo: IndClass.sector or IndClass.subindustry
        # Alpha#67
        ((rank((high - ts_min(high, 2.14593)))^rank(correlation(IndNeutralize(vwap,IndClass.sector), IndNeutralize(adv20, IndClass.subindustry), 6.02936))) * -1)

        Returns:

        """
        adv20 = self.sma(self.volume, 20)
        part_a = self.rank(self.high - self.ts_min(self.high, 2))
        part_b = self.rank(self.correlation(self.indneutralize(self.vwap, self.ind_mapping), self.indneutralize(adv20, self.ind_mapping), 6))
        return (part_a.pow(part_b)) * -1


    def alpha_068(self):
        """
        # Alpha#68
        ((Ts_Rank(correlation(rank(high), rank(adv15), 8.91644), 13.9333) <rank(delta(((close * 0.518371) + (low * (1 - 0.518371))), 1.06157))) * -1)

        Returns:

        """
        adv15 = self.sma(self.volume, 15)
        part_a = self.ts_rank(self.correlation(self.rank(self.high), self.rank(adv15), 9), 14)
        part_b = self.rank(self.delta(((self.close * 0.518371) + (self.low * (1 - 0.518371))), 1))
        return (part_a < part_b) * -1

    def alpha_069(self):
        """
        # Alpha#69
        ((rank(ts_max(delta(IndNeutralize(vwap, IndClass.industry), 2.72412),4.79344))^Ts_Rank(correlation(((close * 0.490655) + (vwap * (1 - 0.490655))), adv20, 4.92416),9.0615)) * -1)

        Returns:

        """
        part_a = self.rank(self.ts_max(self.delta(self.indneutralize(self.vwap, self.ind_mapping), 3), 5))
        part_b = self.ts_rank(self.correlation(((self.close * 0.490655) + (self.vwap * (1 - 0.490655))), self.sma(self.volume, 20), 4), 9)
        return (part_a.pow(part_b)) * -1


    def alpha_070(self):
        """
        # Alpha#70
        ((rank(delta(vwap, 1.29456))^Ts_Rank(correlation(IndNeutralize(close,IndClass.industry), adv50, 17.8256), 17.9171)) * -1)

        Returns:

        """
        part_a = self.rank(self.delta(self.vwap, 1))
        part_b = self.ts_rank(self.correlation(self.indneutralize(self.close, self.ind_mapping), self.sma(self.volume, 50), 18), 18)
        return (part_a.pow(part_b)) * -1

    def alpha_071(self):
        """
        # Alpha#71
        max(Ts_Rank(decay_linear(correlation(Ts_Rank(close, 3.43976), Ts_Rank(adv180,12.0647), 18.0175), 4.20501), 15.6948), Ts_Rank(decay_linear((rank(((low + open) - (vwap +vwap)))^2), 16.4662), 4.4388))

        Returns:

        """
        adv180 = self.sma(self.volume, 180)
        part_a = self.ts_rank(self.decay_linear(self.correlation(self.ts_rank(self.close, 3), self.ts_rank(adv180, 12), 18), 4), 16)
        part_b = self.ts_rank(self.decay_linear(self.rank((self.low + self.open) - (self.vwap + self.vwap)).pow(2), 16), 4)
        return part_a.where(part_a > part_b, part_b)

    def alpha_072(self):
        """
        # Alpha#72
        (rank(decay_linear(correlation(((high + low) / 2), adv40, 8.93345), 10.1519)) /rank(decay_linear(correlation(Ts_Rank(vwap, 3.72469), Ts_Rank(volume, 18.5188), 6.86671),2.95011)))

        Returns:

        """
        adv40 = self.sma(self.volume, 40)
        part_a = self.rank(self.decay_linear(self.correlation((self.high + self.low) / 2, adv40, 9), 10))
        part_b = self.rank(self.decay_linear(self.correlation(self.ts_rank(self.vwap, 4), self.ts_rank(self.volume, 19), 7), 3))
        return part_a / part_b

    def alpha_073(self):
        """
        # Alpha#73
        (max(rank(decay_linear(delta(vwap, 4.72775), 2.91864)),Ts_Rank(decay_linear(((delta(((open * 0.147155) + (low * (1 - 0.147155))), 2.03608) / ((open *0.147155) + (low * (1 - 0.147155)))) * -1), 3.33829), 16.7411)) * -1)

        Returns:
        """
        part_a = self.rank(self.decay_linear(self.delta(self.vwap, 5), 3))
        part_b = self.ts_rank(self.decay_linear((self.delta(((self.open * 0.147155) + (self.low * (1 - 0.147155))), 2) / ((self.open * 0.147155) + (self.low * (1 - 0.147155)))) * -1, 3), 17)
        return part_a.where(part_a > part_b, part_b) * -1

    def alpha_074(self):
        """
        # Alpha#74
        ((rank(correlation(close, sum(adv30, 37.4843), 15.1365)) <rank(correlation(rank(((high * 0.0261661) + (vwap * (1 - 0.0261661)))), rank(volume), 11.4791)))* -1)

        Returns:

        """
        adv30 = self.sma(self.volume, 30)
        part_a = self.rank(self.correlation(self.close, self.ts_sum(adv30, 37), 15))
        part_b = self.rank(self.correlation(self.rank((self.high * 0.0261661) + (self.vwap * (1 - 0.0261661))), self.rank(self.volume), 11))
        return (part_a < part_b) * -1

    def alpha_075(self):
        """
        # Alpha#75
        (rank(correlation(vwap, volume, 4.24304)) < rank(correlation(rank(low), rank(adv50),12.4413)))

        Returns:

        """
        adv50 = self.sma(self.volume, 50)
        part_a = self.rank(self.correlation(self.vwap, self.volume, 4))
        part_b = self.rank(self.correlation(self.rank(self.low), self.rank(adv50), 12))
        return part_a < part_b


    def alpha_076(self):
        """
        # Alpha#76
        (max(rank(decay_linear(delta(vwap, 1.24383), 11.8259)),Ts_Rank(decay_linear(Ts_Rank(correlation(IndNeutralize(low, IndClass.sector), adv81,8.14941), 19.569), 17.1543), 19.383)) * -1)

        Returns:

        """
        adv81 = self.sma(self.volume, 81)
        part_a = self.rank(self.decay_linear(self.delta(self.vwap, 2), 12))
        part_b = self.ts_rank(self.decay_linear(self.ts_rank(self.correlation(self.indneutralize(self.low, self.ind_mapping), adv81, 8), 20), 17), 19)
        return part_a.where(part_a > part_b, part_b) * -1

    def alpha_077(self):
        """
        # Alpha#77
        min(rank(decay_linear(((((high + low) / 2) + high) - (vwap + high)), 20.0451)),rank(decay_linear(correlation(((high + low) / 2), adv40, 3.1614), 5.64125)))

        Returns:

        """
        adv40 = self.sma(self.volume, 40)
        part_a = self.rank(self.decay_linear((((self.high + self.low) / 2) + self.high) - (self.vwap + self.high), 20))
        part_b = self.rank(self.decay_linear(self.correlation(((self.high + self.low) / 2), adv40, 3), 6))
        return part_a.where(part_a < part_b, part_b)

    def alpha_078(self):
        """
        # Alpha#78
        (rank(correlation(sum(((low * 0.352233) + (vwap * (1 - 0.352233))), 19.7428),sum(adv40, 19.7428), 6.83313))^rank(correlation(rank(vwap), rank(volume), 5.77492)))

        Returns:

        """
        adv40 = self.sma(self.volume, 40)
        part_a = self.rank(self.correlation(self.ts_sum((self.low * 0.352233) + (self.vwap * (1 - 0.352233)), 20), self.ts_sum(adv40, 20), 7))
        part_b = self.rank(self.correlation(self.rank(self.vwap), self.rank(self.volume), 6))
        return part_a.pow(part_b)

    def alpha_079(self):
        """
        # Alpha#79
        (rank(delta(IndNeutralize(((close * 0.60733) + (open * (1 - 0.60733))),IndClass.sector), 1.23438)) < rank(correlation(Ts_Rank(vwap, 3.60973), Ts_Rank(adv150,9.18637), 14.6644)))

        Returns:

        """
        part_a = self.rank(self.delta(self.indneutralize(((self.close * 0.60733) + (self.open * (1 - 0.60733))), self.ind_mapping), 2))
        part_b = self.rank(self.correlation(self.ts_rank(self.vwap, 4), self.ts_rank(self.sma(self.volume, 150), 10), 15))
        return part_a < part_b

    def alpha_080(self):
        """
        # Alpha#80
        ((rank(Sign(delta(IndNeutralize(((open * 0.868128) + (high * (1 - 0.868128))),IndClass.industry), 4.04545)))^Ts_Rank(correlation(high, adv10, 5.11456), 5.53756)) * -1)

        Returns:

        """
        part_a = self.rank((self.delta(self.indneutralize(((self.open * 0.868128) + (self.high * (1 - 0.868128))), self.ind_mapping), 5)).apply(np.sign))
        part_b = self.ts_rank(self.correlation(self.high, self.sma(self.volume, 10), 6), 6)
        return part_a.pow(part_b) * -1

    def alpha_081(self):
        """
        # Alpha#81
        ((rank(Log(product(rank((rank(correlation(vwap, sum(adv10, 49.6054),8.47743))^4)), 14.9655))) < rank(correlation(rank(vwap), rank(volume), 5.07914))) * -1)

        Returns:

        """
        adv10 = self.sma(self.volume, 50)
        corr = self.correlation(self.vwap, self.ts_sum(adv10, 50), 8)
        part_a = self.rank(self.log(self.product(self.rank(corr).pow(4), 15)))
        part_b = self.rank(self.correlation(self.rank(self.vwap), self.rank(self.volume), 6))
        return (part_a < part_b) * -1

    def alpha_082(self):
        """
        # Alpha#82
        (min(rank(decay_linear(delta(open, 1.46063), 14.8717)),Ts_Rank(decay_linear(correlation(IndNeutralize(volume, IndClass.sector), ((open * 0.634196) +(open * (1 - 0.634196))), 17.4842), 6.92131), 13.4283)) * -1)

        Returns:

        """
        part_a = self.rank(self.decay_linear(self.delta(self.open, 2), 15))
        part_b = self.ts_rank(self.decay_linear(self.correlation(self.indneutralize(self.volume, self.ind_mapping), self.open, 18), 7), 13)
        return part_a.where(part_a < part_b, part_b) * -1

    def alpha_083(self):
        """
        # Alpha#83
        ((rank(delay(((high - low) / (sum(close, 5) / 5)), 2)) * rank(rank(volume))) / (((high -low) / (sum(close, 5) / 5)) / (vwap - close)))

        Returns:

        """
        part_a = self.rank(self.delay((self.high - self.low) / self.sma(self.close,5), 2))
        part_b = self.rank(self.rank(self.volume))
        return (part_a * part_b) / ((self.high - self.low) / (self.sma(self.close,5)) / (self.vwap - self.close))

    def alpha_084(self):
        """
        # Alpha#84	 SignedPower(Ts_Rank((vwap - ts_max(vwap, 15.3217)), 20.7127), delta(close,4.96796))

        Returns:

        """
        part_a = self.ts_rank(self.vwap - self.ts_max(self.vwap, 15), 21)
        part_b = self.delta(self.close, 5)
        return self.sign_pow(part_a, part_b)

    def alpha_085(self):
        """
        # Alpha#85
        (rank(correlation(((high * 0.876703) + (close * (1 - 0.876703))), adv30,9.61331))^
        rank(correlation(Ts_Rank(((high + low) / 2), 3.70596), Ts_Rank(volume, 10.1595),7.11408)))

        Returns:

        """
        part_a = self.rank(self.correlation(((self.high * 0.876703) + (self.close * (1 - 0.876703))), self.sma(self.volume, 30), 10))
        part_b = self.rank(self.correlation(self.ts_rank(((self.high + self.low) / 2), 4), self.ts_rank(self.volume, 10), 7))
        return part_a.pow(part_b)

    def alpha_086(self):
        """
        # Alpha#86	 ((Ts_Rank(correlation(close, sum(adv20, 14.7444), 6.00049), 20.4195) < rank(((open+ close) - (vwap + open)))) * -1)

        Returns:

        """
        adv20 = self.sma(self.volume, 20)
        part_a = self.ts_rank(self.correlation(self.close, self.ts_sum(adv20, 15), 6), 20)
        part_b = self.rank(((self.open + self.close) - (self.vwap + self.open)))
        return (part_a < part_b) * -1

    def alpha_087(self):
        """
        # Alpha#87
        (max(rank(decay_linear(delta(((close * 0.369701) + (vwap * (1 - 0.369701))),1.91233), 2.65461)),
        Ts_Rank(decay_linear(abs(correlation(IndNeutralize(adv81,IndClass.industry), close, 13.4132)), 4.89768), 14.4535)) * -1)

        Returns:

        """
        adv81 = self.sma(self.volume, 81)
        corr = self.correlation(self.indneutralize(adv81, self.ind_mapping), self.close, 13)
        part_a = self.rank(self.decay_linear(self.delta(((self.close * 0.369701) + (self.vwap * (1 - 0.369701))), 2), 3))
        part_b = self.ts_rank(self.decay_linear(corr.abs(), 5), 14)
        return part_a.where(part_a > part_b, part_b) * -1

    def alpha_088(self):
        """
        # Alpha#88
        min(rank(decay_linear(((rank(open) + rank(low)) - (rank(high) + rank(close))),8.06882)),
        Ts_Rank(decay_linear(correlation(Ts_Rank(close, 8.44728), Ts_Rank(adv60,20.6966), 8.01266), 6.65053), 2.61957))

        Returns:

        """
        adv60 = self.sma(self.volume, 60)
        part_a = self.rank(self.decay_linear(self.rank(self.open) + self.rank(self.low) - self.rank(self.high) - self.rank(self.close), 8))
        part_b = self.ts_rank(self.decay_linear(self.correlation(self.ts_rank(self.close, 8), self.ts_rank(adv60, 21), 8), 7), 3)
        return part_a.where(part_a < part_b, part_b)

    def alpha_089(self):
        """
        # Alpha#89
        (Ts_Rank(decay_linear(correlation(((low * 0.967285) + (low * (1 - 0.967285))), adv10,6.94279), 5.51607), 3.79744)
        - Ts_Rank(decay_linear(delta(IndNeutralize(vwap,IndClass.industry), 3.48158), 10.1466), 15.3012))

        Returns:

        """
        adv10 = self.sma(self.volume, 10)
        part_a = self.ts_rank(self.decay_linear(self.correlation(self.low, adv10, 7), 6), 4)
        part_b = self.ts_rank(self.decay_linear(self.delta(self.indneutralize(self.vwap, self.ind_mapping), 3), 10), 15)
        return part_a - part_b

    def alpha_090(self):
        """
        # Alpha#90	 ((rank((close - ts_max(close, 4.66719)))^Ts_Rank(correlation(IndNeutralize(adv40,IndClass.subindustry), low, 5.38375), 3.21856)) * -1)

        Returns:

        """
        adv40 = self.sma(self.volume, 40)
        part_a = self.rank(self.close - self.ts_max(self.close, 5))
        part_b = self.ts_rank(self.correlation(self.indneutralize(adv40, self.ind_mapping), self.low, 5), 3)
        return part_a.pow(part_b) * -1

    def alpha_091(self):
        """
        # Alpha#91
        ((Ts_Rank(decay_linear(decay_linear(correlation(IndNeutralize(close,IndClass.industry), volume, 9.74928), 16.398), 3.83219), 4.8667)
        -rank(decay_linear(correlation(vwap, adv30, 4.01303), 2.6809))) * -1)

        Returns:

        """
        part_a = self.ts_rank(self.decay_linear(self.decay_linear(self.correlation(self.indneutralize(self.close, self.ind_mapping), self.volume, 10), 16), 4), 5)
        part_b = self.rank(self.decay_linear(self.correlation(self.vwap, self.sma(self.volume, 30), 4), 3))
        return part_b - part_a

    def alpha_092(self):
        """
        # Alpha#92
        min(Ts_Rank(decay_linear(((((high + low) / 2) + close) < (low + open)), 14.7221),18.8683), Ts_Rank(decay_linear(correlation(rank(low), rank(adv30), 7.58555), 6.94024),6.80584))

        Returns:

        """
        part_a = self.ts_rank(self.decay_linear((((self.high +self.low) / 2) + self.close) < (self.low + self.open), 15), 19)
        part_b = self.ts_rank(self.decay_linear(self.correlation(self.rank(self.low), self.rank(self.sma(self.volume, 30)), 8), 7), 7)
        return part_a.where(part_a < part_b, part_b)

    def alpha_093(self):
        """
        # Alpha#93
        (Ts_Rank(decay_linear(correlation(IndNeutralize(vwap, IndClass.industry), adv81,17.4193), 19.848), 7.54455) / rank(decay_linear(delta(((close * 0.524434) + (vwap * (1 -0.524434))), 2.77377), 16.2664)))

        Returns:

        """
        adv81 = self.sma(self.volume, 81)
        part_a = self.ts_rank(self.decay_linear(self.correlation(self.indneutralize(self.vwap, self.ind_mapping), adv81, 17), 20), 8)
        part_b = self.rank(self.decay_linear(self.delta(((self.close * 0.524434) + (self.vwap * (1 - 0.524434))), 3), 16))
        return part_a / part_b

    def alpha_094(self):
        """
        # Alpha#94
        ((rank((vwap - ts_min(vwap, 11.5783)))^Ts_Rank(correlation(Ts_Rank(vwap,19.6462), Ts_Rank(adv60, 4.02992), 18.0926), 2.70756)) * -1)

        Returns:

        """
        adv60 = self.sma(self.volume, 60)
        part_a = self.rank(self.vwap - self.ts_min(self.vwap, 12))
        part_b = self.ts_rank(self.correlation(self.ts_rank(self.vwap, 20), self.ts_rank(adv60, 4), 19), 3)
        return part_a.pow(part_b) * -1

    def alpha_095(self):
        """
        # Alpha#95
        (rank((open - ts_min(open, 12.4105))) < Ts_Rank((rank(correlation(sum(((high + low)/ 2), 19.1351), sum(adv40, 19.1351), 12.8742))^5), 11.7584))

        Returns:

        """
        adv40 = self.sma(self.volume, 40)
        part_a = self.rank(self.open - self.ts_min(self.open, 12))
        part_b = self.ts_rank(self.rank(self.correlation(self.ts_sum((self.high + self.low) / 2, 19), self.ts_sum(adv40, 19), 13)).pow(5), 12)
        return part_a < part_b

    def alpha_096(self):
        """
        # Alpha#96
        (max(Ts_Rank(decay_linear(correlation(rank(vwap), rank(volume), 3.83878),4.16783), 8.38151), Ts_Rank(decay_linear(Ts_ArgMax(correlation(Ts_Rank(close, 7.45404),Ts_Rank(adv60, 4.13242), 3.65459), 12.6556), 14.0365), 13.4143)) * -1)

        Returns:

        """
        adv60 = self.sma(self.volume, 60)
        part_a = self.ts_rank(self.decay_linear(self.correlation(self.rank(self.vwap), self.rank(self.volume), 4), 4), 8)
        part_b = self.ts_rank(self.decay_linear(self.ts_argmax(self.correlation(self.ts_rank(self.close, 7), self.ts_rank(adv60, 4), 4), 13), 14), 13)
        return -1 * part_a.where(part_a > part_b, part_b)

    def alpha_097(self):
        """
        # Alpha#97
        (
            rank(
                decay_linear(
                    delta(
                        IndNeutralize(
                            ((low * 0.721001) + (vwap * (1 - 0.721001))),
                            IndClass.industry
                        ),
                        3.3705
                    ),
                    20.4523
                )
            )
            -
            Ts_Rank(
                decay_linear(
                    Ts_Rank(
                        correlation(
                            Ts_Rank(low, 7.87871),
                            Ts_Rank(adv60, 17.255),
                            4.97547
                        ),
                        18.5925
                    ),
                    15.7152
                ),
                6.71659
            )
        ) * -1
        Returns:

        """
        adv60 = self.sma(self.volume, 60)
        # rank(decay_linear(delta(IndNeutralize((low*0.721 + vwap*0.279), industry), 3), 20))
        part_a = self.rank(self.decay_linear(self.delta(self.indneutralize((self.low * 0.721 + self.vwap * (1 - 0.721)), self.ind_mapping), 3), 20))
        part_b = self.ts_rank(self.decay_linear(self.ts_rank(self.correlation(self.ts_rank(self.low, 8), self.ts_rank(adv60, 17), 5), 19), 16), 7)
        return -1 * (part_a - part_b)

    def alpha_098(self):
        """
        # Alpha#98
        (rank(decay_linear(correlation(vwap, sum(adv5, 26.4719), 4.58418), 7.18088)) -rank(decay_linear(Ts_Rank(Ts_ArgMin(correlation(rank(open), rank(adv15), 20.8187), 8.62571),6.95668), 8.07206)))

        Returns:

        """
        adv5 = self.sma(self.volume, 5)
        adv15 = self.sma(self.volume, 15)
        part_a = self.rank(self.decay_linear(self.correlation(self.vwap, self.ts_sum(adv5, 26), 5), 7))
        part_b = self.rank(self.decay_linear(self.ts_rank(self.ts_argmin(self.correlation(self.rank(self.open), self.rank(adv15), 21), 8), 7), 8))
        return part_a - part_b

    def alpha_099(self):
        """
        # Alpha#99 ((rank(correlation(sum(((high + low) / 2), 19.8975), sum(adv60, 19.8975), 8.8136)) <rank(correlation(low, volume, 6.28259))) * -1)

        Returns:

        """
        adv60 = self.sma(self.volume, 60)
        part_a = self.rank(self.correlation(self.ts_sum((self.high + self.low) / 2, 20), self.ts_sum(adv60, 20), 9))
        part_b = self.rank(self.correlation(self.low, self.volume, 6))
        return (part_a < part_b) * -1

    def alpha_100(self):
        """
        # Alpha#100
        (0 - (
            1 * (
                (
                    1.5 * scale(
                        indneutralize(
                            indneutralize(
                                rank(
                                    ((((close - low) - (high - close)) / (high - low)) * volume
                                ),
                                IndClass.subindustry
                            ),
                            IndClass.subindustry
                        )
                    )
                )
                -
                scale(
                    indneutralize(
                        (correlation(close, rank(adv20), 5) - rank(ts_argmin(close, 30))),
                        IndClass.subindustry
                    )
                )
            )
            *
            (volume / adv20)
        ))

        Returns:

        """
        adv20 = self.sma(self.volume, 20)
        part_a = self.rank(((2 * self.close - self.low - self.high) / (self.high - self.low)) * self.volume)
        part_b = self.correlation(self.close, self.rank(adv20), 5) - self.rank(self.ts_argmin(self.close, 30))
        part_c = 1.5 * self.scale(self.indneutralize(self.indneutralize(part_a, self.ind_mapping), self.ind_mapping))
        part_d = self.scale(self.indneutralize(part_b, self.ind_mapping))
        return (part_c - part_d) * (self.volume / adv20)

    def alpha_101(self):
        """
        # Alpha#101 ((close - open) / ((high - low) + .001))

        Returns:

        """
        return (self.close - self.open) / (self.high - self.low + 0.001)
