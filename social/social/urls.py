from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages import views


urlpatterns = [
    path("", include("posts.urls")),

    # flatpages
    path('about/', include('django.contrib.flatpages.urls')),

    path("auth/", include("users.urls")),

    #  если нужного шаблона для /auth не нашлось в файле users.urls —
    #  ищем совпадения в файле django.contrib.auth.urls
    path("auth/", include("django.contrib.auth.urls")),

    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
        path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
        path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),
        path('about-author/', views.flatpage, {'url': '/about-author/'}, name='author'),
        path('about-spec/', views.flatpage, {'url': '/about-spec/'}, name='spec'),
]
