def wash_hands():
    steps = [
    "Init",
    "Turn on the tap water.",
    "Put hands under running water.",
    "Apply soap and rub hands.",
    "Turn off the tap water.",
    "Dry my hands using a towel.",
    ]
    
    event0 = "I can safely touch a light switch"
    event1 = "Water streaming sound can be heard."
    event0.precondition = ('hands', 'dry')
    event1.precondition = ('water', 'running')


def change_battery_of_tv_remote_control():
    steps = [
    "Init",
    "Pop open the battery cover.",
    "Take out the old batteries.",
    "Put in the new batteries.",
    "Close the battery cover.",
    ]

    event0 = "I can see inside the battery compartment"
    event1 = "The remote can turn on a TV"
    event0.precondition = ("battery cover", "open")
    event1.precondition = ("remote", "has battery")


def cook_salmon_in_oven():
    steps = [
    "Init",
    "Pat dry the salmon.",
    "Brush the salmon with sauce.",
    "Put the salmon on the foil.",
    "Put the salmon in an oven preheated to 350 degrees for 20 minutes.",
    "Serve the salmon.",
    ]
    
    event1 =  "I touch the salmon and my fingers get wet"
    event1.precondition = ("salmon surface", "wet")


