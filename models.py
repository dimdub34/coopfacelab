from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.utils.translation import ugettext
import random


author = 'Dimitri DUBOIS'

doc = """
Selection of cooperative players based on a picture of their face
"""


class Constants(BaseConstants):
    name_in_url = 'coopfacelab'
    players_per_group = 2

    # parameters
    endowment = 20
    mpcr = 0.6
    cooperators = ["1_201016", "11_120117", "11_160117", "17_090117", "5_120117", "7_090117", "7_171016"]
    defectors = ["1_081116", "1_130117", "1_181016", "11_090117", "13_090117", "15_211016", "5_171016"]
    num_rounds = len(cooperators)

    # codes
    defector = 0
    cooperator = 1
    no_deaf = 0
    deaf_only = 1
    deaf_mix = 2
    in_lab = 0
    online = 1


class Subsession(BaseSubsession):
    experimental_room = models.IntegerField()
    treatment = models.IntegerField()

    def creating_session(self):
        self.experimental_room = Constants.in_lab
        self.treatment = self.session.config["treatment"]

        # creation of pairs of pictures
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars["CF_cooperators"] = Constants.cooperators.copy()
                random.shuffle(p.participant.vars["CF_cooperators"])
                p.participant.vars["CF_defectors"] = Constants.defectors.copy()
                random.shuffle(p.participant.vars["CF_defectors"])
                # we set the cooperator either on the left or on the right
                p.participant.vars["CF_left_is_coop"] = \
                    [random.randint(0, 1) for _ in range(Constants.num_rounds)]
                p.participant.vars["CF_period_selected_for_pay"] = random.randint(1, Constants.num_rounds)


class Group(BaseGroup):
    PG_group_contribution = models.IntegerField()

    def pg_set_payoffs(self):
        self.PG_group_contribution = sum([p.PG_contribution for p in self.get_players()])
        payoff_coll_account = float("{:.2f}".format(self.PG_group_contribution * Constants.mpcr))
        for p in self.get_players():
            p.PG_payoff_collective_account = payoff_coll_account
            p.PG_payoff_individual_account = Constants.endowment - p.PG_contribution
            p.PG_payoff = p.PG_payoff_individual_account + p.PG_payoff_collective_account
            p.payoff = p.PG_payoff
            p.participant.vars["pg_payoff"] = p.PG_payoff


class Player(BasePlayer):
    deaf = models.IntegerField()

    # public goods
    PG_contribution = models.IntegerField()
    PG_payoff_individual_account = models.FloatField()
    PG_payoff_collective_account = models.FloatField()
    PG_payoff = models.CurrencyField()

    # Cooperation face
    CF_cooperator = models.StringField()
    CF_defector = models.StringField()
    CF_cooperator_on_left = models.BooleanField()
    CF_choice = models.IntegerField(
        choices=[(0, ugettext("left")), (1, ugettext("right"))],
        widget=widgets.RadioSelectHorizontal)
    CF_choose_cooperator = models.BooleanField()
    CF_number_of_cooperators_found = models.IntegerField()
    CF_period_selected_for_pay = models.BooleanField()
    CF_payoff = models.CurrencyField()

    # Demographic
    age = models.IntegerField(
        label=ugettext('What is your age?'),
        min=13, max=125)
    gender = models.IntegerField(
        choices=[(0, ugettext('Female')), (1, ugettext('Male'))],
        label=ugettext('What is your gender?'),
        widget=widgets.RadioSelectHorizontal)
    student = models.IntegerField(
        choices=[(0, ugettext('No')), (1, ugettext('Yes'))],
        label=ugettext("Are you a student?"),
        widget=widgets.RadioSelectHorizontal)
    student_level = models.IntegerField(
        choices=[(0, ugettext('Bachelor')), (1, ugettext('Master')),
                 (3, ugettext('PhD')), (4, ugettext('Not in the list'))],
        blank=True)
    student_discipline = models.StringField(
        choices=[
            ugettext("Administration"), ugettext("Archeology"), ugettext("Biology"),
            ugettext("Buisiness school"), ugettext("Chemistry"),
            ugettext("Computer science"), ugettext("Economics"),
            ugettext("Education"), ugettext("Law"), ugettext("Management"),
            ugettext("Nursing school"), ugettext("Engineer"), ugettext("Geography"),
            ugettext("History"), ugettext("Lettres"), ugettext("Mathematics"),
            ugettext("Medicine"), ugettext("Music"), ugettext("Pharmacy"),
            ugettext("Philosophy"), ugettext("Physics"), ugettext("Politics"),
            ugettext("Sociology"), ugettext("Sport"), ugettext("Not in the list")
        ],
        label=ugettext("What are you studying?"), blank=True)
    sport = models.IntegerField(
        choices=[(0, ugettext('No')), (1, ugettext('Yes'))],
        label=ugettext("Do you pratice (regularly) some sport?"),
        widget=widgets.RadioSelectHorizontal)
    experience = models.IntegerField(
        choices=[(0, ugettext('No')), (1, ugettext('Yes'))],
        label=ugettext("Have you ever participated in an experiment?"),
        widget=widgets.RadioSelectHorizontal)
    comments = models.LongStringField(blank=True)

    def set_cf_period_payoff(self):
        if not self.CF_cooperator_on_left:  # defector on the left on the screen
            self.CF_choose_cooperator = True if self.CF_choice == 1 else False
        else:  # cooperator on the left side of pictures
            self.CF_choose_cooperator = True if self.CF_choice == 0 else False

        # payoff depending on whether he choosed the cooperator
        self.CF_payoff = Constants.endowment * 2 * Constants.mpcr if \
            self.CF_choose_cooperator else Constants.endowment * Constants.mpcr

        if self.round_number == self.participant.vars["CF_period_selected_for_pay"]:
            self.CF_period_selected_for_pay = True
        else:
            self.CF_period_selected_for_pay = False

        if self.round_number == Constants.num_rounds:
            # compute the number of "good" answer
            self.CF_number_of_cooperators_found = sum(
                [p.CF_choose_cooperator for p in self.in_all_rounds()])
            # compute the part payoff
            self.CF_payoff = sum(
                [p.CF_payoff for p in self.in_all_rounds() if
                 p.CF_period_selected_for_pay])
            self.participant.vars["cf_payoff"] = self.CF_payoff
            self.participant.payoff = \
                self.participant.vars["pg_payoff"] + self.CF_payoff
