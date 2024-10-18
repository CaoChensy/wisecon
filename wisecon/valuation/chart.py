import pyecharts.options as opts
from pyecharts.charts import Line
from typing import List, Optional
import numpy as np


__all__ = [
    "PEChart"
]


class PEChart:
    """"""
    def __init__(
            self,
            x: List[str],
            y: List[float],
            title: Optional[str] = None,
            width: Optional[str] = "1000px",
            height: Optional[str] = "600px",
            q: Optional[List[float]] = None,
    ):
        """"""
        self.x = x
        self.y = y
        self.width = width if width is not None else "1000px"
        self.height = height if height is not None else "600px"
        self.title = title if title is not None else "PE Chart"
        if q is None:
            self.q = [0.15, 0.5, 0.85]
        else:
            self.q = q

    def line_chart(self, ):
        """"""
        min_ = round(min(self.y) - min(self.y) * 0.1, 2)
        max_ = round(max(self.y) + max(self.y) * 0.1, 2)
        pe_buy, pe_mid, pe_sell = np.quantile(self.y, self.q)
        markline_data = [
            opts.MarkLineItem(y=pe_buy),
            opts.MarkLineItem(y=pe_mid),
            opts.MarkLineItem(y=pe_sell)
        ]

        chart = Line(
            init_opts=opts.InitOpts(width=self.width, height=self.height)
        )
        chart.add_xaxis(self.x)
        chart.add_yaxis(
            "PE", self.y,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
            markline_opts=opts.MarkLineOpts(data=markline_data),
        )
        chart.set_global_opts(
            title_opts=opts.TitleOpts(title=self.title),
            yaxis_opts=opts.AxisOpts(min_=min_, max_=max_),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            datazoom_opts=[opts.DataZoomOpts(type_="inside", range_end=100)],
        )
        return chart

    def render(self, path: str):
        """"""
        chart = self.line_chart()
        chart.render(path)
