from django.shortcuts import render, redirect
from .models import Note, Tag


def get_tags(request):
    # "tag1, tag2" -> lista de Tag; vazio = nota sem tag; nome novo cria a tag na hora
    nomes = {n.strip() for n in request.POST.get('tags', '').split(',') if n.strip()}
    return [Tag.objects.get_or_create(nome=nome)[0] for nome in nomes]


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        note = Note.objects.create(title=title, content=content)
        note.tags.set(get_tags(request))
        return redirect('index')
    else:
        all_notes = Note.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes})

def delete(request, id):
    Note.objects.get(id=id).delete()
    return redirect('index')

def update(request, id):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        note = Note.objects.get(id=id)
        note.title = title
        note.content = content
        note.save()
        note.tags.set(get_tags(request))
        return redirect('index')
    else:
        note = Note.objects.get(id=id)
        return render(request, 'notes/update.html', {'note': note})

def tags(request):
    return render(request, 'notes/tags.html', {'tags': Tag.objects.all()})

def tag_detail(request, id):
    tag = Tag.objects.get(id=id)
    return render(request, 'notes/tag.html', {'tag': tag, 'notes': tag.note_set.all()})
