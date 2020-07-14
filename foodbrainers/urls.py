from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('restaurants.urls')),
    # tutaj django wie, ze uzywamy templatu registration/login - w tym pliku nalezy umiescic template login,
    # ale mozna tez nadpisac uzywajac template_view, ale my mamy w folderze template login, ale nie mamy logout,
    # bo zrobilismy na logout przekierowanie na strone glowna
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + static(settings.MEDIA_URL,
                             document_root=settings.MEDIA_ROOT)
