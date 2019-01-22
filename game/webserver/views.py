import asyncio

from aiohttp import web

from aiohttp.web import Response
from aiohttp_sse import sse_response
from datetime import datetime


async def hello(request):
    return web.Response(text="Hello, world")


async def show_date(request):
    redis = request.app['redis_pool']
    await redis.psetex('my-key', 3000, 'value')
    await asyncio.sleep(0.3)

    async with sse_response(request) as resp:
        while True:
            # data = 'Server Time : {}'.format(datetime.now())
            # await redis.set('my-key', 'value')
            # data = await redis.get('my-key')
            data = await redis.pttl('my-key')
            data = str(data)
            print(data)
            await resp.send(data)
            await asyncio.sleep(1)
    return resp


async def index(request):
    d = """
        <html>
        <body>
            <script>
                var evtSource = new EventSource("/date");
                evtSource.onmessage = function(e) {
                    document.getElementById('response').innerText = e.data
                }
            </script>
            <h1>Response from server:</h1>
            <div id="response"></div>
        </body>
    </html>
    """
    return Response(text=d, content_type='text/html')
