from django.db import models

class Tag(models.Model):
    nome = models.CharField(max_length=200)

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True)
    tag = models.ForeignKey(Tag, null=True, on_delete=models.CASCADE)

    def __str__(self):
        ret = f'{self.id}. {self.title}'
        return ret
