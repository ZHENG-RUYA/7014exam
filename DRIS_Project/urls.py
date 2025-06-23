"""
URL configuration for DRIS_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# DRIS_Project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from DRIS import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('shelters/', views.shelter_list, name='shelters'),
    # Authentication
    path('register/', views.register, name='register'),
    path('register/volunteer/', views.register_volunteer, name='register_volunteer'),
    path('login/', auth_views.LoginView.as_view(template_name='DRIS/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='DRIS/logout.html'), name='logout'),

    # Profile
    path('profile/', views.profile, name='profile'),

    # Disaster Reports
    path('reports/', views.DisasterReportListView.as_view(), name='disaster_reports'),
    path('report/<int:pk>/', views.DisasterReportDetailView.as_view(), name='report_detail'),
    path('report/new/', views.DisasterReportCreateView.as_view(), name='submit_report'),
    path('report/<int:pk>/update/', views.DisasterReportUpdateView.as_view(), name='update_report'),

    # Aid Requests
    path('request/new/<int:disaster_id>/', views.AidRequestCreateView.as_view(), name='request_aid'),

    # Volunteer
    path('volunteer/dashboard/', views.volunteer_dashboard, name='volunteer_dashboard'),

    # Admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)