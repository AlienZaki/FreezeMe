from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import ClientsItemListView, SubmissionsRecordListView, SettingsListView, ClientsListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ClientsItemListView.as_view(), name='clients-list'),
    path('submissions/history/', SubmissionsRecordListView.as_view(), name='submissions-history'),
    path('settings/', SettingsListView.as_view(), name='settings'),
    path('client/new/', ClientsListView.as_view(), name='new-client'),


    # Debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
