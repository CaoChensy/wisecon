import unittest
import json
from sseclient import SSEClient

from wisecon.utils import headers


class TestSSE(unittest.TestCase):
    def test_sse(self):
        url = "https://push2.eastmoney.com/api/qt/stock/sse?fields=f58,f734,f107,f57,f43,f59,f169,f301,f60,f170,f152,f177,f111,f46,f44,f45,f47,f260,f48,f261,f279,f277,f278,f288,f19,f17,f531,f15,f13,f11,f20,f18,f16,f14,f12,f39,f37,f35,f33,f31,f40,f38,f36,f34,f32,f211,f212,f213,f214,f215,f210,f209,f208,f207,f206,f161,f49,f171,f50,f86,f84,f85,f168,f108,f116,f167,f164,f162,f163,f92,f71,f117,f292,f51,f52,f191,f192,f262,f294,f295,f269,f270,f256,f257,f285,f286,f748,f747&mpi=1000&invt=2&fltt=1&secid=0.301618&ut=fa5fd1943c7b386f172d6893dbfba10b&dect=1&wbp2u=|0|0|0|web"
        import requests
        from sseclient import SSEClient

        # 目标 URL

        # 发送请求并获取响应
        response = requests.get(url, stream=True)
        for resp in response:
            print(resp)

"""
https://5.push2.eastmoney.com/api/qt/stock/details/sse?
fields1=f1,f2,f3,f4
&fields2=f51,f52,f53,f54,f55
&mpi=1000
&dect=1
&fltt=2
&pos=-11
&secid=0.301618
&wbp2u=|0|0|0|web
"""