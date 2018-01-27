from otree.api import Currency as c, currency_range, Submission
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield (pages.Instructions)
            yield Submission(pages.InstructionsRead, check_html=False)
            yield (pages.PGDecision, {"PG_contribution": random.randint(0, Constants.endowment)})
            yield Submission(pages.PGResults, check_html=False)
            yield Submission(pages.PGEnd, check_html=False)
            yield (pages.Instructions)
            yield Submission(pages.InstructionsRead, check_html=False)
        yield (pages.CFDecision, {"CF_choice": random.randint(0, 1)})
        if self.round_number == Constants.num_rounds:
            yield (pages.CFResults)
            yield Submission(pages.CFEnd, check_html=False)
            yield (pages.Demographic,
                   {
                       "age": random.randint(15, 90),
                       "gender": random.randint(0, 1),
                       "student": random.randint(0, 1),
                       "student_level": random.randint(0, 2),
                       "student_discipline": random.randint(0, 8),
                       "sport": random.randint(0, 1),
                       "experience": random.randint(0, 1)
                   })
            yield (pages.Final, {"comments": "Automatic message"})