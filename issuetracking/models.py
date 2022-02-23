from django.db import models


class Users(models.Model):
    user_id = models.IntegerField()
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.EmailField()
    password = models.CharField()


class Contributors(models.Model):
    pass


class Projects(models.Model):
    pass


class Issues(models.Model):
    pass


class Comments(models.Model):
    pass
