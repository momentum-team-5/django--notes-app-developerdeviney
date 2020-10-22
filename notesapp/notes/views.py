from django.shortcuts import render, get_object_or_404
from django.contrib.messages import success, error
from django.core.mail import send_mail, mail_admins
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm, ContactForm, SearchForm

# Create your views here.
def notes_list(request):
    notes = Note.objects.all()

    return render(request, "notes/notes_list.html", {"notes": notes})


def notes_details(request, pk):
    note = get_object_or_404(Note, pk=pk)
    
    return render(request, "notes/notes_details.html", {"note": note})

@login_required
def add_note(request):
    if request.method == GET:
        form = NoteForm()
    else:
        form = NoteForm(data=request.POST)
        if form.is_valid():
            note =form.save(commit=False)
            form.save()
            return redirect(to='notes_list')
        else:
            error(request, "We got a complicated order.")
    
    return render(request, "notes/add_note.html", {"form": form})

@login_required
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == GET:
        form = NoteForm(instance=note)
    else:
        form = NoteForm(data=request.POST, instance=note)
        if form.is_valid():
            form.save()
            
            return redirect(to='notes_list')
    
    return render(request, "notes/edit_note.html", {"form": form, "note": note})

@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == POST:
        note.delete()
        return redirect(to='notes_list')

def contact_us(request):
    if request.method == GET:
        form =ContactForm()

    else:
        form = ContactForm(data=request.POST)

        if form.is_valid():
            user_email = form.cleaned_data['email']
            message_title = form.cleaned_data['title']
            message_body = form.cleaned_data['body']

            send_mail("We received your message", "We received your message...Please check your email.", None, recipient_list=[user_email])
            mail_admins(message_title, message_body, fail_silently=True)   
        
            return redirect(to='notes_list')

        else:
            error("We got a complicated order")
    
    return render(request, "contact_us.html", {"form": form})

def search(request):
    if request.method == GET:
        form = SearchForm()
    
    elif request.method == POST:
        form = SearchForm(data=request.POST)

    if form.is_valid():
        title = form.cleaned_data["title"]
        order_by = form.cleaned_data['order_by']
        note = Note.objects.filter(title__contains=title).order_by(order_by)

        return render(request, "notes/search_results.html", {"notes": note})

    return render(request, "notes/search.html", {"form": form})

