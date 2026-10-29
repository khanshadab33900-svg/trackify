#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Automatically seed demo users if not present so live deployment works out of the box
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bug_tracker.settings')
django.setup()
from tracker.models import User, Project, Ticket, Comment

if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    admin.role = 'admin'
    admin.save()
    
    dev, _ = User.objects.get_or_create(username='rahul_dev', defaults={'role': 'developer'})
    dev.set_password('admin123')
    dev.save()

    tester, _ = User.objects.get_or_create(username='sneha_qa', defaults={'role': 'tester'})
    tester.set_password('admin123')
    tester.save()

    p1, _ = Project.objects.get_or_create(name='E-Commerce Cloud Microservices', defaults={'description': 'Microservices backend for payment processing, cart checkout, and inventory sync.', 'status': 'active'})
    p2, _ = Project.objects.get_or_create(name='College Mobile App v2', defaults={'description': 'Cross-platform flutter application for student attendance, timetable, and campus alerts.', 'status': 'active'})
    
    t1, _ = Ticket.objects.get_or_create(
        title='High memory spike on checkout endpoint under concurrent load',
        defaults={'description': 'Handling 500+ requests/sec causes thread pool exhaustion.', 'priority': 'high', 'status': 'in_progress', 'project': p1, 'creator': tester, 'assigned_developer': dev}
    )
    t2, _ = Ticket.objects.get_or_create(
        title='OAuth Google Sign-in fails on Android 14 devices',
        defaults={'description': 'Users report NullPointerException on authorization callback.', 'priority': 'high', 'status': 'open', 'project': p2, 'creator': tester}
    )
    Comment.objects.create(ticket=t1, user=dev, content='Identified connection pool leak. Patch deployed.')
    print('Successfully auto-seeded Render production demo data!')
"
