from datetime import date
from views import Index, About


# Front Controller
def date_key():
    return dict(date=date.today())


def secret_key():
    return dict(key='1234567890')


def static_key():
    return dict(static_url="/static/")


fronts = [secret_key, date_key, static_key]

# Page Controller
routes = {
    '/': Index(),
    '/about/': About(),
}
