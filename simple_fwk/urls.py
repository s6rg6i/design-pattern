from fwk.url import Url
from views import Index, About, Adm, AddCategory, AddCourse, ShowCourses

urlpatterns = [
    Url('/', Index),
    Url('/adm/', Adm),
    Url('/add-ctg/', AddCategory),
    Url('/add-course/', AddCourse),
    Url('/show-courses/', ShowCourses),
    Url('/about/', About),
]
