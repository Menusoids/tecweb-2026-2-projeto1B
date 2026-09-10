from django.shortcuts import render, redirect
from .models import Note


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        Note.objects.create(title=title, content=content)
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
        return redirect('index')
    else:
        note = Note.objects.get(id=id)
        return render(request, 'notes/update.html', {'note': note})

