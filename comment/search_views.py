from haystack.views import SearchView
from .models import *


class MySeachView(SearchView):
    def extra_context(self):
        context = super(MySeachView, self).extra_context()
        print(11111122222222222222)
        return context