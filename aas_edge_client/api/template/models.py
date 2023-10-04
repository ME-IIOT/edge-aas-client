from django.db import models

class Template(models.Model):
    template_name = models.CharField(max_length=255, unique=True)
    content = models.JSONField()

    def __str__(self):
        return self.template_name
