from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.client_list, name='client_list'),
    path('submissions/all/', views.submission_list, name='submission_list'),
    path('settings/', views.setting_list, name='setting_list'),
    path('client/new/', views.add_client, name='add_client'),
    path('client/edit/<int:pk>', views.UpdateClientView.as_view(), name='update_client'),

    # Debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
