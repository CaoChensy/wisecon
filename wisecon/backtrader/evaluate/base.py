import numpy as np
import pandas as pd
from typing import Dict, Literal, Optional
import statsmodels.api as sm

__all__ = [
    "alpha_beta_ols",
    "PriceIndexEvaluator",
]


def alpha_beta_ols(
        prices: pd.Series,
        benchmark: pd.Series,
        risk_free_rate: Optional[float] = 0.03,
        daily_rf_type: Literal["mean", "compound"] = "compound"
) -> Dict[str, float]:
    """Calculate the alpha of a stock using the OLS regression method.

    Args:
        prices: The prices of the stock.
        benchmark: The prices of the benchmark.
        risk_free_rate: The risk-free rate of return.
        daily_rf_type: The type of daily risk-free rate to use.

    Returns:
        A DataFrame with columns 'alpha' and 'beta'.
    """
    if risk_free_rate is None:
        raise ValueError("risk_free_rate must be provided to calculate alpha")
    if benchmark is None:
        raise ValueError("Benchmark is not provided.")

    n = len(prices)
    if daily_rf_type == "mean":
        daily_rf = risk_free_rate / n
    elif daily_rf_type == "compound":
        daily_rf = (1 + risk_free_rate) ** (1 / n) - 1
    else:
        raise ValueError("Invalid daily_rf_type. Choose 'mean' or 'compound'.")

    returns = prices.pct_change()
    bench_returns = benchmark.pct_change()

    # Align the indices in case they don't match
    common_index = returns.index.intersection(bench_returns.index)
    returns = returns[common_index]
    bench_returns = bench_returns[common_index]

    excess_returns = returns - daily_rf
    excess_bench = bench_returns - daily_rf

    cond_inf_na = np.isinf(excess_bench) | np.isinf(excess_returns) | np.isnan(excess_bench) | np.isnan(
        excess_returns)
    excess_returns = excess_returns[~cond_inf_na]
    excess_bench = excess_bench[~cond_inf_na]

    X = sm.add_constant(excess_bench)  # Add intercept
    model = sm.OLS(excess_returns, X).fit()
    return {
        "alpha": model.params.iloc[0] * n,  # Annualized alpha
        "beta": model.params.iloc[1],  # Beta
        "alpha_tstat": model.tvalues.iloc[0],  # Alpha t-statistic
        "beta_tstat": model.tvalues.iloc[1],  # Beta t-statistic
        "r_squared": model.rsquared,  # R-squared
        "p_value_alpha": model.pvalues.iloc[0],  # Alpha p-value
        "p_value_beta": model.pvalues.iloc[1],  # Beta p-value
    }


class PriceIndexEvaluator:
    """周期滚动价格指数计算器

    计算各种滚动窗口金融指标，包括收益率、风险指标和与基准的比较指标。
    """

    def __init__(
            self,
            prices: pd.Series,
            risk_free_rate: float = 0.03,
            benchmark: Optional[pd.Series] = None,
            ols_alpha: Optional[bool] = False,
    ):
        """初始化滚动价格指数计算器

        Args:
            prices: 价格序列，必须是pandas Series
            risk_free_rate: 无风险利率（如3% → 0.03），必须非负
            benchmark: 基准价格序列，可选
            ols_alpha: 是否计算OLS回归的Alpha值，可选
        """
        if not isinstance(prices, pd.Series):
            raise TypeError("prices must be a pandas Series")
        if risk_free_rate < 0:
            raise ValueError("risk_free_rate must be non-negative")
        if benchmark is not None and not isinstance(benchmark, pd.Series):
            raise TypeError("benchmark must be a pandas Series or None")

        self.prices = prices
        self.risk_free_rate = risk_free_rate
        self.benchmark = benchmark
        self.ols_alpha = ols_alpha
        self._daily_returns = None  # 缓存日收益率

    def __call__(self, *args, **kwargs) -> Dict:
        """计算并返回所有可用的滚动指标

        等同于调用call()方法
        """
        return self.evaluate()

    @property
    def daily_returns(self) -> pd.Series:
        """计算并缓存日收益率"""
        if self._daily_returns is None:
            self._daily_returns = self.prices.pct_change().dropna()
        return self._daily_returns

    def cumulative_return(self) -> float:
        """Calculate total cumulative return"""
        return (self.prices.iloc[-1] / self.prices.iloc[0]) - 1

    def annualized_return(self) -> float:
        """Calculate annualized return"""
        n_years = len(self.prices) / 252  # Assuming 252 trading days per year
        return (1 + self.cumulative_return()) ** (1 / n_years) - 1

    def volatility(self) -> float:
        """Calculate volatility"""
        return self.daily_returns.std() * np.sqrt(len(self.prices))

    def sharpe_ratio(self) -> float:
        """Calculate Sharpe ratio"""
        if self.risk_free_rate is None:
            raise ValueError("risk_free_rate is None")
        return (self.cumulative_return() - self.risk_free_rate) / self.volatility()

    def max_drawdown(self) -> float:
        """Calculate maximum drawdown"""
        cumulative_returns = (1 + self.daily_returns).cumprod()
        peak = cumulative_returns.expanding(min_periods=1).max()
        drawdown = (cumulative_returns - peak) / peak
        return drawdown.min()

    def sortino_ratio(self) -> float:
        """Calculate Sortino ratio (only considers downside risk)"""
        if self.risk_free_rate is None:
            raise ValueError("risk_free_rate is None")

        downside_returns = self.daily_returns[self.daily_returns < 0]
        if len(downside_returns) == 0:
            return np.nan
        downside_vol = downside_returns.std() * np.sqrt(len(self.prices))
        return (self.cumulative_return() - self.risk_free_rate) / downside_vol

    def calmar_ratio(self) -> float:
        """计算滚动Calmar比率（年化收益/最大回撤）

        返回:
            pd.Series: Calmar比率序列
        """
        mdd = abs(self.max_drawdown())
        if mdd == 0:
            return np.nan
        return self.annualized_return() / mdd

    def win_rate(self) -> float:
        """Calculate win rate (percentage of positive returns)"""
        return (self.daily_returns > 0).mean()

    def profit_loss_ratio(self) -> float:
        """Calculate profit/loss ratio (average gain / average loss)"""
        gains = self.daily_returns[self.daily_returns > 0]
        losses = self.daily_returns[self.daily_returns < 0]
        if len(losses) == 0:
            return np.nan
        return gains.mean() / abs(losses.mean())

    def skewness(self) -> float:
        """Calculate skewness of returns"""
        return self.daily_returns.skew()

    def kurtosis(self) -> float:
        """Calculate kurtosis of returns"""
        return self.daily_returns.kurtosis()

    def volatility_adjusted_return(self) -> float:
        """Calculate volatility-adjusted return (return/volatility)"""
        return self.cumulative_return() / self.volatility() if self.volatility() != 0 else np.nan

    def beta(self) -> float:
        """Calculate beta (systematic risk)"""
        if self.benchmark is None:
            raise ValueError("Benchmark is not provided.")

        bench_returns = self.benchmark.pct_change().dropna()
        common_index = self.daily_returns.index.intersection(bench_returns.index)
        asset_returns = self.daily_returns[common_index]
        bench_returns = bench_returns[common_index]

        cov = asset_returns.cov(bench_returns)
        bench_var = bench_returns.var()
        if bench_var == 0:
            return np.nan
        return cov / bench_var

    def alpha(self) -> float:
        """Calculate alpha (excess return)"""
        if self.risk_free_rate is None:
            raise ValueError("risk_free_rate must be provided to calculate alpha")
        if self.benchmark is None:
            raise ValueError("Benchmark is not provided.")
        beta = self.beta()
        asset_return = self.cumulative_return()
        bench_return = (self.benchmark.iloc[-1] / self.benchmark.iloc[0]) - 1
        return asset_return - (self.risk_free_rate + beta * (bench_return - self.risk_free_rate))

    def correlation(self) -> float:
        """Calculate correlation with benchmark"""
        if self.benchmark is None:
            raise ValueError("Benchmark is not provided.")

        bench_returns = self.benchmark.pct_change().dropna()
        common_index = self.daily_returns.index.intersection(bench_returns.index)
        return self.daily_returns[common_index].corr(bench_returns[common_index])

    def evaluate(self) -> Dict[str, float]:
        """Calculate and return all available evaluation metrics"""
        metrics: Dict[str, float] = {
            "cumulative_return": self.cumulative_return(),
            "annualized_return": self.annualized_return(),
            "volatility": self.volatility(),
            "volatility_adjusted_return": self.volatility_adjusted_return(),
            "max_drawdown": self.max_drawdown(),
            "win_rate": self.win_rate(),
            "profit_loss_ratio": self.profit_loss_ratio(),
            "sharpe_ratio": self.sharpe_ratio(),
            "sortino_ratio": self.sortino_ratio(),
            "calmar_ratio": self.calmar_ratio(),
            "skewness": self.skewness(),
            "kurtosis": self.kurtosis(),
        }

        if self.benchmark is not None:
            metrics.update({
                "correlation": self.correlation(),
                "beta": self.beta(),
                "alpha": self.alpha(),
            })

        if self.ols_alpha and self.benchmark is not None and self.risk_free_rate is not None:
            ols_results = alpha_beta_ols(
                prices=self.prices,
                benchmark=self.benchmark,
                risk_free_rate=self.risk_free_rate
            )
            metrics.update(ols_results)
        metrics = {key: float(round(val, 6)) for key, val in metrics.items()}
        return metrics
