
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'type_effort_1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    checkbox = models.BooleanField()
    prolific = models.StringField(label="Prolific ID")
    chosen_type = models.StringField(choices=[['A', 'A'], ['B', 'B']],blank=False,label="Please Select your type", widget=widgets.RadioSelectHorizontal)
    
    task1 = models.IntegerField(blank=False,choices=[[1, 'Considerate'], [2, 'Playful'],[3, 'Obnoxious'],[4, 'Motivated']], widget=widgets.RadioSelect, 
                                label = "<p>Jake is Cassie's older brother. One day they are walking home from school when a cold front rolls in and the temperature drops 20 degrees. Jake is dressed more appropriately for the weather than Cassie. He takes off his hooded sweatshirt and offers it to her. She gratefully accepts. Jake is now colder, but he is happier.</p>")

    task2 = models.IntegerField(blank=False,choices=[[1, 'Entertain'], [2, 'Persuade'],[3, 'Inform']], widget=widgets.RadioSelect, 
                                label = "<p>A story about a family trying to stick together and survive through the Great Depression in the Midwest in the 1930s.</p> What is the author's purpose?")

    task3 = models.IntegerField(blank=False,choices=[[1, 'adjusted'], [2, 'boldly'],[3, 'curved'],[4, 'brim']], widget=widgets.RadioSelect, 
                                label = "<p>Captain Pete boldly adjusted the curved brim of his tricorn hat.</p> What is the verb in this sentence?")
    
    task4 = models.IntegerField(blank=False,choices=[[1, 'Person Versus Person'], [2, 'Person Versus Self'],[3, 'Person Versus Society'],[4, 'Person Versus Nature'],[5, 'Person Versus Supernatural'],[6, 'Person Versus Technology']], widget=widgets.RadioSelect, 
                                label = "<p>After breaking his mother's favorite vase, Casey struggles to decide whether he should tell her the truth and face the consequences or hide his mistake and blame the family dog.</p> Which type of conflict is described above?")
    
    task5 = models.IntegerField(blank=False,choices=[[1, 'The speaker is appreciating the park.'], [2, 'The speaker is complaining about work.'],[3, 'The speaker is enjoying a concert.'],[4, 'The speaker is rushing through traffic.']], label = "<p>What is this poem about?</p>", widget=widgets.RadioSelect)
    
    a1 = models.IntegerField(blank=False, label ="83+51=")
    a2 = models.IntegerField(blank=False, label ="49+62=")
    a3 = models.IntegerField(blank=False, label ="73+87=")
    a4 = models.IntegerField(blank=False, label ="92+25=")
    a5 = models.IntegerField(blank=False, label ="52+23=")
    a6 = models.IntegerField(blank=False, label ="68+39=")
    a7 = models.IntegerField(blank=False, label ="97+61=")
    a8 = models.IntegerField(blank=False, label ="46+14=")
    a9 = models.IntegerField(blank=False, label ="35+68=")
    a10 = models.IntegerField(blank=False, label ="69+87=")
    a11 = models.IntegerField(blank=False, label ="23+47=")
    a12 = models.IntegerField(blank=False, label ="14+68=")
 
    num_correct = models.IntegerField()
    
    ball = models.StringField()  
    multiplier = models.FloatField()
    multiplier_display = models.StringField()

    effort = models.IntegerField()
    points = models.IntegerField()
    


def draw_ball():
    import random 
    return random.choice(["black", "white"])
    
def get_multiplier(chosen_type, ball):
    if ball == "black":
        return 1 if chosen_type == "A" else 1/3
    else:  # white
        return 1/3 if chosen_type == "A" else 1

class Consent(Page):
    form_model = "player"
    form_fields = ["checkbox", 'prolific']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Introduction(Page):
    form_model = "player"
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class ChooseType(Page):
    form_model = 'player'
    form_fields = ['chosen_type']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

        
class Task1(Page):
    form_model = 'player'
    form_fields = ['task1']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Task2(Page):
    form_model = 'player'
    form_fields = ['task2']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Task3(Page):
    form_model = 'player'
    form_fields = ['task3']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Task4(Page):
    form_model = 'player'
    form_fields = ['task4']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
        
class Task5(Page):
    form_model = 'player'
    form_fields = ['task5']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1        
        
class TypeEarned(Page):
    form_model = 'player'
    def is_displayed(player):
        return player.round_number == 1
    def vars_for_template(self):
      participant = self.participant
      return dict(playerType=self.chosen_type)


class Round1(Page):
    timeout_seconds = 180
    form_model = 'player'
    form_fields = ['a1', 'a2', 'a3', 'a4',
                  'a5', 'a6', 'a7', 'a8',
                  'a9', 'a10', 'a11', 'a12']
    
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def before_next_page(player, timeout_happened):
        solutions = [83+51,49+62, 73+87,92+25, 52+23, 68+39, 97+61,46+14, 35+68,69+87 , 23+47,14+68]
        answers = [player.a1, player.a2, player.a3, player.a4,
                  player.a5, player.a6, player.a7, player.a8,
                  player.a9, player.a10, player.a11, player.a12]
        player.num_correct = sum(a == s for a, s in zip(answers, solutions))
        player.effort = player.num_correct*25
        
        player.ball = draw_ball()
        player.multiplier = get_multiplier(player.chosen_type, player.ball)
        if player.multiplier == 1 : 
            player.multiplier_display = "1"
        else : 
            player.multiplier_display = "1/3"

        player.points = int(round(player.effort * player.multiplier))
        player.payoff = player.points * cu(2.50/300)


class Result1(Page):
    form_model = 'player'
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(self):
      participant = self.participant
      return dict(effort=self.effort, ball = self.ball, playerType=self.chosen_type, 
                  multiplier = self.multiplier_display, points= self.points, payoff = self.payoff)
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.vars['chosen_type'] = player.chosen_type
        player.participant.vars['payoff1'] = player.payoff

page_sequence = [Introduction,ChooseType,#Task1,Task2,Task3,Task4, Task5,TypeEarned,Round1,Result1]

#Consent,
