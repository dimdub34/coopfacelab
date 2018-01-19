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
        yield (pages.Decision, {"choice_id": random.randint(0, 1)})
        if self.round_number == Constants.num_rounds:
            yield (pages.Results)
            yield Submission(pages.End, check_html=False)