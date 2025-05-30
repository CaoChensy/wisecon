import numba
import hashlib
import numpy as np
import pandas as pd
from typing import Tuple, Optional
from datetime import timedelta
from wisecon.utils import LoggerMixin


__all__ = [
    "AdjustmentFactorCalculator",
]


class AdjustmentFactorCalculator(LoggerMixin):
    """
    复权因子计算器（支持比例型/累积型/定点复权）

    功能：
    1. 计算比例型复权因子
    2. 计算任意时点的累积型复权因子
    3. 生成定点前复权数据
    4. 增量更新复权因子
    5. 处理振幅、涨跌幅等衍生字段的复权
    """

    # 需要复权的价格字段
    PRICE_FIELDS = ['open', 'close', 'high', 'low']
    # 需要复权的衍生字段
    DERIVED_FIELDS = ['amplitude', 'change_pct', "change_amt"]

    def __init__(self, raw_kline: pd.DataFrame, adj_kline: pd.DataFrame, verbose: Optional[bool] = False, **kwargs):
        """
        初始化复权计算器

        参数：
        raw_kline - 不复权K线数据，需包含列：time, open, high, low, close, volume等
        adj_kline - 前复权K线数据，需包含相同结构的列
        """
        self.raw_kline = self._validate_data(raw_kline).copy()
        self.adj_kline = self._validate_data(adj_kline).copy()
        self.ratio_factors = self._calculate_ratio_factors()
        self.cumulative_base_date = None
        self.verbose = verbose
        self.kwargs = kwargs

    def _validate_data_type(self, df: pd.DataFrame) -> pd.DataFrame:
        """数据类型验证"""
        columns = [
            'open', 'close', 'high', 'low', 'volume', 'turnover',
            'amplitude', 'change_pct', 'change_amt', 'turnover_rate']
        for col in columns:
            if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                df[col] = pd.to_numeric(df[col])
        return df

    def _validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """数据验证"""
        required_cols = {'time', 'open', 'high', 'low', 'close'}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"缺失必要列，需要: {required_cols}")
        df = self._validate_data_type(df)
        df = df.sort_values('time')
        return df.set_index('time')

    def _calculate_ratio_factors(self) -> pd.Series:
        """计算比例型复权因子（基于收盘价）"""
        close_factors = self.adj_kline['close'] / self.raw_kline['close']
        close_factors = close_factors.replace([np.inf, -np.inf], np.nan)
        if close_factors.isna().any():
            raise ValueError("存在无效价格数据（零或NaN）")
        events = self.detect_adjustment_events(factors=close_factors)
        data = pd.DataFrame({"factors": close_factors, "group": events.cumsum(),})
        factors = data.groupby('group')['factors'].transform('mean').round(6).cummax()
        return factors

    def get_cumulative_factors(self, base_date: str) -> pd.Series:
        """
        计算基于指定基准日的累积型复权因子

        参数：
        base_date - 基准日期（该日复权价=不复权价）

        返回：
        累积型复权因子序列
        """
        if base_date not in self.ratio_factors.index:
            raise ValueError(f"基准日期 {base_date} 不在数据范围内")
        self.cumulative_base_date = base_date
        base_factor = self.ratio_factors.loc[base_date]

        if base_factor <= 0:
            self.warning(msg=f"基准日期 {base_date} 的复权因子为 {base_factor}")

        cumulative_factors = self.ratio_factors / base_factor
        return cumulative_factors

    def _adjust_price_fields(self, df: pd.DataFrame, factors: pd.Series) -> pd.DataFrame:
        """调整价格相关字段"""
        adj_df = df.copy()
        for col in self.PRICE_FIELDS:
            adj_df[col] = adj_df[col] * factors
        return adj_df

    def _adjust_derived_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """调整衍生字段"""
        adj_df = df.copy()
        if 'amplitude' in adj_df.columns:
            adj_df['amplitude'] = (adj_df['high'] - adj_df['low']) / adj_df['low']
        if 'change_pct' in adj_df.columns:
            adj_df['change_pct'] = adj_df['close'].pct_change() * 100
        if 'change_amt' in adj_df.columns:
            adj_df['change_amt'] = adj_df['close'].diff()
        return adj_df

    def get_anchor_adjusted_kline(self, anchor_date: str) -> pd.DataFrame:
        """
        生成基于指定日期的定点前复权K线

        参数：
        anchor_date - 基准日期（该日复权价=不复权价）

        返回：
        定点前复权K线数据（包含所有字段）
        """
        if anchor_date not in self.ratio_factors.index:
            raise ValueError(f"锚定日期 {anchor_date} 不在数据范围内")

        anchor_factor = self.ratio_factors.loc[anchor_date]
        adj_factors = self.ratio_factors / anchor_factor
        adj_kline = self.raw_kline.copy()
        adj_kline = self._adjust_price_fields(adj_kline, adj_factors)
        adj_kline = self._adjust_derived_fields(adj_kline)

        for field in ['volume', 'turnover', 'turnover_rate']:
            if field in adj_kline:
                assert adj_kline[field].equals(self.raw_kline[field]), f"{field} 被意外修改"
        return adj_kline

    def update_factors(self, new_raw: pd.DataFrame, new_adj: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        """
        增量更新复权因子

        参数：
        new_raw - 新增的不复权K线
        new_adj - 新增的前复权K线

        返回：
        (更新后的比例型因子, 更新后的累积型因子)
        """
        # 合并新数据
        new_raw = self._validate_data(new_raw)
        new_adj = self._validate_data(new_adj)

        self.raw_kline = pd.concat([self.raw_kline, new_raw]).sort_index()
        self.adj_kline = pd.concat([self.adj_kline, new_adj]).sort_index()

        # 重新计算因子
        old_ratio = self.ratio_factors.copy()
        self.ratio_factors = self._calculate_ratio_factors()

        # 增量计算累积因子
        if self.cumulative_base_date is not None:
            new_cumulative = self.get_cumulative_factors(self.cumulative_base_date)
        else:
            new_cumulative = pd.Series(dtype=float)

        return self.ratio_factors, new_cumulative

    def detect_adjustment_events(
            self,
            factors: pd.Series,
            threshold: float = 0.01
    ) -> pd.Series:
        """
        检测除权事件发生日
        Args:
            factors:
            threshold:

        Returns:

        """
        factor_changes = factors.pct_change().abs()
        rol_max = factor_changes.rolling(window=22, min_periods=1).max()
        rol_min = factor_changes.rolling(window=22, min_periods=1).min()
        position = rol_max - rol_min > threshold
        events = (position & (~position.shift(1, fill_value=False)))
        return events
