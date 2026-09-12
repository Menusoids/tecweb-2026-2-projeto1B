from django.test import TestCase

from .models import Note, Tag


class TagsManyToManyTest(TestCase):
    def test_cria_edita_e_mostra_tags(self):
        self.client.post('/', {'titulo': 'n', 'detalhes': 'd', 'tags': 'a, b ,a'})
        note = Note.objects.get()
        self.assertEqual(sorted(note.tags.values_list('nome', flat=True)), ['a', 'b'])

        html = self.client.get(f'/{note.id}/update').content.decode()
        self.assertIn(f'value="{note.tag_names()}"', html)

        self.client.post(f'/{note.id}/update', {'titulo': 'n', 'detalhes': 'd', 'tags': 'b, c'})
        self.assertEqual(sorted(note.tags.values_list('nome', flat=True)), ['b', 'c'])
        self.assertEqual(Tag.objects.count(), 3)  # tags existentes reaproveitadas, sem duplicar

        self.client.post(f'/{note.id}/update', {'titulo': 'n', 'detalhes': 'd', 'tags': ''})
        self.assertEqual(note.tags.count(), 0)
