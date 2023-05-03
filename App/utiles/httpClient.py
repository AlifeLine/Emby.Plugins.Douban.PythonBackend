import httpx

from App.utiles.proxyConfig import s5Proxy, apiUrl

httpClient = httpx.AsyncClient(proxies=s5Proxy, base_url=apiUrl, timeout=30,
                               limits=httpx.Limits(max_keepalive_connections=2000, max_connections=5000))
