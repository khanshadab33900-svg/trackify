from django.urls import path
from . import views

urlpatterns = [
    # Health checks for Render wake-up and auto-seeding
    path('health/', views.health_check, name='health_check'),
    path('health', views.health_check, name='health_check_noslash'),
    path('api/health/', views.health_check, name='api_health_check'),
    path('api/health', views.health_check, name='api_health_check_noslash'),

    # 1-Click Instant Demo Authentication
    path('demo-login/<str:role>/', views.demo_login, name='demo_login'),

    # REST API Endpoints (Both with & without trailing slashes for seamless client calls)
    path('api/auth/login', views.api_auth_login, name='api_auth_login_noslash'),
    path('api/auth/login/', views.api_auth_login, name='api_auth_login'),
    path('api/auth/demo-login/<str:role>', views.api_auth_demo_login, name='api_auth_demo_login_noslash'),
    path('api/auth/demo-login/<str:role>/', views.api_auth_demo_login, name='api_auth_demo_login'),
    path('api/auth/register', views.api_auth_register, name='api_auth_register_noslash'),
    path('api/auth/register/', views.api_auth_register, name='api_auth_register'),
    path('api/dashboard/stats', views.api_dashboard_stats, name='api_dashboard_stats_noslash'),
    path('api/dashboard/stats/', views.api_dashboard_stats, name='api_dashboard_stats'),
    path('api/projects', views.api_projects, name='api_projects_noslash'),
    path('api/projects/', views.api_projects, name='api_projects'),
    path('api/tickets', views.api_tickets, name='api_tickets_noslash'),
    path('api/tickets/', views.api_tickets, name='api_tickets'),
    path('api/tickets/<int:pk>', views.api_ticket_detail, name='api_ticket_detail_noslash'),
    path('api/tickets/<int:pk>/', views.api_ticket_detail, name='api_ticket_detail'),
    path('api/tickets/<int:pk>/comments', views.api_ticket_comments, name='api_ticket_comments_noslash'),
    path('api/tickets/<int:pk>/comments/', views.api_ticket_comments, name='api_ticket_comments'),

    # Authentication
    path('', views.CustomLoginView.as_view(), name='login'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
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
