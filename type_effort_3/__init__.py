
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'type_effort_3'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    def creating_session(subsession):
        subsession.group_randomly()



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    num_correct = models.IntegerField()
    ball = models.StringField()  
    multiplier = models.FloatField()
    effort = models.IntegerField()
    points = models.IntegerField()    
    c1 = models.IntegerField(blank=False, label ="28+75=")
    c2 = models.IntegerField(blank=False, label ="64+31=")
    c3 = models.IntegerField(blank=False, label ="34+21=")
    c4 = models.IntegerField(blank=False, label ="54+67=")
    c5 = models.IntegerField(blank=False, label ="25+83=")
    c6 = models.IntegerField(blank=False, label ="27+92=")
    c7 = models.IntegerField(blank=False, label ="79+96=")
    c8 = models.IntegerField(blank=False, label ="38+75=")
    c9 = models.IntegerField(blank=False, label ="30+78=")
    c10 = models.IntegerField(blank=False, label ="37+34=")
    c11 = models.IntegerField(blank=False, label ="51+93=")
    c12 = models.IntegerField(blank=False, label ="28+76=")
    
    fairness = models.IntegerField(blank=False,choices=[[1, 'Very unfair'],[2, 'Somewhat unfair'],[3, 'Somewhat fair'],[4, 'Very fair']],widget=widgets.RadioSelect,
    label="How fair did you find the method of distributing payment based on your type, in the first two tasks?")
    fairness_text = models.LongStringField(label="Why do you think the method of distributing payment based on your type was unfair/fair?")


def draw_ball():
    import random 
    return random.choice(["black", "white"])
    
def get_multiplier(chosen_type, ball):
    if ball == "black":
        return 1 if chosen_type == "A" else 1/3
    else:  # white
        return 1/3 if chosen_type == "A" else 1

"""class Matching(WaitPage): 
    group_by_arrival_time = True
    body_text = "Please, wait to be match you into a group with 5 other people."
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
"""

class Round3(Page):
    timeout_seconds = 180
    form_model = 'player'
    form_fields = ['c1', 'c2', 'c3', 'c4',
                   'c5', 'c6', 'c7', 'c8',
                   'c9', 'c10', 'c11', 'c12']

    def is_displayed(player: Player):
        return player.round_number == 1 and player.participant.choice == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        solutions = [28+75, 64+31, 34+21, 54+67, 25+83, 27+92, 79+96, 38+75, 30+78, 37+34, 51+93, 28+76]
        answers = [player.c1, player.c2, player.c3, player.c4,
                   player.c5, player.c6, player.c7, player.c8,
                   player.c9, player.c10, player.c11, player.c12]
        player.num_correct = sum(a == s for a, s in zip(answers, solutions))
        player.effort = player.num_correct * 25

class FeedBack(Page):
    form_model = 'player'
    form_fields = ['fairness', 'fairness_text']
    def is_displayed(player):
        return player.round_number == 1
        
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.ball = draw_ball()
        player.multiplier = get_multiplier(player.participant.chosen_type, player.ball)
        if player.participant.choice == 2:
            player.payoff = cu(1.2)

        elif player.participant.choice == 1:
            others = player.get_others_in_group()
            #others_choices = [p.participant.choice for p in others]  # list of choices
            others_choices = [p.participant.field_maybe_none(choice) for p in others]
            n_opt_out_others = sum(1 for c in others_choices if c == 2)
            player.payoff = (2.50 - 0.25 * n_opt_out_others) *  player.multiplier
            


class End(Page):
  def is_displayed(player):
      return player.round_number == 1





page_sequence = [Round3, FeedBack,End]
# Matching

