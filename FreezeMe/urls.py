from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ClientListView.as_view(), name='client_list'),
    path('submissions/', views.SubmissionListView.as_view(), name='submission_list'),
    path('resubmit/<int:pk>', views.resubmit, name='resubmit'),
    path('client/<int:pk>/submissions/', views.SubmissionListView.as_view(), name='client_submissions'),
    path('client/new/', views.add_client, name='add_client'),
    path('client/edit/<int:pk>', views.UpdateClientView.as_view(), name='update_client'),
    path('settings/', views.setting_list, name='setting_list'),

    # Debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),
    path('test/', views.test, name='test'),
]


# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
