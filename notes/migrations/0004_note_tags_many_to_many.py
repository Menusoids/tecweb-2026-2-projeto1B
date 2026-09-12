from django.db import migrations, models


def copia_tag_para_tags(apps, schema_editor):
    Note = apps.get_model('notes', 'Note')
    for note in Note.objects.exclude(tag=None):
        note.tags.add(note.tag)


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_tag_note_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='tags',
            field=models.ManyToManyField(blank=True, to='notes.tag'),
        ),
        migrations.RunPython(copia_tag_para_tags, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='note',
            name='tag',
        ),
    ]
