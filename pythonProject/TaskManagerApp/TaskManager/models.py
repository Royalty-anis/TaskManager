from django.db import models

class event(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=300)


class attendees(models.Model):
    email = models.CharField(max_length=20)
    user_name = models.CharField(max_length=200)
    pass_code = models.TextField()
    full_name = models.CharField(max_length=50)

class organizers(models.Model):
    organisation = models.CharField(max_length=40)

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)