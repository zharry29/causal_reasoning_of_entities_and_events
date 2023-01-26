# python code
class Wash_Hands():
    def __init__(self):
        self.hands = None
        self.water = None
        self.state = None    
    
    def step_0(self):
        content = "I turn on the tap water."
        self.water = "water is on"
        self.hands = None
        # likelihood that I can safely touch a light switch
        self.state.likelihood = "unrelated"
    
    def step_1(self):
        content = "I put hands under running water."
        self.water = "water is on"
        self.hands = "hands are wet"
        # likelihood that I can safely touch a light switch
        self.state.likelihood = "unlikely"
    
    def step_2(self):
        content = "I apply soap and rub hands."
        self.water = "water is on"
        self.hands = "hands are wet"
        # likelihood that I can safely touch a light swith
        self.state.likelihood = "unlikely"
    
    def step_3(self):
        content = "I turn off the tap water. After this, the water is not on." 
        self.water = 'water is not on'
        self.hands = "hands are wet"
        # likelihood that I can safely touch a light switch
        self.state.likelihood = "unlikely"
    
    def step_4(self):
        content = "I dry my hands using a towel."
        self.water = 'water is not on'
        self.hands = "hands are not wet"
        # likelihood that I can safely touch a light switch
        self.state.likelihood = "likely"

        
class Cook_Salmon_In_Oven:
    def __init__(self):
        self.salmon = None
        self.state = None
    
    def step_0(self):
        content = 'I pat dry the salmon.'
        self.salmon = "salmon is dry"
        # likelihood that the salmon can be easily flaked by a fork
        self.state.likelihood = "unlikely"
    
    def step_1(self):
        content = "I brush the salmon with sauce."
        self.salmon = "salmon is wet"
        # likelihood that the salmon can be easily flaked by a fork
        self.state.likelihood = "unlikely"
    
    def step_2(self):
        content = "I put the salmon on the foil."
        self.salmon = "salmon is wet"
        # likelihood that the salmon can be easily flaked by a fork
        self.state.likelihood = "unlikely"
    
    def step_3(self):
        content = "I put the salmon in an oven preheated to 350 degrees for 20 minutes."
        self.salmon = "salmon is not wet and salmon is cooked"
        # likelihood that the salmon can be easily flaked by a fork
        self.state.likelihood = "likely"

    def step_4(self):
        content = "I serve the salmon."
        self.salmon = "salmon is not wet and salmon is cooked"
        # likelihood that the salmon can be easily flaked by a fork
        self.state.likelihood = "likely"


