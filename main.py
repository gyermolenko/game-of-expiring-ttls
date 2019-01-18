import asyncio
import logging
from datetime import datetime

from aiohttp import web
from aiohttp.web import Response
from aiohttp_sse import sse_response


async def hello(request):
    return web.Response(text="Hello, world")

async def show_date(request):
    # loop = request.app.loop
    async with sse_response(request) as resp:
        while True:
            data = 'Server Time : {}'.format(datetime.now())
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


def setup_routes(app):
    app.router.add_get('/hello', hello)
    app.router.add_get('/', index)
    app.router.add_get('/date', show_date)

async def init_app():
    app = web.Application()
    setup_routes(app)
    return app

def main():
    logging.basicConfig(level=logging.DEBUG)
    app = init_app()
    # config = get_config()
    web.run_app(app)


if __name__ == '__main__':
    main()
