import asyncio
import logging
import time

from aiohttp.web import Response
from aiohttp_sse import sse_response
from game.webserver import db
from game import settings


def prepare_response(data):
    """Format

        [('1x3:t2', 304500), ('1x4:t2', 96501), ('3x1:t2', 49501)]

    into

        <p>1x3:t2 : 304500</p>
        <p>1x4:t2 : 96501</p>
        <p>3x1:t2 : 49501</p>

    """
    line_tpl = "{} : {}<br>"
    res_str = ""
    for item in sorted(data):
        res_str += line_tpl.format(*item)
    return res_str


async def tasks(request):
    conn = request.app['redis_pool']

    async with sse_response(request) as resp:
        while True:

            t0 = time.time()
            data = await db.read_tasks_from_nearby_players(conn, x=0, y=0)
            logging.info(f"--tasks qty--: {len(data)}")
            logging.info(f"--TIME-- response: {time.time() - t0}")

            data = prepare_response(data)

            logging.info('-' * 80)
            logging.debug(data)
            await resp.send(data)
            await asyncio.sleep(settings.PAGE_REFRESH_RATE)
    return resp


async def index(request):
    d = """
        <html>
        <body>
            <script>
                var evtSource = new EventSource("/tasks");
                evtSource.onmessage = function(e) {
                    document.getElementById('response').innerHTML = e.data
                }
            </script>
            <h2>Tasks (name : ttl):</h2>
            <div id="response"></div>
        </body>
    </html>
    """
    return Response(text=d, content_type='text/html')
