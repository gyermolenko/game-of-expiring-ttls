import asyncio

from aiohttp.web import Response
from aiohttp_sse import sse_response
from game import db

SLEEP_FOR = 3


async def tasks(request):
    redis = request.app['redis_pool']
    # await redis.psetex('my-key', 3000, 'value')

    async with sse_response(request) as resp:
        while True:
            data = await db.read_tasks_by_mask(redis, 4, 4)
            # data = await redis.pttl('my-key')

            data = str(data)
            print(data)
            await resp.send(data)
            await asyncio.sleep(SLEEP_FOR)
    return resp


async def index(request):
    d = """
        <html>
        <body>
            <script>
                var evtSource = new EventSource("/tasks");
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


