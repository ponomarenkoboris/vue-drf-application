from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('account/', include('accounts.urls')),
    path('tasks/', include('tasks.urls')),
]

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]