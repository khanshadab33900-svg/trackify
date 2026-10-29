from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # Health check for Render wake-up
    path('health/', views.health_check, name='health_check'),
    path('api/health/', views.health_check, name='api_health_check'),

    # Login page (default page)
    path('', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Projects
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),

    # Tickets
    path('tickets/', views.TicketListView.as_view(), name='ticket_list'),
    path('tickets/create/', views.TicketCreateView.as_view(), name='ticket_create'),
    path('tickets/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('tickets/<int:pk>/update/', views.TicketUpdateView.as_view(), name='ticket_update'),

]
