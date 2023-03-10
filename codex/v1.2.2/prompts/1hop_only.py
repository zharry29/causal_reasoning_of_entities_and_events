class Wash_Hands:
  # Init
  # Turn on the tap water.
  # Put hands under running water.
  # Apply soap and rub hands.
  # Turn off the tap water.
  # Dry my hands using a towel.
  def __init__(self, event0, event1):
    self.event0 = event0 # I can safely touch a light switch.
    self.event1 = event1 # Water streaming sound can be heard.
  def turn_on_tap_water(self):
    self.event0.change = "equally likely"
    self.event1.change = "more likely"
  def put_hands_under_running_water(self):
    self.event0.change = "less likely"
    self.event1.change = "equally likely"
  def apply_soap_and_rub_hands(self):
    self.event0.change = "equally likely"
    self.event1.change = "equally likely"
  def turn_off_tap_water(self):
    self.event0.change = "equally likely"
    self.event1.change = "less likely"
  def dry_hands_with_towel(self):
    self.event0.change = "more likely"
    self.event1.change = "equally likely"
    
class Change_Battery_of_TV_Remote_Control:
  # Init
  # Pop open the battery cover.
  # Take out the old batteries.
  # Put in the new batteries.
  # Close the battery cover.
  def __init__(self, event0, event1):
    self.event0 = event0 # I can see inside the battery compartment
    self.event1 = event1 # The remote can turn on a TV.
  def pop_open_battery_cover(self):
    self.event0.change = "more likely"
    self.event1.change = "equally likely"
  def take_out_old_batteries(self):
    self.event0.change = "equally likely"
    self.event1.change = "less likely"
  def put_in_new_batteries(self):
    self.event0.change = "equally likely"
    self.event1.change = "more likely"
  def close_battery_cover(self):
    self.event0.change = "less likely"
    self.event1.change = "equally likely"

class Cook_Salmon_In_Oven:
  # Init
  # Pat dry the salmon.
  # Brush the salmon with sauce.
  # Put the salmon on foil.
  # Put the salmon in an oven preheated to 350 degrees for 20 minutes.
  # Serve the salmon.
  def __init__(self, event0, event1):
    self.event0 = event0 # The salmon can be easliy flaked by a fork.
    self.event1 = event1 # I touch the salmon and my fingers get wet.
  def pat_dry_salmon(self):
    self.event0.change = "equally likely"
    self.event1.change = "less likely"
  def brush_salmon_with_sauce(self):
    self.event0.change = "equally likely"
    self.event1.change = "more likely"
  def put_salmon_on_foil(self):
    self.event0.change = "equally likely"
    self.event1.change = "equally likely"
  def put_salmon_in_oven_preheated_to_350_degrees_for_20_minutes(self):
    self.event0.change = "more likely"
    self.event1.change = "less likely"
  def serve_salmon(self):
    self.event0.change = "equally likely"
    self.event1.change = "equally likely"

