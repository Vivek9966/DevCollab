from django.db import models
from django.conf import settings
from projects.models import Projects
# Create your models here.
User  =settings.AUTH_USER_MODEL

class Task(models.Model):
    STATUS_CHOICES = [
        ('to_do',"TO_DO"),
        ('in_progress','IN_PROGRESS'),
        ('done',"DONE"),
        ('abandoned','ABANDONED')
    ] 
    name = models.CharField(max_length=255,null=False,blank=False)
    status = models.CharField( max_length=20,choices=STATUS_CHOICES, default='to_do')
    project = models.ForeignKey(to=Projects,on_delete=models.CASCADE,related_name='tasks')
    assigned_to = models.ForeignKey(to=User,blank=True,null=True,on_delete=models.SET_NULL,related_name='assigned_tasks')
    created_by  =models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='cerated_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=255)
    title = models.CharField(blank=True)

    def __str__(self):
        return f"{self.title} project {self.project}"