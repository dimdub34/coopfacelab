from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


author = 'Dimitri DUBOIS'

doc = """
Selection of cooperative players based on a picture of their face
"""


class Constants(BaseConstants):
    name_in_url = 'coopfacevoice'
    players_per_group = None
    contribution = 20
    endowment = 20
    mpcr = 0.6
    noncoop = 0
    coop = 1
    cooperators = ["1_201016", "11_120117", "11_160117", "17_090117", "5_120117", "7_090117", "7_171016"]
    defectors = ["1_081116", "1_130117", "1_181016", "11_090117", "13_090117", "15_211016", "5_171016"]
    num_rounds = len(cooperators)


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars["cooperators"] = Constants.cooperators.copy()
                random.shuffle(p.participant.vars["cooperators"])
                p.participant.vars["defectors"] = Constants.defectors.copy()
                random.shuffle(p.participant.vars["defectors"])
                # on détermine si à gauche ou à droite on met la photo du
                # coopérateur / défecteur
                p.participant.vars["left_is_coop"] = \
                    [random.randint(0, 1) for _ in range(Constants.num_rounds)]
                p.participant.vars["period_selected_for_pay"] = random.randint(1, Constants.num_rounds)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    coop_id = models.StringField()
    noncoop_id = models.StringField()
    left_is_coop = models.BooleanField()
    choice_id = models.PositiveIntegerField(
        choices=[(0, "Gauche"), (1, "Droite")],
        widget=widgets.RadioSelectHorizontal)
    choose_cooperator = models.BooleanField()
    number_of_cooperators_found = models.IntegerField()
    period_selected_for_pay = models.BooleanField()
    part_payoff = models.CurrencyField()

    def set_period_payoff(self):
        if not self.left_is_coop:  # defector on the left on the screen
            self.choose_cooperator = True if self.choice_id == 1 else False
        else:  # cooperator on the left side of pictures
            self.choose_cooperator = True if self.choice_id == 0 else False

        # payoff depending on whether he choosed the cooperator
        self.payoff = Constants.contribution * 2 * Constants.mpcr if \
            self.choose_cooperator else Constants.contribution * Constants.mpcr

        if self.round_number == self.participant.vars["period_selected_for_pay"]:
            self.period_selected_for_pay = True
        else:
            self.period_selected_for_pay = False

        if self.round_number == Constants.num_rounds:
            # compute the number of "good" answer
            self.number_of_cooperators_found = sum(
                [p.choose_cooperator for p in self.in_all_rounds()])
            # compute the part payoff
            self.part_payoff = sum(
                [p.payoff for p in self.in_all_rounds() if
                 p.period_selected_for_pay])
            self.participant.vars["coopfacevoice_payoff"] = self.part_payoff
            self.participant.payoff = \
                self.participant.vars.get("public_goods_simple__payoff", 0) + \
                self.part_payoff
