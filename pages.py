from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class InstructionsRead(Page):
    def is_displayed(self):
        return self.round_number == 1


class Decision(Page):
    form_model = 'player'
    form_fields = ["choice_id"]

    def vars_for_template(self):
        self.player.coop_id = self.player.participant.vars["cooperators"][self.round_number-1]
        self.player.noncoop_id = self.player.participant.vars["defectors"][self.round_number-1]
        self.player.left_is_coop = self.player.participant.vars["left_is_coop"][self.round_number-1]
        return {
            "coop_pic": "coopfacevoice/{}.JPG".format(self.player.coop_id),
            "noncoop_pic": "coopfacevoice/{}.JPG".format(
                self.player.noncoop_id),
            "left_is_coop" : self.player.left_is_coop  # just to see it during the demo
        }

    def before_next_page(self):
        for p in self.group.get_players():
            p.set_period_payoff()


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {"period_selected_for_pay":
                    self.player.participant.vars["period_selected_for_pay"]}


class End(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {"subsession_payoff": c(self.participant.vars["coopfacevoice__payoff"]).to_real_world_currency(self.session)}


page_sequence = [Instructions, InstructionsRead, Decision, Results, End]
