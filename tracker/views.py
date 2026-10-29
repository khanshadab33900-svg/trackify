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


# ==============================================================================
# REST API JSON ENDPOINTS (For Static Client, SPAs, and Decoupled Frontends)
# ==============================================================================
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_auth_login(request):
    ensure_demo_data()
    if request.method != 'POST':
        return JsonResponse({'detail': 'POST method required'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    user = User.objects.filter(username=username).first()
    if not user and username in ['admin', 'rahul_dev', 'sneha_qa']:
        ensure_demo_data()
        user = User.objects.filter(username=username).first()

    if user and (user.check_password(password) or (username in ['admin', 'rahul_dev', 'sneha_qa'] and (password == 'admin123' or not password))):
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user)
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'full_name': user.get_full_name() or user.username
        })
    return JsonResponse({'detail': 'Invalid username or password'}, status=401)

@csrf_exempt
def api_auth_demo_login(request, role='admin'):
    ensure_demo_data()
    role_map = {'admin': 'admin', 'developer': 'rahul_dev', 'dev': 'rahul_dev', 'tester': 'sneha_qa', 'qa': 'sneha_qa'}
    username = role_map.get(role.lower(), 'admin')
    user = User.objects.filter(username=username).first()
    if not user:
        ensure_demo_data()
        user = User.objects.filter(username=username).first()

    if user:
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user)
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'full_name': user.get_full_name() or user.username
        })
    return JsonResponse({'detail': 'Demo user not found'}, status=404)

@csrf_exempt
def api_auth_register(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'POST method required'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    role = data.get('role', 'tester').strip()

    if not username or not password:
        return JsonResponse({'detail': 'Username and password required'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'detail': 'Username already exists'}, status=400)

    user = User.objects.create_user(username=username, password=password)
    user.role = role
    user.save()
    return JsonResponse({'id': user.id, 'username': user.username, 'role': user.role, 'message': 'Registered successfully'})

def api_dashboard_stats(request):
    ensure_demo_data()
    total_projects = Project.objects.count()
    total_tickets = Ticket.objects.count()
    in_progress = Ticket.objects.filter(status='in_progress').count()
    resolved = Ticket.objects.filter(status='resolved').count()
    
    recent_qs = Ticket.objects.select_related('project', 'creator').order_by('-created_at')[:6]
    recent_tickets = [{
        'id': t.id,
        'title': t.title,
        'priority': t.priority,
        'status': t.status,
        'project_name': t.project.name if t.project else 'General',
        'creator_username': t.creator.username if t.creator else 'System',
        'created_at': t.created_at.strftime('%Y-%m-%d %H:%M') if t.created_at else ''
    } for t in recent_qs]

    projects_qs = Project.objects.annotate(ticket_count=Count('tickets')).order_by('-id')[:6]
    projects_list = [{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'status': p.status,
        'ticket_count': p.ticket_count
    } for p in projects_qs]

    return JsonResponse({
        'total_projects': total_projects,
        'total_tickets': total_tickets,
        'in_progress_tickets': in_progress,
        'resolved_tickets': resolved,
        'recent_tickets': recent_tickets,
        'projects': projects_list
    })

@csrf_exempt
def api_projects(request):
    ensure_demo_data()
    if request.method == 'GET':
        projects_qs = Project.objects.annotate(ticket_count=Count('tickets')).order_by('-id')
        data = [{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'status': p.status,
            'ticket_count': p.ticket_count
        } for p in projects_qs]
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
        except Exception:
            body = request.POST
        p = Project.objects.create(
            name=body.get('name', 'Untitled Project'),
            description=body.get('description', ''),
            status=body.get('status', 'active')
        )
        return JsonResponse({'id': p.id, 'name': p.name, 'message': 'Created successfully'}, status=201)

@csrf_exempt
def api_tickets(request):
    ensure_demo_data()
    if request.method == 'GET':
        project_id = request.GET.get('project') or request.GET.get('project_id')
        qs = Ticket.objects.select_related('project', 'creator', 'assigned_developer').order_by('-created_at')
        if project_id:
            qs = qs.filter(project_id=project_id)
        data = [{
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'priority': t.priority,
            'status': t.status,
            'project_name': t.project.name if t.project else 'General',
            'project_id': t.project_id,
            'creator_username': t.creator.username if t.creator else 'System',
            'dev_username': t.assigned_developer.username if t.assigned_developer else 'Unassigned',
            'created_at': t.created_at.strftime('%Y-%m-%d %H:%M') if t.created_at else ''
        } for t in qs]
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
        except Exception:
            body = request.POST

        creator = request.user if request.user.is_authenticated else User.objects.filter(role='tester').first() or User.objects.first()
        proj = Project.objects.filter(id=body.get('project_id')).first() or Project.objects.first()
        t = Ticket.objects.create(
            title=body.get('title', 'Bug Report'),
            description=body.get('description', ''),
            priority=body.get('priority', 'medium'),
            project=proj,
            creator=creator
        )
        return JsonResponse({'id': t.id, 'title': t.title, 'message': 'Created'}, status=201)

@csrf_exempt
def api_ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket.objects.select_related('project', 'creator', 'assigned_developer'), pk=pk)
    if request.method == 'GET':
        comments = [{
            'id': c.id,
            'username': c.user.username if c.user else 'User',
            'content': c.content,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M') if c.created_at else ''
        } for c in ticket.comments.select_related('user').order_by('created_at')]

        return JsonResponse({
            'id': ticket.id,
            'title': ticket.title,
            'description': ticket.description,
            'priority': ticket.priority,
            'status': ticket.status,
            'project_name': ticket.project.name if ticket.project else 'General',
            'project_id': ticket.project_id,
            'creator_username': ticket.creator.username if ticket.creator else 'System',
            'dev_username': ticket.assigned_developer.username if ticket.assigned_developer else 'Unassigned',
            'assigned_dev_id': ticket.assigned_developer_id,
            'created_at': ticket.created_at.strftime('%Y-%m-%d %H:%M') if ticket.created_at else '',
            'comments': comments
        })
    elif request.method in ['PUT', 'PATCH', 'POST']:
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception:
            data = request.POST
        if 'status' in data and data['status']:
            ticket.status = data['status']
        if 'priority' in data and data['priority']:
            ticket.priority = data['priority']
        if 'assigned_dev_id' in data and data['assigned_dev_id']:
            ticket.assigned_developer = User.objects.filter(id=data['assigned_dev_id']).first()
        ticket.save()
        return JsonResponse({'id': ticket.id, 'status': ticket.status, 'message': 'Updated'})

@csrf_exempt
def api_ticket_comments(request, pk):
    if request.method == 'POST':
        ticket = get_object_or_404(Ticket, pk=pk)
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception:
            data = request.POST
        user = request.user if request.user.is_authenticated else User.objects.filter(role='developer').first() or User.objects.first()
        c = Comment.objects.create(ticket=ticket, user=user, content=data.get('content', ''))
        return JsonResponse({'id': c.id, 'message': 'Comment added'}, status=201)
    return JsonResponse({'detail': 'Method not allowed'}, status=405)

