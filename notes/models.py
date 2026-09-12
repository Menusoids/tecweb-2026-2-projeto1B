from django.db import models

class Tag(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        ret = f'{self.id}. {self.title}'
        return ret

    def tag_names(self):
        # usado pra preencher o input de tags na edição
        return ', '.join(t.nome for t in self.tags.all())
