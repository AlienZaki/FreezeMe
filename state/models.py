from django.db import models


class State(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, unique=True)
    abbreviation = models.CharField(max_length=2, null=True, blank=True, unique=True)

    def __str__(self):
        return f'{self.abbreviation} - {self.name}'

    class Meta:
        ordering = ['name']