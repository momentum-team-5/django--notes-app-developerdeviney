from django.shortcuts import render, get_object_or_404
from .models import Note
from .forms import NoteForm

# Create your views here.
def notes_list(request):
    notes = Note.objects.all()
    return render(request, "notes/notes_list.html", {"notes": notes})


def note_detail(request, pk):
    note = get_object_or_404(Contact, pk=pk)
    note = Note.objects.filter(contact=contact)
    
    if note:
        note = note[0]

    else:
        note = None

    return render(request, "contacts/detail_contact.html", {"contact": contact, "note": note})


def add_note(request):
    if request.method == 'GET':
        form = NoteForm()

    else:
        form = NoteForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='list_contacts')

    return render(request, "notes/add_note.html", {"form": form})


def edit_note(request, pk):
    note = get_object_or_404(Contact, pk=pk)
    if request.method == 'GET':
        form = NoteForm(instance=note)
    else:
        form = NoteForm(data=request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect(to='notes_list')

    return render(request, "notes/edit_note.html", {
        "form": form,
        "contact": contact
    })


def delete_note(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect(to='notes_list')

    return render(request, "notes/delete_note.html",
                  {"note": note})


def add_note(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    if request.method == 'GET':
        form = NoteForm()

    else:
        form = NoteForm(data=request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.notes = note

            note.save()
            return redirect(to='list_contacts')

    return render(request, "notes/add_note.html", {"form": form, "note": note})
