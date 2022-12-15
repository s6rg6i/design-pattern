from fwk.url import Url
from views import Index, About


urlpatterns = [
    Url('/', Index),
    Url('/about/', About),
]
