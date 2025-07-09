from django.db import models




class attendees(models.Model):
    email = models.CharField(max_length=20)
    user_name = models.CharField(max_length=200)
    pass_code = models.TextField()
    full_name = models.CharField(max_length=50)

class organizers(models.Model):


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
