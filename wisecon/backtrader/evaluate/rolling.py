import numpy as np
import pandas as pd
from typing import Dict, Literal, Optional
import statsmodels.api as sm


__all__ = [
    "rolling_alpha_beta_ols",
    "RollingPricesIndex",
]


def rolling_alpha_beta_ols(
        prices: pd.Series,
        benchmark: pd.Series,
        risk_free_rate: Optional[float] = 0.03,
        window: int = 252,
        daily_rf_type: Literal["mean", "compound"] = "compound"
) -> pd.DataFrame:
    """Calculate the alpha of a stock using the OLS regression method.

        $$ alpha = R_p - left( R_f + beta x (R_b - R_f) right) $$
        - R_p = 资产收益率（`returns`）
        - R_b = 基准收益率（`bench_returns`）
        - R_f = 无风险利率（`risk_free_rate`）
        - beta = 资产的Beta（`beta()`）

        Alpha 衡量超额收益（超出市场和无风险利率的部分），反映投资经理的选股能力。

        Alpha 的典型取值范围

        | Alpha 值（年化） | 金融含义 | 解释 |
        |------------------|---------|------|
        | α > 0 | 正向超额收益（跑赢市场） | 投资组合表现优异 |
        | α = 0 | 无超额收益（与市场一致） | 被动指数基金通常如此 |
        | α < 0 | 负向超额收益（跑输市场） | 投资组合表现不佳 |

        合理范围

        - 优秀基金经理：年化 α ≈ 2%~5%（持续为正已很难得）。
        - 普通基金：α ≈ -1%~1%（扣除费用后接近零）。
        - 指数基金：α ≈ -0.5%~0%（跟踪误差导致小幅偏离）。

        Beta 衡量资产相对于市场（基准）的系统性风险，反映市场波动对资产的影响程度。

        Beta 的典型取值范围

        | Beta 值 | 金融含义 | 适用资产举例 |
        |---------|---------|-------------|
        | β < 0 | 资产与市场负相关（反向波动） | 黄金、国债（某些情况下） |
        | 0 ≤ β < 1 | 资产波动小于市场（防御型） | 公用事业股、消费必需品 |
        | β = 1 | 资产波动等于市场（完全同步） | 宽基指数基金（如沪深300 ETF） |
        | β > 1 | 资产波动大于市场（进攻型） | 科技股、成长股、杠杆ETF |

        Beta 的极端情况

        - β ≈ 0：资产几乎不受市场影响（如国债）。
        - β ≈ 2：资产波动是市场的两倍（如高杠杆ETF）。
        - β < 0：罕见，通常出现在对冲工具或特殊资产（如黄金在某些时期）。

        Alpha 和 Beta 的关系

        - 高 Beta + 高 Alpha：高风险高回报（如成长股）。
        - 低 Beta + 高 Alpha：理想组合（低风险高收益，如优质价值股）。
        - 高 Beta + 低 Alpha：高风险低回报（需避免）。
        - 低 Beta + 低 Alpha：保守但收益平庸（如债券基金）。

        Beta 的稳定性
        - Beta 会随时间变化（如公司业务转型、市场环境变化）。
        - 短期 Beta（如 60 天）波动大，长期 Beta（如 252 天）更稳定。Alpha 的统计显著性

        Alpha 的统计显著性
        - Alpha 可能受运气影响（短期 α 可能不显著）。
        - 需检查 t-statistic（|t| > 2 表示 α 显著不为零）。

        无风险利率的影响
        - 如果无风险利率（risk_free_rate）选择不当，Alpha 可能失真。
        - 中国：可用 10年期国益率（约 2.5%~3.5%）。
        - 美国：可用 3个月国债利率（约 0%~5%，随美联储政策变化）。

        指标	良好标准	预警信号
        Beta	0.5~1.5（常见）	>1.5：极高风险；<0：逆市场
        Alpha	-1%~3%（年化）	>5%：可能过度拟合；< -1%：表现差
        Alpha t-statistic	> 2（良好）	< 1（预警，不显著）
        Beta t-statistic	> 2（良好）	< 1（预警，与市场无关）
        R-squared	0.3~0.8（良好）	< 0.2（预警，模型解释力差）

    Args:
        prices: The prices of the stock.
        benchmark: The prices of the benchmark.
        risk_free_rate: The risk-free rate of return.
        window: The window size for the rolling regression.
        daily_rf_type: The type of daily risk-free rate to use.

    Returns:
        A DataFrame with columns 'alpha' and 'beta'.
    """
    if risk_free_rate is None:
        raise ValueError("risk_free_rate must be provided to calculate alpha")
    if benchmark is None:
        raise ValueError("Benchmark is not provided.")

    if daily_rf_type == "mean":
        daily_rf = risk_free_rate / window
    elif daily_rf_type == "compound":
        daily_rf = (1 + risk_free_rate) ** (1 / window) - 1
    else:
        raise ValueError("Invalid daily_rf_type. Choose 'mean' or 'compound'.")

    returns = prices.pct_change()
    bench_returns = benchmark.pct_change()
    excess_returns = returns - daily_rf
    excess_bench = bench_returns - daily_rf

    columns = ["alpha", "beta", "alpha_tstat", "beta_tstat", "r_squared"]
    df_alpha_beta = pd.DataFrame(index=returns.index, columns=columns, dtype=float)
    for i in range(window - 1, len(returns)):
        window_returns = excess_returns.iloc[i - window + 1:i + 1]
        window_bench = excess_bench.iloc[i - window + 1:i + 1]
        cond_inf_na = np.isinf(window_returns) | np.isinf(window_bench) | np.isnan(window_returns) | np.isnan(window_bench)
        window_returns = window_returns[~cond_inf_na]
        window_bench = window_bench[~cond_inf_na]
        X = sm.add_constant(window_bench)  # 添加截距项
        model = sm.OLS(window_returns, X).fit()
        df_alpha_beta.iloc[i, 0] = model.params.iloc[0] * window  # Alpha
        df_alpha_beta.iloc[i, 1] = model.params.iloc[1]           # Beta
        df_alpha_beta.iloc[i, 2] = model.tvalues.iloc[0]          # Alpha t-statistic
        df_alpha_beta.iloc[i, 3] = model.tvalues.iloc[1]          # Beta t-statistic
        df_alpha_beta.iloc[i, 4] = model.rsquared                 # R-squared
    return df_alpha_beta


class RollingPricesIndex:
    """周期滚动价格指数计算器

    计算各种滚动窗口金融指标，包括收益率、风险指标和与基准的比较指标。
    """
    def __init__(
            self,
            prices: pd.Series,
            window: int = 252,
            risk_free_rate: float = 0.03,
            benchmark: Optional[pd.Series] = None,
            ols_alpha: Optional[bool] = False,
    ):
        """初始化滚动价格指数计算器

        Args:
            prices: 价格序列，必须是pandas Series
            window: 滚动周期，必须为正整数
            risk_free_rate: 无风险利率（如3% → 0.03），必须非负
            benchmark: 基准价格序列，可选
            ols_alpha: 是否计算OLS回归的Alpha值，可选
        """
        if not isinstance(prices, pd.Series):
            raise TypeError("prices must be a pandas Series")
        if window <= 0:
            raise ValueError("window must be positive")
        if risk_free_rate < 0:
            raise ValueError("risk_free_rate must be non-negative")
        if benchmark is not None and not isinstance(benchmark, pd.Series):
            raise TypeError("benchmark must be a pandas Series or None")

        self.prices = prices
        self.window = window
        self.risk_free_rate = risk_free_rate
        self.benchmark = benchmark
        self.ols_alpha = ols_alpha
        self._daily_returns = None  # 缓存日收益率

    def __call__(self, *args, **kwargs) -> pd.DataFrame:
        """计算并返回所有可用的滚动指标

        等同于调用call()方法
        """
        return self.evaluate()

    @property
    def daily_returns(self) -> pd.Series:
        """计算并缓存日收益率"""
        if self._daily_returns is None:
            returns = self.prices.pct_change()
            # Replace infinite values with 0 while preserving NaN
            self._daily_returns = returns.replace([np.inf, -np.inf], 0)
        return self._daily_returns

    def cumulative_return(self) -> pd.Series:
        """滚动累计收益率（实际1年收益）

        返回:
            pd.Series: 滚动窗口累计收益率
        """
        return (self.prices / self.prices.shift(self.window)) - 1
    
    def volatility(self,) -> pd.Series:
        """计算年滚动波动率（年化标准差）

        返回:
            pd.Series: 年化波动率
        """
        return self.daily_returns.rolling(window=self.window).std() * np.sqrt(self.window)

    def sharpe_ratio(self,) -> pd.Series:
        """计算年滚动夏普比率

        返回:
            pd.Series: 夏普比率序列
        """
        if self.risk_free_rate is None:
            raise ValueError("risk_free_rate is None")

        annualized_return = self.daily_returns.rolling(window=self.window).mean() * self.window
        volatility = self.volatility()
        sharpe = (annualized_return - self.risk_free_rate) / volatility
        return sharpe

    def max_drawdown(self,) -> pd.Series:
        """计算滚动最大回撤

        返回:
            pd.Series: 最大回撤序列(负值表示回撤)
        """
        rolling_max = self.prices.rolling(window=self.window, min_periods=1).max()
        drawdown = (self.prices - rolling_max) / rolling_max
        return drawdown

    def sortino_ratio(self,) -> pd.Series:
        """计算滚动索提诺比率（Sortino Ratio）

        仅考虑下行风险（负收益）的夏普比率变体，适合风险厌恶型投资者。

        返回:
            pd.Series: 索提诺比率序列
        """
        if self.risk_free_rate is None:
            raise ValueError("risk_free_rate is None")

        downside_returns = self.daily_returns.where(self.daily_returns < 0, 0)
        downside_vol = downside_returns.rolling(window=self.window).std() * np.sqrt(self.window)
        annualized_return = self.daily_returns.rolling(window=self.window).mean() * self.window
        sortino = (annualized_return - self.risk_free_rate) / downside_vol.replace(0, np.nan)
        return sortino

    def calmar_ratio(self) -> pd.Series:
        """计算滚动Calmar比率（年化收益/最大回撤）

        返回:
            pd.Series: Calmar比率序列
        """
        annualized_return = self.daily_returns.rolling(window=self.window).mean() * self.window
        mdd = self.max_drawdown().abs()
        calmar = annualized_return / mdd.replace(0, np.nan)
        return calmar

    def win_rate(self) -> pd.Series:
        """计算滚动胜率（正收益占比）

        返回:
            pd.Series: 胜率序列(0到1之间)
        """
        return (self.daily_returns > 0).rolling(window=self.window).mean()

    def profit_loss_ratio(self) -> pd.Series:
        """计算滚动盈亏比（平均盈利/平均亏损）

        返回:
            pd.Series: 盈亏比序列，当窗口内无亏损时为NaN
        """
        avg_gain = self.daily_returns.where(self.daily_returns > 0).fillna(0).rolling(window=self.window).mean()
        avg_loss = self.daily_returns.where(self.daily_returns < 0).fillna(0).rolling(window=self.window).mean().abs()
        pl_ratio = avg_gain / avg_loss
        return pl_ratio

    def volatility_adjusted_return(self) -> pd.Series:
        """计算滚动波动率调整收益（收益/波动率）

        返回:
            pd.Series: 波动率调整收益序列
        """
        annualized_return = self.daily_returns.rolling(window=self.window).mean() * self.window
        vol = self.volatility()
        var = annualized_return / vol.replace(0, np.nan)
        return var

    def correlation(self) -> pd.Series:
        """计算资产与基准的滚动相关系数

        返回:
            pd.Series: 相关系数序列(-1到1之间)
        """
        if self.benchmark is None:
            raise ValueError("Benchmark is not provided.")

        bench_returns = self.benchmark.pct_change()
        corr = self.daily_returns.rolling(window=self.window).corr(bench_returns)
        return corr

    def skew(self) -> pd.Series:
        """计算滚动偏度

        返回:
            pd.Series: 偏度序列
        """
        return self.daily_returns.rolling(window=self.window).skew()

    def kurtosis(self) -> pd.Series:
        """计算滚动峰度

        返回:
            pd.Series: 峰度序列
        """
        return self.daily_returns.rolling(window=self.window).kurt()

    def beta(self) -> pd.Series:
        """计算滚动Beta（系统性风险）

        返回:
            pd.Series: Beta系数序列
        """
        if self.benchmark is None:
            raise ValueError("Benchmark is not provided.")

        bench_returns = self.benchmark.pct_change()
        cov = self.daily_returns.rolling(window=self.window).cov(bench_returns)
        bench_var = bench_returns.rolling(window=self.window).var()
        beta = cov / bench_var.replace(0, np.nan)
        return beta

    def alpha(self) -> pd.Series:
        """计算滚动Alpha（超额收益）

        返回:
            pd.Series: Alpha序列
        """
        if self.risk_free_rate is None:
            raise ValueError("risk_free_rate must be provided to calculate alpha")
        if self.benchmark is None:
            raise ValueError("Benchmark is not provided.")

        # 计算年化收益
        asset_return = self.daily_returns.rolling(window=self.window).mean() * self.window
        bench_return = self.benchmark.pct_change().rolling(window=self.window).mean() * self.window

        # 计算beta
        beta = self.beta()

        # 计算alpha
        alpha = asset_return - (self.risk_free_rate + beta * (bench_return - self.risk_free_rate))
        return alpha

    def evaluate(self) -> pd.DataFrame:
        """计算并返回所有可用的滚动指标

        返回:
            pd.DataFrame: 包含所有计算指标的DataFrame
        """
        base_index: Dict[str, pd.Series] = {
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

        if self.ols_alpha and self.benchmark is not None and self.risk_free_rate is not None:
            df_ols_alpha_beta = rolling_alpha_beta_ols(
                prices=self.prices, benchmark=self.benchmark,
                risk_free_rate=self.risk_free_rate, window=self.window)
            for col in df_ols_alpha_beta.columns:
                base_index.update({col: df_ols_alpha_beta[col],})
        return pd.DataFrame(base_index)
