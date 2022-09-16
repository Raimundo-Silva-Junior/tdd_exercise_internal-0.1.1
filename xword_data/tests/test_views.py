from bs4 import BeautifulSoup
from django.test import TestCase, tag
from django.urls import reverse

from ..models import Clue
from .factories import ClueFactory, EntryFactory


class TestDrillView(TestCase):

    def setUp(self):
        for _unused in range(10):
            ClueFactory()
        self.url = reverse('xword-drill')

    def test_drill_get(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        soup = BeautifulSoup(response.content, features="html.parser")
        # The page has a form
        form = soup.find('form')
        self.assertTrue(form is not None)
        # The form has a text field named "answer"
        self.assertTrue(form.find('input', attrs={'name': 'answer', 'type': 'text'}))
        # The page also offers an escape link to get the answer
        clue_id = response.context['clue_id']
        answer_link_url = reverse('xword-answer', args=(clue_id,))
        self.assertTrue(soup.find('a', attrs={'href': answer_link_url}))

    def test_drill_post_incorrect(self):
        clue = Clue.objects.order_by("?").first()
        data = {
            "clue_id": clue.id,
            "answer": clue.entry.entry_text + 'wrong'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "not correct")

    def test_drill_post_correct(self):
        clue = Clue.objects.order_by("?").first()
        data = {
            "clue_id": clue.id,
            "answer": clue.entry.entry_text.lower()
        }
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, reverse('xword-answer', args=(clue.id,)))

    @tag('stats')
    def test_drill_messaging(self):
        # Request the page 3 times, provide 1 correct answer
        self.client.get(self.url)
        self.client.get(self.url)
        response = self.client.get(self.url)
        clue = Clue.objects.get(pk=response.context["clue_id"])
        data = {
            "clue_id": clue.id,
            "answer": clue.entry.entry_text
        }
        response = self.client.post(self.url, data=data, follow=True)
        self.assertRedirects(response, reverse('xword-answer', args=(clue.id,)))
        # Answer page should show status of how many correct answers have been provided.
        self.assertContains(
            response,
            f"{clue.entry.entry_text} is the correct answer! You have now answered 1 (of 3) clues correctly")


class TestAnswerView(TestCase):

    def setUp(self):
        clue_text = "Still"
        entry = EntryFactory(entry_text="ATREST")
        for _unused in range(3):
            ClueFactory(entry=entry, clue_text=clue_text)
        entry = EntryFactory(entry_text="YET")
        for _unused in range(2):
            ClueFactory(entry=entry, clue_text=clue_text)
        entry = EntryFactory(entry_text="SILENT")
        ClueFactory(entry=entry, clue_text=clue_text)

    @tag('stats')
    def test_answer_stats(self):
        # All clues in setup have the same text, any one chosen at random
        # should show the same table of stats for use of that clue.
        clue = Clue.objects.order_by("?").first()
        response = self.client.get(reverse("xword-answer", args=(clue.pk,)))
        self.assertEqual(200, response.status_code)
        soup = BeautifulSoup(response.content, features="html.parser")
        table = soup.find("table")
        self.assertTrue(table)
        rows = table.find_all("tr")
        # table should 4 rows: header and 3 data rows
        self.assertEqual(4, len(rows))
        self.assertTrue(rows[0].find("th", text="Count"))
        self.assertTrue(rows[0].find("th", text="Entry"))
        self.assertTrue(rows[1].find("td", text="3"))
        self.assertTrue(rows[1].find("td", text="ATREST"))
        self.assertTrue(rows[2].find("td", text="2"))
        self.assertTrue(rows[2].find("td", text="YET"))
        self.assertTrue(rows[3].find("td", text="1"))
        self.assertTrue(rows[3].find("td", text="SILENT"))

    @tag('stats')
    def test_answer_unique(self):
        clue = ClueFactory(clue_text="Unique", entry=EntryFactory(entry_text="SINGLE"))
        response = self.client.get(reverse("xword-answer", args=(clue.pk,)))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "only appearance of this clue")

    def test_answer_nonexistent(self):
        # Rely on DB not using primary key value of 0
        response = self.client.get(reverse("xword-answer", args=(0,)))
        self.assertEqual(404, response.status_code)
