from django.db import models
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        assign_perm('change_mymodel', self.owner, self)
        assign_perm('delete_mymodel', self.owner, self)