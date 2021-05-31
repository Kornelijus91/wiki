from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
import random
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, entry):
    return render(request, "encyclopedia/entry.html", {
        "name": entry,
        "entry": markdown2.markdown(util.get_entry(entry))
        })

def search(request):
    q = request.GET.get('q', '')
    entries = [x.lower() for x in util.list_entries()]
    display_entries = []
    if q.lower() in entries:
        return redirect("wiki", q)
    else:
        for entry in util.list_entries():
            if q.lower() in str(entry).lower():
                display_entries.append(entry)

        return render(request, "encyclopedia/search.html", {
        "result": display_entries
        })

def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]

        entries = [x.lower() for x in util.list_entries()]
        if title.lower() in entries:
            return render(request, "encyclopedia/new.html", {
                "alert": "display:block",
                "form": NewEntryForm(initial={
                    "title": title,
                    "description": description
                })
            })
        else:
            util.save_entry(title, description)
            return redirect("wiki", title)
    else:
        return render(request, "encyclopedia/new.html", {
            "alert": "display:none",
            "form": NewEntryForm()
        })

def edit(request, entry):
    if request.method == "POST":
        save = EditForm(request.POST)
        if save.is_valid():
            content = save.cleaned_data["edit"]
            util.save_entry(entry, content)
            return redirect("wiki", entry)
    else:
        description = util.get_entry(entry)
        return render(request, "encyclopedia/edit.html", {
            "title": entry,
            "description": description,
            "form": EditForm(initial={
                    "edit": description
                }) 
            })

def randomentry(request):
    entrylist = util.list_entries()
    page = random.choice(entrylist)
    return redirect("wiki", page)

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title:")
    description = forms.CharField(label="Description:", widget=forms.Textarea)

class EditForm(forms.Form):
    edit = forms.CharField(label="Description:", widget=forms.Textarea)