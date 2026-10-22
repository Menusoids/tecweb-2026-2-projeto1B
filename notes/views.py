import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
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


# API REST consumida pelo notes-frontend (React)
# ponytail: JsonResponse puro no lugar do Django REST framework, sem dependência nova
def note_json(note):
    return {'id': note.id, 'title': note.title, 'content': note.content}


@csrf_exempt
def api_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == 'PUT':
        data = json.loads(request.body)
        note.title = data['title']
        note.content = data['content']
        note.save()

    if request.method == 'DELETE':
        note.delete()
        return HttpResponse(status=204)

    return JsonResponse(note_json(note))


@csrf_exempt
def api_notes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Note.objects.create(title=data['title'], content=data['content'])

    return JsonResponse([note_json(n) for n in Note.objects.all()], safe=False)
