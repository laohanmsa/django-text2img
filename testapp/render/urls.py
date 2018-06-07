from django.conf.urls import url
from .views import RenderTextView
from .views import RenderListTextView

urlpatterns = [
    # actions
    url(r'^render/detail?$', RenderTextView.as_view(), name='detail'),
    url(r'^render/list?$', RenderListTextView.as_view(), name='list'),
]
