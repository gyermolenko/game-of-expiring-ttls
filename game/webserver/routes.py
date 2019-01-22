from views import hello
from views import index
from views import show_date

def setup_routes(app):
    app.router.add_get('/hello', hello)
    app.router.add_get('/', index)
    app.router.add_get('/date', show_date)