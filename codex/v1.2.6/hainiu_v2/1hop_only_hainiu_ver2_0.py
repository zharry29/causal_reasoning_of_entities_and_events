# python code
class ComputeLikelihood():
    """
    class definiting the likelihood of an event at a step
    """

    def __init__(self, cur_event, cur_step):
        self.cur_event = cur_event,
        self.cur_step = cur_step    

    def compute_likelihood(self):
        """
        function to compute the change of likelihood given an event and a step
        Returns:
            str: the change of likelihood, possible options: 'more', 'less', and 'equal'
        """
        return reasoning_engine(self.cur_event, self.cur_step)
    
    @property
    def event_likelihood(self):
        likelihood = self.reason_likelihood(self.cur_event, self.cur_step)
        if likelihood in ['more', 'less', 'equal']:
            return likelihood


class Wash_Hands():
    """
    function to predict the change of likelihood of events at a given step
    event0 (str): I can safely touch a light switch. 
    event1 (str): Water streaming sound can be heard.
    steps (list): list of steps in a procedure
    """

    def __init__(self, event0, event1):
        self.event0 = event0
        self.event1 = event1
        self.steps = [
            "Turn on the tap water.",
            "Put hands under running water.",
            "Apply soap and rub hands.",
            "Turn off the tap water.",
            "Dry my hands using a towel."
        ]
        
    def step_0(self):
        # self.step[0] = "Turn on the tap water."
        cur_step = self.steps[0]  
        
        # event0 = "I can safely touch a light switch."
        event0_state = ComputeLikelihood(self.event0, cur_step)
        event0_state.likelihood = 'equal'
        
        # event1 = "Water streaming sound can be heard."
        event1_state = ComputeLikelihood(self.event1, cur_step)
        event1_state.likelihood = 'more'

    def step_1(self):
        # self.step[1] = "Put hands under running water."
        cur_step = self.steps[1]
        
        # event0 = "I can safely touch a light switch."
        event0_state = ComputeLikelihood(self.event0, cur_step)
        event0_state.likelihood = 'less'
        
        # event1 = "Water streaming sound can be heard."
        event1_state = ComputeLikelihood(self.event1, cur_step)
        event1_state.likelihood = 'equal'

    def step_2(self):
        # self.step[2] = "Apply soap and rub hands." 
        cur_step = self.steps[2]
        
        # event0 = "I can safely touch a light switch."
        event0_state = ComputeLikelihood(self.event0, cur_step)
        event0_state.likelihood = 'equal'
        
        # event1 = "Water streaming sound can be heard."
        event1_state = ComputeLikelihood(self.event1, cur_step)
        event1_state.likelihood = 'equal'

    def step_3(self):
        # self.steps[3] = "Turn off the tap water." 
        cur_step = self.steps[3]
        
        # event0 = "I can safely touch a light switch."
        event0_state = ComputeLikelihood(self.event0, cur_step)
        event0_state.likelihood = 'equal'
        
        # event1 = "Water streaming sound can be heard."
        event1_state = ComputeLikelihood(self.event1, cur_step)
        event1_state.likelihood = 'less'

    def step_4(self):
        # self.steps[4] = "Dry my hands using a towel." 
        cur_step = self.steps[4]
        
        # event0 = "I can safely touch a light switch."
        event0_state = ComputeLikelihood(self.event0, cur_step)
        event0_state.likelihood = 'equal'
        
        # event1 = "Water streaming sound can be heard."
        event1_state = ComputeLikelihood(self.event1, cur_step)
        event1_state.likelihood = 'more'

        
class Refuel_Car():
    """
    function to predict the change of likelihood of events at a given step
    event0 (str): I pull the handle of the fuel nozzle and fuel comes out.
    steps (list): list of steps in a procedure
    """
    def __init__(self, event0):
        self.event0 = event0 
        self.steps = [
            "Go to a gas station.",
            "Insert credit card into the gas pump and pay.",
            "Remove nozzle and select fuel grade.",
            "Insert the nozzle into the car's gas tank.",
            "Pull the handle until the gas meter starts running.",
            "When done, put the nozzle back."
        ]
    def step_0(self):
        # self.steps[0] = "Go to a gas station." 
        cur_step = self.steps[0]

        # event0 = "I pull the handle of the fuel nozzle and fuel comes out." 
        event0_state = ComputeLikelihood(self.event0, cur_step)
        event0_state.likelihood = 'equal'

    def step_1(self):
        # self.steps[1] = "Insert credit card into the gas pump and pay." 
        cur_step = self.steps[1]

        # event0 = "I pull the handle of the fuel nozzle and fuel comes out." 
        event0_state = ComputeLikelihood(self.event0, cur_step)
        event0_state.likelihood = 'equal'
        
    def step_2(self):
        # self.steps[2] = "Remove nozzle and select fuel grade."
        cur_step = self.steps[2]

        # event0 = "I pull the handle of the fuel nozzle and fuel comes out." 
        event0_state = ComputeLikelihood(self.event0, cur_step)
        event0_state.likelihood = 'more'
        
    def step_3(self):
        # self.steps[3] = "Insert the nozzle into the car's gas tank." 
        cur_step = self.steps[3]

        # event0 = "I pull the handle of the fuel nozzle and fuel comes out." 
        event0_state = ComputeLikelihood(self.event0, cur_step)
        event0_state.likelihood = 'equal'
        
    def step_4(self):
        # self.steps[4] = "Pull the handle until the gas meter starts running."
        cur_step = self.steps[4]

        # event0 = "I pull the handle of the fuel nozzle and fuel comes out." 
        event0_state = ComputeLikelihood(self.event0, cur_step)
        event0_state.likelihood = 'equal'
        
    def step_5(self):
        # self.steps[5] = "When done, put the nozzle back.
        cur_step = self.steps[5]
        
        # event0 = "I pull the handle of the fuel nozzle and fuel comes out." 
        event0_state = ComputeLikelihood(self.event0, cur_step)
        event0_state.likelihood = 'less'
    
