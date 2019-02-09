from django.db import models


class Mem(models.Model):
    title = models.CharField(max_length=300, null=True)
    description = models.TextField()
    image = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class WhiteId(models.Model):
    name = models.CharField(max_length=100)
    mid = models.IntegerField(unique=True)

    def __str__(self):
        return f'({self.mid}) {self.name}'
