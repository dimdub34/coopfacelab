from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.translation import ugettext


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class InstructionsRead(Page):
    def is_displayed(self):
        return self.round_number == 1


class Demographic(Page):
    form_model = "player"
    form_fields = ["age", "gender", "student", "student_level",
                   "student_discipline", "sport", "experience"]

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def error_message(self, values):
        if values["student"] and (values["student_level"] is None or
        values["student_discipline"] is None):
            return ugettext("If you are a student you must select "
                           "your level of study and the displine "
                           "you are studying")

class Final(Page):
    form_model = "player"
    form_fields = ["comments"]

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Final_after_comments(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


# ==============================================================================
#
# Public goods
#
# ==============================================================================

class PGDecision(Page):
    form_model = 'player'
    form_fields = ['PG_contribution']

    def is_displayed(self):
        return self.round_number == 1


class PGResultsWaitPage(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1

    def after_all_players_arrive(self):
        for g in self.subsession.get_groups():
            g.pg_set_payoffs()


class PGResults(Page):
    def is_displayed(self):
        return self.round_number == 1


class PGEnd(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            "pg_payoff": self.player.PG_payoff.to_real_world_currency(self.session)
        }


# ==============================================================================
#
# Cooperation face
#
# ==============================================================================

class CFDecision(Page):
    form_model = 'player'
    form_fields = ["CF_choice"]

    def vars_for_template(self):
        self.player.CF_cooperator = \
            self.player.participant.vars["CF_cooperators"][self.round_number-1]
        self.player.CF_defector = \
            self.player.participant.vars["CF_defectors"][self.round_number-1]
        self.player.CF_cooperator_on_left = \
            self.player.participant.vars["CF_left_is_coop"][self.round_number-1]
        return {
            "coop_pic": "coopfacelab/{}.JPG".format(self.player.CF_cooperator),
            "noncoop_pic": "coopfacelab/{}.JPG".format(
                self.player.CF_defector),
            "left_is_coop" : self.player.CF_cooperator_on_left  # just to see it during the demo
        }

    def before_next_page(self):
        for p in self.group.get_players():
            p.set_cf_period_payoff()


class CFResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {"period_selected_for_pay":
                    self.player.participant.vars["CF_period_selected_for_pay"]}

class CFEnd(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            "cf_payoff": self.player.CF_payoff.to_real_world_currency(self.session)
        }




page_sequence = [
    Instructions, InstructionsRead,
    PGDecision, PGResultsWaitPage, PGResults, PGEnd,
    Instructions, InstructionsRead,
    CFDecision, CFResults, CFEnd,
    Demographic,
    Final, Final_after_comments]
