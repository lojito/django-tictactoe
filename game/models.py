from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    board = models.CharField(max_length=16)
    created = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created']
    
