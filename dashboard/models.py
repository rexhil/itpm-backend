from django.db import models


# Create your models here.


class Menu(models.Model):
    menu_icon = models.CharField(max_length=20, null=False)
    menu_name = models.CharField(max_length=20, null=False)
    menu_parent_id = models.CharField(max_length=20, null=False)
    menu_url = models.CharField(max_length=20, null=False)
