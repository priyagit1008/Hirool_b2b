# django/rest_framework imports
from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter
from django.contrib import admin
from django.conf import settings

# project level imports
from accounts.users import views as account_views
from misc import views as misc_views
from libs.custom_api_docs import include_docs_urls
from clients import views as client_view


# intialize DefaultRouter
router = SimpleRouter()


# register misc app urls with router
router.register(r'', misc_views.APIConfViewSet, base_name='misc')

# register accounts app urls with router
router.register(r'accounts', account_views.UserViewSet, base_name='accounts')


# register clients app urls with router
router.register(r'client', client_view.ClientViewSet, base_name='client')

router.register(r'jd', client_view.JobViewSet, base_name='jd')


# urlpatterns
urlpatterns = [
    path('api/v1/', include((router.urls, 'api'), namespace='v1')),
    path('HS456GAG4FAYJSTT0O/hire-admin/', admin.site.urls),
]

if settings.ENV != "PROD":
    urlpatterns += [re_path(r'^docs/A92DFFBB6B9EC/', include_docs_urls(title="Leads API"))]
