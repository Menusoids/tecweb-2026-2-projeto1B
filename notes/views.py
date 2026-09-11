from django.shortcuts import render, redirect
from .models import Note, Tag


def get_tag(request):
    # tag vazia = nota sem tag; nome novo cria a tag na hora
    tag_nome = request.POST.get('tag', '').strip()
    if not tag_nome:
        return None
    tag, _ = Tag.objects.get_or_create(nome=tag_nome)
    return tag


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        Note.objects.create(title=title, content=content, tag=get_tag(request))
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
        note.tag = get_tag(request)
        note.save()
        return redirect('index')
    else:
        note = Note.objects.get(id=id)
        return render(request, 'notes/update.html', {'note': note})

def tags(request):
    return render(request, 'notes/tags.html', {'tags': Tag.objects.all()})

def tag_detail(request, id):
    tag = Tag.objects.get(id=id)
    return render(request, 'notes/tag.html', {'tag': tag, 'notes': tag.note_set.all()})
