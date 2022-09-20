from django.contrib import admin
from xword_data.models import Puzzle, Entry, Clue

admin.site.register(Puzzle)
admin.site.register(Entry)
admin.site.register(Clue)