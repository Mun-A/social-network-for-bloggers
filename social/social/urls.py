from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages.views import flatpage
from django.conf.urls import handler404, handler500


import posts.views

handler404 = "posts.views.page_not_found"  # noqa
handler500 = "posts.views.server_error"  # noqa

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("posts.urls")),

    # flatpages
    path("about/", include('django.contrib.flatpages.urls')),

    path("auth/", include("users.urls")),

    #  если нужного шаблона для /auth не нашлось в файле users.urls —
    #  ищем совпадения в файле django.contrib.auth.urls
    path("auth/", include("django.contrib.auth.urls")),

    path("api/v1/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
]

urlpatterns += [
        path('about-us/', flatpage, {'url': '/about-us/'}, name='about'),
        path('terms/', flatpage, {'url': '/terms/'}, name='terms'),
        path('about-author/', flatpage, {'url': '/about-author/'}, name='author'),
        path('about-spec/', flatpage, {'url': '/about-spec/'}, name='spec'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)


