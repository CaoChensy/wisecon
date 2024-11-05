import unittest
from wisecon.macro import *


class TestCPI(unittest.TestCase):
    """"""

    def test_asset_invest(self):
        data = AssetInvest(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_boom_index(self):
        """"""
        data = BoomIndex(size=10, verbose=True).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_cpi(self):
        data = CPI(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_currency_supply(self):
        """"""
        data = CurrencySupply(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_customs(self):
        """"""
        data = Customs(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_deposit_rate(self):
        """"""
        data = DepositRate(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_deposit_reserve(self):
        """"""
        data = DepositReserve(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_faith_index(self):
        """"""
        data = FaithIndex(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_fdi(self):
        """"""
        data = FDI(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_forex_deposit(self):
        """"""
        data = ForexDeposit(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_forex_loan(self):
        """"""
        data = ForexLoan(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_gdp(self):
        """"""
        data = GDP(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_gold_currency(self):
        """"""
        data = GoldCurrency(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_goods_index(self):
        """"""
        data = GoodsIndex(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_gov_income(self):
        """"""
        data = GovIncome(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_old_hose(self):
        """"""
        data = HoseIndexOld(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_new_hose(self):
        """"""
        data = HoseIndexNew(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

        data = HoseIndexNew(size=10, cities=["杭州", "深圳"]).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

        data = HoseIndexNew(size=10, report_date="2023-01-01").load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_imp_interest(self):
        """"""
        data = ImpInterest(size=10, ).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_indus_grow(self):
        """"""
        data = IndusGrow(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_lpr(self):
        """"""
        data = LPR(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_new_loan(self):
        """"""
        data = NewLoan(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_oil_price(self):
        """"""
        data = OilPrice(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_pmi(self):
        """"""
        data = PMI(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_ppi(self):
        """"""
        data = PPI(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_stock_open(self):
        """"""
        data = StockOpen(size=10).load()
        data.show_columns()
        print(data.to_markdown(chinese_column=True))

    def test_stock_statistics(self):
        """"""
        data = StockStatistics(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_tax(self):
        """"""
        data = Tax(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_total_retail(self):
        """"""
        data = TotalRetail(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))

    def test_transfer_fund(self):
        """"""
        data = TransferFund(size=10).load()
        data.show_columns()
        print(data.to_frame(chinese_column=True))


class TestLoopLoadData(unittest.TestCase):
    """"""
    def test_loop(self):
        """"""
        macro_mapping = {
            "居民消费价格指数(CPI)": CPI,
            "工业品出厂价格指数(PPI)": PPI,
            "国内生产总值(GDP)": GDP,
            "采购经理人指数(PMI)": PMI,
            "城镇固定资产投资": AssetInvest,
            "房价指数(old)": HoseIndexOld,
            "新房价指数": HoseIndexNew,
            "企业景气及企业家信心指数": BoomIndex,
            "工业增加值增长": IndusGrow,
            "企业商品价格指数": GoodsIndex,
            "消费者信心指数": FaithIndex,
            "社会消费品零售总额": TotalRetail,
            "货币供应量": CurrencySupply,
            "海关进出口增减情况一览表": Customs,
            "全国股票交易统计表": StockStatistics,
            "外汇和黄金储备": GoldCurrency,
            "交易结算资金(银证转账)": TransferFund,
            "股票账户统计表(新)": StockOpen,
            "外商直接投资数据(FDI)": FDI,
            "财政收入": GovIncome,
            "全国税收收入": Tax,
            "新增信贷数据": NewLoan,
            "银行间拆借利率": ImpInterest,
            "本外币存款": ForexDeposit,
            "外汇贷款数据": ForexLoan,
            "存款准备金率": DepositReserve,
            "利率调整": DepositRate,
            "油价": OilPrice,
            "LPR数据": LPR,
        }
        for macro_name, macro_class in macro_mapping.items():
            print(macro_name)
            data = macro_class(size=5).load()
            data.show_columns()
            print(data.to_frame(chinese_column=True).to_markdown())
            print("\n\n")
