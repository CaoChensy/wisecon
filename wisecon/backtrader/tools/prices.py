import numpy as np
import pandas as pd
from typing import Optional


__all__ = [
    "RollingPricesIndex",
]


class RollingPricesIndex:
    """"""
    def __init__(
            self,
            prices: pd.Series,
            window: int = 252,
            risk_free_rate: float = 0.03,
            benchmark: Optional[pd.Series] = None,
    ):
        """周期滚动价格指数

        Args:
            prices: 价格序列
            window: 滚动周期
            risk_free_rate: 无风险利率（如3% → 0.03）
            benchmark: 基准价格序列
        """
        self.prices = prices
        self.window = window
        self.risk_free_rate = risk_free_rate
        self.benchmark = benchmark

    def __call__(self, *args, **kwargs) -> pd.DataFrame:
        """"""
        return self.call()
        
    def cumulative_return(self) -> pd.Series:
        """滚动累计收益率（实际1年收益）"""
        return (self.prices / self.prices.shift(self.window)) - 1
    
    def volatility(self,) -> pd.Series:
        """计算年滚动波动率（年化标准差）"""
        # 计算日收益率
        daily_returns = self.prices.pct_change()
        # 滚动波动率（年化）
        volatility = daily_returns.rolling(window=self.window).std() * np.sqrt(self.window)
        return volatility

    def sharpe_ratio(self,) -> pd.Series:
        """计算年滚动夏普比率"""
        if self.risk_free_rate is None:
            raise ValueError("risk_free_rate is None")

        # 计算日收益率
        daily_returns = self.prices.pct_change()
        # 滚动年化收益
        annualized_return = daily_returns.rolling(window=self.window).mean() * self.window
        # 滚动年化波动率
        volatility = daily_returns.rolling(window=self.window).std() * np.sqrt(self.window)
        # 滚动夏普比率
        sharpe = (annualized_return - self.risk_free_rate) / volatility
        return sharpe

    def max_drawdown(self,) -> pd.Series:
        """计算滚动最大回撤"""
        max = self.prices.rolling(window=self.window).max()
        drawdown = (self.prices / max) - 1
        mdd = drawdown.rolling(window=self.window).min()
        return mdd

    def sortino_ratio(self,) -> pd.Series:
        """计算滚动索提诺比率（Sortino Ratio），仅考虑下行风险（负收益）的夏普比率变体，适合风险厌恶型投资者。"""

        if self.risk_free_rate is None:
            raise ValueError("risk_free_rate is None")

        daily_returns = self.prices.pct_change()
        # 下行波动率（仅负收益）
        downside_returns = daily_returns[daily_returns < 0].reindex(daily_returns.index, fill_value=0)
        downside_vol = downside_returns.rolling(window=self.window).std() * np.sqrt(self.window)
        # 滚动年化收益
        annualized_return = daily_returns.rolling(window=self.window).mean() * self.window
        # 索提诺比率
        sortino = (annualized_return - self.risk_free_rate) / downside_vol
        return sortino

    def calmar_ratio(self) -> pd.Series:
        """
        计算滚动Calmar比率

        参数:
        - price_series: pandas Series, 价格序列
        - window: 滚动窗口天数

        返回:
        - calmar: pandas Series, 滚动Calmar比率
        """
        # 滚动年化收益
        daily_returns = self.prices.pct_change()
        annualized_return = daily_returns.rolling(window=self.window).mean() * self.window
        # 滚动最大回撤
        mdd = self.max_drawdown()
        # Calmar比率
        calmar = annualized_return / (-mdd)
        return calmar
    
    def win_rate(self) -> pd.Series:
        """计算滚动胜率（正收益占比）"""
        daily_returns = self.prices.pct_change()
        win = (daily_returns > 0).rolling(window=self.window).sum() / self.window
        return win

    def profit_loss_ratio(self) -> pd.Series:
        """计算滚动盈亏比（Profit Loss Ratio），衡量每笔盈利交易的平均盈利与平均亏损的比例。"""
        daily_returns = self.prices.pct_change()
        # 平均盈利
        avg_gain = daily_returns[daily_returns > 0].rolling(window=self.window).mean()
        # 平均亏损（取绝对值）
        avg_loss = -daily_returns[daily_returns < 0].rolling(window=self.window).mean()
        # 盈亏比
        pl_ratio = avg_gain / avg_loss
        return pl_ratio

    def volatility_adjusted_return(self, ) -> pd.Series:
        """计算滚动波动率调整收益（收益/波动率）"""
        # 滚动年化收益
        daily_returns = self.prices.pct_change()
        annualized_return = daily_returns.rolling(window=self.window).mean() * self.window
        # 滚动年化波动率
        vol = self.volatility()
        # 波动率调整收益
        var = annualized_return / vol
        return var

    def correlation(self,) -> pd.Series:
        """
        计算资产与基准的滚动相关系数
        """
        if self.benchmark is None:
            raise ValueError("Benchmark is not provided.")

        returns = self.prices.pct_change()
        bench_returns = self.benchmark.pct_change()
        corr = returns.rolling(window=self.window).corr(bench_returns)
        return corr

    def skew(self,) -> pd.Series:
        """
        计算滚动年化偏度与峰度

        返回:
        - skew: pandas Series, 滚动偏度
        """
        daily_returns = self.prices.pct_change()
        skew = daily_returns.rolling(window=self.window).skew()
        return skew

    def kurtosis(self, ) -> pd.Series:
        """
        计算滚动年化偏度与峰度

        返回:
        - kurt: pandas Series, 滚动峰度
        """
        daily_returns = self.prices.pct_change()
        kurt = daily_returns.rolling(window=self.window).kurt()
        return kurt

    def beta(self,) -> pd.Series:
        """
        计算滚动Beta（系统性风险）
        """
        if self.benchmark is None:
            raise ValueError("Benchmark is not provided.")

        returns = self.prices.pct_change().dropna()
        bench_returns = self.benchmark.pct_change().dropna()
    
        def calc_beta(asset_rets, bench_rets):
            cov_matrix = np.cov(asset_rets, bench_rets)
            return cov_matrix[0, 1] / cov_matrix[1, 1]
    
        beta = pd.Series(index=returns.index)
        for i in range(self.window, len(returns)):
            window_asset = returns.iloc[i - self.window:i]
            window_bench = bench_returns.iloc[i - self.window:i]
            beta.iloc[i] = calc_beta(window_asset, window_bench)
        return beta

    def alpha(self,) -> pd.Series:
        """
        计算滚动Alpha（超额收益）
        """
        if self.risk_free_rate is None:
            raise ValueError("risk_free_rate must be provided to calculate alpha")

        if self.benchmark is None:
            raise ValueError("Benchmark is not provided.")

        returns = self.prices.pct_change().dropna()
        bench_returns = self.benchmark.pct_change().dropna()
        beta = self.beta()
        alpha = returns - (self.risk_free_rate / 252 + beta * (bench_returns - self.risk_free_rate / 252))
        return alpha.rolling(window=self.window).mean() * 252  # 年化

    def call(self) -> pd.DataFrame:
        """"""
        base_index = {
            "return": self.cumulative_return(),
            "volatility": self.volatility(),
            "max_drawdown": self.max_drawdown(),
            "win_rate": self.win_rate(),
            "profit_loss_ratio": self.profit_loss_ratio(),
            "volatility_adjusted_return": self.volatility_adjusted_return(),
            "skew": self.skew(),
            "kurtosis": self.kurtosis(),
            "calmar_ratio": self.calmar_ratio(),
        }

        if self.risk_free_rate is not None:
            base_index.update({
                "sharpe": self.sharpe_ratio(),
                "sortino_ratio": self.sortino_ratio(),
            })

        if self.benchmark is not None:
            base_index.update({
                "correlation": self.correlation(),
                "beta": self.beta(),
            })

        if self.risk_free_rate is not None and self.benchmark is not None:
            base_index.update({
                "alpha": self.alpha(),
            })
        return pd.DataFrame(base_index)
