from game.webserver.views import tasks, index

def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/tasks', tasks)
