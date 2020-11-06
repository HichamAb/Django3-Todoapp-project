from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TodoModel(models.Model) : 
    title = models.CharField(max_length=100)
    note  = models.CharField(max_length=250)
    is_important=models.BooleanField(default=False)
    added_on=models.DateTimeField(auto_now_add=True)
    finished_on=models.DateTimeField(null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE) 

    def __str__(self) : 
        return self.title
