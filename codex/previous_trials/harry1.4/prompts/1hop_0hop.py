class Wash_Hands:
  # Init
  # Turn on the tap water.
  # Put hands under running water.
  # Apply soap and rub hands.
  # Turn off the tap water.
  # Dry my hands using a towel.
  def __init__(self):
    self.event0.name = "I can safely touch a light switch."
    self.event0.subevent.name = "My hands are wet."
    self.event1 = "Water streaming sound can be heard."
    self.event1.subevent.name = "The water is on."
  def turn_on_tap_water(self):
    self.event0.change = "equally likely"
    self.event1.subevent.change = "more likely"
    self.event1.change = "more likely"
  def put_hands_under_running_water(self):
    self.event0.subevent.change = "more likely"
    self.event0.change = "less likely"
    self.event1.change = "equally likely"
  def apply_soap_and_rub_hands(self):
    self.event0.change = "equally likely"
    self.event1.change = "equally likely"
  def turn_off_tap_water(self):
    self.event0.change = "equally likely"
    self.event1.subevent.name.change = "less likely"
    self.event1.change = "less likely"
  def dry_hands_with_towel(self):
    self.event0.subevent.change = "less likely"
    self.event0.change = "more likely"
    self.event1.change = "equally likely"

class Change_Battery_of_TV_Remote_Control:
  # Init
  # Pop open the battery cover.
  # Take out the old batteries.
  # Put in the new batteries.
  # Close the battery cover.
  def __init__(self):
    self.event0.name = "I can see inside the battery compartment."
    self.event0.subevent.name = "The battery cover is removed."
    self.event1.name = "The remote can turn on a TV."
    self.event1.subevent.name = "The remote has battery."
  def pop_open_battery_cover(self):
    self.event0.subevent.change = "more likely"
    self.event0.change = "more likely" # I can see inside the battery compartment
    self.event1.change = "equally likely" # The remote can turn on a TV.
  def take_out_old_batteries(self):
    self.event0.change = "equally likely" # I can see inside the battery compartment
    self.event1.subevent.change = "less likely"
    self.event1.change = "less likely" # The remote can turn on a TV.
  def put_in_new_batteries(self):
    self.event0.change = "equally likely" # I can see inside the battery compartment
    self.event1.subevent.change = "more likely"
    self.event1.change = "more likely" # The remote can turn on a TV.
  def close_battery_cover(self):
    self.event0.subevent.change = "less likely"
    self.event0.change = "less likely" # I can see inside the battery compartment
    self.event1.change = "equally likely" # The remote can turn on a TV.

class Cook_Salmon_In_Oven:
  # Init
  # Pat dry the salmon.
  # Brush the salmon with sauce.
  # Put the salmon on the foil.
  # Put the salmon in an oven preheated to 350 degrees for 20 minutes.
  # Serve the salmon.
  def __init__(self):
    self.event0.name = "The salmon can be easliy flaked by a fork."
    self.event0.subevent.name = "The salmon is cooked."
    self.event1.name = "I touch the salmon and my fingers get wet."
    self.event1.subevent.name = "The salmon is wet."
  def pat_dry_salmon(self):
    self.event0.change = "equally likely" # The salmon can be easliy flaked by a fork.
    self.event1.subevent.change = "less likely"
    self.event1.change = "less likely" # I touch the salmon and my fingers get wet.
  def brush_salmon_with_sauce(self):
    self.event0.change = "equally likely" # The salmon can be easliy flaked by a fork.
    self.event1.subevent.change = "more likely"
    self.event1.change = "more likely" # I touch the salmon and my fingers get wet.
  def cover_salmon_with_foil(self):
    self.event0.change = "equally likely" # The salmon can be easliy flaked by a fork.
    self.event1.change = "equally likely" # I touch the salmon and my fingers get wet.
  def put_salmon_in_oven_preheated_to_350_degrees_for_20_minutes(self):
    self.event0.subevent.change = "more likely"
    self.event0.change = "more likely" # The salmon can be easliy flaked by a fork.
    self.event1.subevent.change = "less likely"
    self.event1.change = "less likely" # I touch the salmon and my fingers get wet.
  def serve_salmon(self):
    self.event0.change = "equally likely" # The salmon can be easliy flaked by a fork.
    self.event1.change = "equally likely" # I touch the salmon and my fingers get wet.

