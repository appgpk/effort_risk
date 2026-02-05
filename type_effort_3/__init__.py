
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
    multiplier_display = models.StringField()
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
    nb_opt_out = models.IntegerField()
    fairness = models.IntegerField(blank=False,choices=[[1, 'Very unfair'],[2, 'Somewhat unfair'],[3, 'Somewhat fair'],[4, 'Very fair']],widget=widgets.RadioSelect,
    label="How fair did you find the method of distributing payment based on your type, in the first two tasks?")
    fairness_text = models.LongStringField(label="Why do you think the method of distributing payment based on your type was unfair/fair?", blank = True)


def draw_ball():
    import random 
    return random.choice(["black", "white"])
    
def get_multiplier(chosen_type, ball):
    if ball == "black":
        return 1 if chosen_type == "A" else 1/3
    else:  # white
        return 1/3 if chosen_type == "A" else 1

def set_payoffs(group: Group):
    players = group.get_players()

    for p in players:
        # Count how many OTHER players chose 2
        others = p.get_others_in_group()
        n_opt_out_others = sum(o.participant.choice == 2 for o in others)
        p.nb_opt_out = n_opt_out_others
        p.ball = draw_ball()
        p.multiplier = get_multiplier(p.participant.chosen_type, p.ball)       
        if p.multiplier == 1 : 
            p.multiplier_display = "1"
        else : 
            p.multiplier_display = "1/3"
        #  payoff rule
        if p.participant.choice == 2:
            p.payoff = cu(0.83)
        elif p.participant.choice == 1:
            p.points = int(round(p.effort * p.multiplier))
            p.payoff = cu(2.50 - 0.25 * n_opt_out_others) * p.multiplier
        else:
            p.points = int(round(p.effort * p.multiplier))
            p.payoff = cu(0)



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
        if timeout_happened:
            player.c1  = 0 if player.c1  is None else player.c1
            player.c2  = 0 if player.c2  is None else player.c2
            player.c3  = 0 if player.c3  is None else player.c3
            player.c4  = 0 if player.c4  is None else player.c4
            player.c5  = 0 if player.c5  is None else player.c5
            player.c6  = 0 if player.c6  is None else player.c6
            player.c7  = 0 if player.c7  is None else player.c7
            player.c8  = 0 if player.c8  is None else player.c8
            player.c9  = 0 if player.c9  is None else player.c9
            player.c10 = 0 if player.c10 is None else player.c10
            player.c11 = 0 if player.c11 is None else player.c11
            player.c12 = 0 if player.c12 is None else player.c12
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
        

            


class End(Page):
  def is_displayed(player):
      return player.round_number == 1


class Matching(WaitPage): 
    after_all_players_arrive = set_payoffs
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class Result3(Page):
    form_model = 'player'

    def is_displayed(player):
        return player.round_number == 1 
    @staticmethod
    def vars_for_template(self):
        participant = self.participant

        if participant.choice == 1:
            return dict(
                choice=self.participant.choice,
                ball=player.ball,
                playerType=player.chosen_type,
                effort=player.effort,
                multiplier=player.multiplier_display,
                points=player.points,
                payoff=player.payoff,
                nb_opt_out=player.nb_opt_out,
            )
        else:
            return dict(
                choice=self.participant.choicee,
                ball=player.ball,
                playerType=player.chosen_type,
                multiplier=player.multiplier_display,
                payoff=player.payoff,
                nb_opt_out=player.nb_opt_out,
            )



page_sequence = [Round3, FeedBack, Matching, Result3, End]




