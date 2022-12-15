from fwk.url import Url
from views import Index, Hi, Homepage


urlpatterns = [
    Url('/', Index),
    Url('/home/', Homepage),
    Url('/hi/', Hi),
]
