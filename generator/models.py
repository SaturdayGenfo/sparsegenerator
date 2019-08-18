from django.db import models
from .libs.white_noise import white_noise

class Law(models.Model):
    law_name = models.CharField(max_length=20)
