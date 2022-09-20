from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.urls import reverse
from .models import Puzzle, Entry, Clue


class EntryText(ModelForm):
    class Meta:
        model = Entry
        fields = ['entry_text']
        
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        
        context_data = super(HomeView, self).get_context_data(**kwargs)

        self.request.session['total_score'] = 0
        self.request.session['correct_answer'] = 0
        self.request.session['repeat'] = False

        if self.request.session.has_key('clue_id') is True:
            del self.request.session['clue_id']

        return context_data

class DrillView(TemplateView):
    template_name = 'drill.html'

    def get_context_data(self, **kwargs):
        
        context_data = super(DrillView, self).get_context_data(**kwargs)
        repeat = False

        if self.request.session.has_key('repeat') is True:
           repeat = self.request.session['repeat']

        if repeat is True:
            clue_id = self.request.session['clue_id']
            random_clue = Clue.objects.get(pk=clue_id)
        else:
           random_clue = Clue.objects.order_by("?").first()
           clue_id = random_clue.id

           self.request.session['clue_id'] = clue_id
           self.request.session['success'] = False
           self.request.session['total_score'] += 1
           
        context_data['entry_text'] = EntryText()
        context_data['random_clue'] = random_clue
        context_data['repeat'] = repeat

        context_data['total_score'] = self.request.session['total_score']
        context_data['correct_answer'] = self.request.session['correct_answer']

        return context_data
    
    def post(self, request, *args, **kwargs):
        
        if request.session.has_key('clue_id') is False:
            self.request.session['repeat'] = False
            return HttpResponseRedirect(reverse('xword-drill'))

        clue_id = self.request.session['clue_id']

        entry_form = EntryText(request.POST or None)
        entry_text = entry_form['entry_text'].value()

        clue_match = Clue.objects.get(pk=clue_id)
        entry_match = Entry.objects.filter(entry_text=entry_text.upper()).first()

        if entry_match == clue_match.entry:
            self.request.session['correct_answer'] += 1
            self.request.session['repeat'] = False
            self.request.session['success'] = True
            
            return HttpResponseRedirect(reverse('xword-answer'))
        else:
            request.session['repeat'] = True

            return HttpResponseRedirect(reverse('xword-drill'))

class AnswerView(TemplateView):
    template_name = 'answer.html'

    def get_context_data(self, **kwargs):
        
        context_data = super(AnswerView, self).get_context_data(**kwargs)

        if self.request.session.has_key('clue_id') is False:
            return HttpResponseRedirect(reverse('xword-drill'))

        if self.request.session.has_key('repeat') is True:
            self.request.session['repeat'] = False

        clue_id = self.request.session['clue_id']
        clue = Clue.objects.get(pk=clue_id)
        other_clues =  Clue.objects.filter(entry=clue.entry)
        puzzles = Puzzle.clue_objects.get_clue(clue.clue_text)

        context_data['puzzles'] = puzzles
        context_data['clue'] = clue
        context_data['other_clues'] = other_clues

        context_data['total_score'] = self.request.session['total_score']
        context_data['correct_answer'] = self.request.session['correct_answer']
        context_data['success'] = self.request.session['success']

        return context_data   