import datetime
import random

import factory

from ..models import Clue, Entry, Puzzle


class PuzzleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Puzzle

    title = factory.Faker("sentence")
    date = factory.Faker("past_date", start_date=datetime.date(1970, 1, 1))
    byline = factory.Faker("name")
    publisher = factory.Faker("random_element", elements=("NYT", "NYSun", "LAT", "WaPo", "USAToday"))


class EntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Entry
        django_get_or_create = ("entry_text",)

    entry_text = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for x in range(random.randint(3, 23)))


class ClueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Clue

    clue_text = factory.Faker("sentence")
    entry = factory.SubFactory(EntryFactory)
    puzzle = factory.SubFactory(PuzzleFactory)
