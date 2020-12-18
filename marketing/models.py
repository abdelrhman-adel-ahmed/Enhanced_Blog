from django.db import models


class Signup(models.Model):
    email=models.EmailField()
    timestamp=models.DateTimeField(auto_now_add=True)
