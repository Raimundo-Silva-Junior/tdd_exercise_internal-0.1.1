from django.db import models
from django.db.models.manager import Manager
from django.db.models.deletion import CASCADE

class PuzzleManager(Manager):
    
    def get_clue(self, clue_text):
        return self.filter(puzzle_clue__clue_text=clue_text)

class Puzzle(models.Model):
    
    title = models.CharField(max_length=255)
    date = models.DateField()
    byline = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)

    clue_objects = PuzzleManager()
    
    def __str__(self):
        return f"{self.byline} published by {self.publisher} on {self.date}"
    
class Entry(models.Model):
    
    entry_text = models.CharField(
        unique=True, 
        max_length=50
        )
    
    def __str__(self):
        return self.entry_text
    
class Clue(models.Model):
    
    entry = models.ForeignKey(
        Entry, on_delete=CASCADE,
        related_name="entry_clue"
        )
    puzzle = models.ForeignKey(
        Puzzle, 
        on_delete=CASCADE, 
        related_name="puzzle_clue"
        )
    clue_text = models.CharField(
        max_length=512
        )
    theme = models.BooleanField(
        default=False
        )

    def __str__(self):
        return f'"{self.entry.entry_text}" - {self.clue_text}'
    

    



