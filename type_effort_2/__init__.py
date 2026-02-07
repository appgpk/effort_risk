
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'type_effort_2'
    PLAYERS_PER_GROUP = None
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
    b1 = models.IntegerField(blank=False, label ="53+64=")
    b2 = models.IntegerField(blank=False, label ="78+95=")
    b3 = models.IntegerField(blank=False, label ="23+34=")
    b4 = models.IntegerField(blank=False, label ="13+66=")
    b5 = models.IntegerField(blank=False, label ="24+78=")
    b6 = models.IntegerField(blank=False, label ="95+67=")
    b7 = models.IntegerField(blank=False, label ="58+37=")
    b8 = models.IntegerField(blank=False, label ="67+84=")
    b9 = models.IntegerField(blank=False, label ="53+45=")
    b10 = models.IntegerField(blank=False, label ="78+76=")
    b11 = models.IntegerField(blank=False, label ="26+39=")
    b12 = models.IntegerField(blank=False, label ="42+57=")
    choice = models.IntegerField(blank=False,label ="Which do you choose?", choices=[[1, 'Participate in the math task and be paid according to the table above.'], [2, 'Opt out of the task and be paid $0.83.']],widget=widgets.RadioSelect)



    


def draw_ball():
    import random 
    return random.choice(["black", "white"])
    
def get_multiplier(chosen_type, ball):
    if ball == "black":
        return 1 if chosen_type == "A" else 1/3
    else:  # white
        return 1/3 if chosen_type == "A" else 1

class Round2(Page):
   timeout_seconds = 180
   form_model = 'player'
   form_fields = ['b1', 'b2', 'b3', 'b4',
                 'b5', 'b6', 'b7', 'b8',
                 'b9', 'b10', 'b11', 'b12']
   def is_displayed(player):
       return player.round_number == 1
   @staticmethod
   def before_next_page(player, timeout_happened):
       if timeout_happened:
            player.b1  = 0 if player.b1  is None else player.b1
            player.b2  = 0 if player.b2  is None else player.b2
            player.b3  = 0 if player.b3  is None else player.b3
            player.b4  = 0 if player.b4  is None else player.b4
            player.b5  = 0 if player.b5  is None else player.b5
            player.b6  = 0 if player.b6  is None else player.b6
            player.b7  = 0 if player.b7  is None else player.b7
            player.b8  = 0 if player.b8  is None else player.b8
            player.b9  = 0 if player.b9  is None else player.b9
            player.b10 = 0 if player.b10 is None else player.b10
            player.b11 = 0 if player.b11 is None else player.b11
            player.b12 = 0 if player.b12 is None else player.b12

       solutions = [53+64, 78+95, 23+34, 13+66, 24+78, 95+67, 58+37, 67+84, 53+45, 78+76, 26+39, 42+57]
       answers = [player.b1, player.b2, player.b3, player.b4,
                 player.b5, player.b6, player.b7, player.b8,
                 player.b9, player.b10, player.b11, player.b12]
       player.num_correct = sum(a == s for a, s in zip(answers, solutions))
       player.effort = player.num_correct*25
      
       player.ball = draw_ball()
       player.multiplier = get_multiplier(player.participant.chosen_type, player.ball)
       if player.multiplier == 1 : 
            player.multiplier_display = "1"
       else :
            player.multiplier_display = "1/3"
        
       player.points = int(round(player.effort * player.multiplier))
       player.payoff = player.points * cu(2.50/300)




      
class Result2(Page):
   form_model = 'player'
   def is_displayed(player):
       return player.round_number == 1
   @staticmethod
   def vars_for_template(self):
     participant = self.participant
     return dict(effort=self.effort, ball = self.ball, playerType=self.participant.chosen_type, multiplier = self.multiplier_display, points= self.points, payoff = self.payoff)





class Choice(Page):
   form_model = 'player'
   form_fields = ['choice']
   def is_displayed(player):
       return player.round_number == 1
   @staticmethod
   def vars_for_template(player):
       payoff_1 = player.participant.payoff1
       payoff_2 = player.payoff
       return dict(payoff_r1=payoff_1, payoff_r2=payoff_2)
   
   @staticmethod
   def before_next_page(player, timeout_happened):
       player.participant.vars['choice'] = player.choice
       player.participant.vars['payoff2'] = player.payoff




page_sequence = [Choice]
#Round2,Result2, 

