from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^Hashtag/', include('Hashtag.urls')),
    url(r'^admin/', admin.site.urls),
]
