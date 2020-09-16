from django.db import models

class Link(models.Model):
    code = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.code} : {self.url}"
