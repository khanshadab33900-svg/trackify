from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('developer', 'Developer'),
        ('tester', 'Tester'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='tester')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Project(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name

class Ticket(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    screenshot = models.ImageField(upload_to='screenshots/', blank=True, null=True)
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tickets')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_developer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets', limit_choices_to={'role': 'developer'})

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.project.name}"

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.ticket.title}"
