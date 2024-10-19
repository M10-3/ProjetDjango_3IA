from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Conferences
from django.views.generic import ListView, DetailView
# Create your views here.

def conferencesList(req):
    liste=Conferences.objects.all()
    return render(req, 'conferences/list.html', {'conferences':liste})

class ConferenceListView(ListView) :
    model=Conferences
    template_name = 'conferences/conferences_list.html'
    context_object_name = 'conferences'
    def get_queryset(self) :
        return Conferences.objects.order_by('-start_date')

class DetailsViewConference(DetailView):
    model=Conferences
    template_name = 'conferences/conferences_detail_view.html'
    context_object_name = 'conferences'