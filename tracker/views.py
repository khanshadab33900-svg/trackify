from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Count
from .models import Project, Ticket, Comment, User
from .forms import UserRegistrationForm, ProjectForm, TicketForm, TicketUpdateForm, CommentForm

def ensure_demo_data():
    """
    Self-healing routine: guarantees demo accounts (admin, rahul_dev, sneha_qa),
    sample projects, and bug tickets are present in SQLite regardless of deploy method.
    """
    try:
        from django.core.management import call_command
        call_command('migrate', interactive=False)

        # 1. Admin Superuser
        admin = User.objects.filter(username='admin').first()
        if not admin:
            admin = User.objects.create_superuser('admin', 'admin@trackify.internal', 'admin123')
            admin.role = 'admin'
            admin.save()
        else:
            admin.role = 'admin'
            admin.set_password('admin123')
            admin.save()

        # 2. Developer User
        dev = User.objects.filter(username='rahul_dev').first()
        if not dev:
            dev = User.objects.create_user('rahul_dev', 'rahul@trackify.internal', 'admin123')
            dev.role = 'developer'
            dev.save()
        else:
            dev.role = 'developer'
            dev.set_password('admin123')
            dev.save()

        # 3. QA / Tester User
        tester = User.objects.filter(username='sneha_qa').first()
        if not tester:
            tester = User.objects.create_user('sneha_qa', 'sneha@trackify.internal', 'admin123')
            tester.role = 'tester'
            tester.save()
        else:
            tester.role = 'tester'
            tester.set_password('admin123')
            tester.save()

        # 4. Seed sample projects and tickets if database has no projects
        if Project.objects.count() == 0:
            p1 = Project.objects.create(
                name='E-Commerce Cloud Microservices',
                description='Microservices backend for payment processing, cart checkout, and inventory sync.',
                status='active'
            )
            p2 = Project.objects.create(
                name='College Mobile App v2',
                description='Cross-platform flutter application for student attendance, timetable, and campus alerts.',
                status='active'
            )
            p3 = Project.objects.create(
                name='DevOps CI/CD Automation Pipeline',
                description='Automated test suites, containerized Docker deployment, and cluster health monitoring.',
                status='completed'
            )

            t1 = Ticket.objects.create(
                title='High memory spike on checkout endpoint under concurrent load',
                description='Stress tests revealed that handling 500+ requests/sec causes thread pool exhaustion and 504 Gateway Timeouts.',
                priority='high',
                status='in_progress',
                project=p1,
                creator=tester,
                assigned_developer=dev
            )
            t2 = Ticket.objects.create(
                title='OAuth Google Sign-in fails on Android 14 devices',
                description='Users on newer Android versions report NullPointerException during authorization callback redirect.',
                priority='high',
                status='open',
                project=p2,
                creator=tester,
                assigned_developer=None
            )
            t3 = Ticket.objects.create(
                title='Push notification token expired exception in background service',
                description='FCM registration tokens are not being refreshed automatically when app runs in battery saver mode.',
                priority='medium',
                status='in_progress',
                project=p2,
                creator=admin,
                assigned_developer=dev
            )
            t4 = Ticket.objects.create(
                title='Broken pagination on order history data table',
                description='Clicking page 2 in order summary table resets date filters. Query parameters need to be preserved.',
                priority='low',
                status='resolved',
                project=p1,
                creator=tester,
                assigned_developer=dev
            )

            Comment.objects.create(ticket=t1, user=dev, content='Identified connection pool leak in Redis connector. Patch applied and under load testing.')
            Comment.objects.create(ticket=t3, user=admin, content='Please prioritize this fix before the sprint demo on Friday.')
    except Exception as e:
        print(f"[Trackify] ensure_demo_data error: {e}")

def health_check(request):
    """
    Lightweight health check endpoint to wake up Render free tier backend instantly.
    Also ensures demo data is pre-seeded before user logs in.
    """
    ensure_demo_data()
    return JsonResponse({
        "status": "ok",
        "message": "Trackify Backend is Active & Awake",
        "service": "render-web-service"
    })

def demo_login(request, role='admin'):
    """
    True 1-Click Instant Demo Authentication endpoint.
    Directly logs in as Admin, Developer, or Tester and redirects to dashboard.
    """
    ensure_demo_data()
    role_map = {
        'admin': 'admin',
        'developer': 'rahul_dev',
        'dev': 'rahul_dev',
        'tester': 'sneha_qa',
        'qa': 'sneha_qa'
    }
    username = role_map.get(role.lower(), 'admin')
    user = User.objects.filter(username=username).first()
    if not user:
        ensure_demo_data()
        user = User.objects.filter(username=username).first()

    if user:
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user)
        return redirect('dashboard')
    return redirect('login')

class CustomLoginView(auth_views.LoginView):
    template_name = 'tracker/login.html'

    def get(self, request, *args, **kwargs):
        ensure_demo_data()
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        username = self.request.POST.get('username', '').strip()
        password = self.request.POST.get('password', '').strip()

        # If user tried logging in with standard demo credentials, heal user and log in!
        if username in ['admin', 'rahul_dev', 'sneha_qa'] and (password == 'admin123' or not password):
            ensure_demo_data()
            user = User.objects.filter(username=username).first()
            if user:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth_login(self.request, user)
                return redirect('dashboard')

        return super().form_invalid(form)

def custom_logout(request):
    """
    Logs out user cleanly for both GET and POST requests without 405 errors.
    """
    auth_logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def dashboard(request):
    total_projects = Project.objects.count()
    total_tickets = Ticket.objects.count()
    open_tickets = Ticket.objects.filter(status='open').count()
    in_progress_tickets = Ticket.objects.filter(status='in_progress').count()
    resolved_tickets = Ticket.objects.filter(status='resolved').count()
    
    recent_tickets = Ticket.objects.select_related('project', 'assigned_developer', 'creator').order_by('-created_at')[:6]
    projects = Project.objects.annotate(ticket_count=Count('tickets')).order_by('-id')[:6]

    context = {
        'total_projects': total_projects,
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'in_progress_tickets': in_progress_tickets,
        'resolved_tickets': resolved_tickets,
        'recent_tickets': recent_tickets,
        'projects': projects,
    }
    return render(request, 'tracker/dashboard.html', context)


# Project Views
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'tracker/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.annotate(ticket_count=Count('tickets')).order_by('-id')

class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tracker/project_form.html'
    success_url = reverse_lazy('project_list')

    def test_func(self):
        return self.request.user.role == 'admin'


# Ticket Views
class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tracker/ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        queryset = Ticket.objects.select_related('project', 'assigned_developer', 'creator').order_by('-created_at')
        project_id = self.request.GET.get('project')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tracker/ticket_form.html'
    success_url = reverse_lazy('ticket_list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'tracker/ticket_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = self.object
            comment.user = request.user
            comment.save()
            return redirect('ticket_detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))

class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ticket
    form_class = TicketUpdateForm
    template_name = 'tracker/ticket_form.html'
    
    def get_success_url(self):
        return reverse_lazy('ticket_detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        ticket = self.get_object()
        if self.request.user.role == 'admin':
            return True
        if self.request.user.role == 'developer' and ticket.assigned_developer == self.request.user:
            return True
        return False
