from django.urls import path
from . import views

urlpatterns = [
    # Health checks for Render wake-up and auto-seeding
    path('health/', views.health_check, name='health_check'),
    path('api/health/', views.health_check, name='api_health_check'),

    # 1-Click Instant Demo Authentication
    path('demo-login/<str:role>/', views.demo_login, name='demo_login'),

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
