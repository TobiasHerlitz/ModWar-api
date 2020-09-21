import asyncio
import aiohttp
from funcs_helper import cookie_getter

cookies = {'ACT_SSO_COOKIE': cookie_getter()}


async def aiohttp_handler(username_list, **kwargs):
    url_list = []

    for i in range(len(username_list)):
        url_list.append(
            'https://my.callofduty.com/api/papi-client/stats/cod/v1/'
            'title/mw/platform/uno/gamer/{}/profile/type/mp'
            .format(username_list[i]))

    async with aiohttp.ClientSession(cookies=cookies) as session:
        tasks = []
        for i in url_list:
            tasks.append(get(session=session, url=i, **kwargs))

        # asyncio.gather() will wait on the entire task set to be
        # completed.  If you want to process results greedily as they come in,
        # loop over asyncio.as_completed()
        htmls = await asyncio.gather(*tasks, return_exceptions=True)
        return htmls


async def get(session: aiohttp.ClientSession, url: str, **kwargs) -> dict:
    resp = await session.request('GET', url=url, **kwargs)

    # Note that this may raise an exception for non-2xx responses
    # You can either handle that here, or pass the exception through
    data = await resp.json()
    data = data['data']['lifetime']['all']['properties']['kdRatio']
    return data
