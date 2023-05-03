import base64
import hashlib
import hmac
import random
import string
import time

import httpx

orderno = ""
secret = ""
useProxy = False


class DouBanClient:
    def __init__(self):
        self.udid = ''.join([random.choice(string.ascii_lowercase + string.digits) for i in range(40)])
        self.userAgent = "api-client/1 com.douban.frodo/7.35.0(240) Android/29 product/aosp_blueline " \
                         "vendor/Google model/AOSP on blueline brand/Android  " \
                         "rom/android  network/wifi  udid/" + self.udid + "  platform/mobile nd/1"
        self.baseHeaders = {
            "User-Agent": self.userAgent,
            "Host": "frodo.douban.com",
            "Connection": "close",
        }
        self.apiKey = "0dad551ec0f84ed02907ff5c42e8ec70"
        self.secretKey = "bf7dddc7c9cfe6f7"
        self.baseParams = {"apikey": self.apiKey,
                           "channel": "Douban",
                           "udid": self.udid,
                           "os_rom": "android",
                           "timezone": "Asia/Shanghai"}
        if useProxy:
            self.httpClient = httpx.AsyncClient(timeout=30, proxies="http://forward.xdaili.cn:80", verify=False,
                                                limits=httpx.Limits(max_keepalive_connections=2000,
                                                                    max_connections=5000))
        else:
            self.httpClient = httpx.AsyncClient(timeout=30, limits=httpx.Limits(max_keepalive_connections=2000,
                                                                                max_connections=5000))

    def getAuth(self):
        timestamp = str(int(time.time()))
        string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
        string = string.encode()
        md5_string = hashlib.md5(string).hexdigest()
        sign = md5_string.upper()
        return "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp

    def getSign(self, path, ts):
        strList = ["GET", path.replace("/", "%2F"), ts]
        signMessage = "&".join(strList)
        sign = base64.b64encode(hmac.new(self.secretKey.encode(), signMessage.encode(), hashlib.sha1).digest()).decode()
        return sign

    async def apiResult(self, path, params):
        ts = str(int(time.time()))
        sign = self.getSign(path, ts)
        headers = self.baseHeaders.copy()
        if useProxy:
            headers['Proxy-Authorization'] = self.getAuth()
        params["_sig"] = sign
        params["_ts"] = ts
        url = "https://frodo.douban.com" + path
        res = await self.httpClient.get(url, params=params, headers=headers)
        self.udid = ''.join([random.choice(string.ascii_lowercase + string.digits) for i in range(40)])
        return res.json()

    async def getSubject(self, doubanId, mediaType):
        result = await self.apiResult("/api/v2/" + mediaType + "/" + str(doubanId), self.baseParams)
        return result

    async def getPersonInfo(self, doubanId):
        result = await self.apiResult("/api/v2/elessar/subject/" + doubanId, self.baseParams)
        return result

    async def search(self, keyword, count=20):
        params = self.baseParams.copy()
        params["q"] = keyword
        params["count"] = str(count)
        result = await self.apiResult("/api/v2/search/subjects", params)
        return result

    async def getSubjectCredits(self, doubanId, mediaType):
        params = self.baseParams.copy()
        params["start"] = "0"
        params["count"] = "50"
        result = await self.apiResult("/api/v2/" + mediaType + "/" + str(doubanId) + "/credits_stats", params)
        return result

    async def test(self):
        result = await self.getSubjectCredits("1295038", "movie")
        print(result)

    def runTest(self):
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.test())


if __name__ == '__main__':
    client = DouBanClient()
    client.runTest()
