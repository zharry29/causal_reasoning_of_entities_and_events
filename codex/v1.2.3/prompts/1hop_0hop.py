class Wash_Hands:
  # Init
  # Turn on the tap water.
  # Put hands under running water.
  # Apply soap and rub hands.
  # Turn off the tap water.
  # Dry my hands using a towel.
  def __init__(self, event0, event1):
    self.water = Water()
    self.hands = Hands()
    self.event0 = event0 # I can safely touch a light switch.
    self.event1 = event1 # Water streaming sound can be heard.
  def turn_on_tap_water(self):
    self.water.on = True
    self.event1 = self.water.on # Water streaming sound can be heard.
  def put_hands_under_running_water(self):
    self.hands.wet = True
    self.event0 = not self.hands.wet # I can safely touch a light switch.
  def apply_soap_and_rub_hands(self):
    pass
  def turn_off_tap_water(self):
    self.water.on = False
    self.event1 = self.water.on # Water streaming sound can be heard.
  def dry_hands_with_towel(self):
    self.hands.wet = False
    self.event0 = not self.hands.wet # I can safely touch a light switch.

class Change_Battery_of_TV_Remote_Control:
  # Init
  # Pop open the battery cover.
  # Take out the old batteries.
  # Put in the new batteries.
  # Close the battery cover.
  def __init__(self, event0, event1):
    self.remote = Remote()
    self.battery_cover = Battery_Cover()
    self.event0 = event0 # I can see inside the battery compartment
    self.event1 = event1 # The remote can turn on a TV.
  def pop_open_battery_cover(self):
    self.battery_cover.removed = True
    self.event0 = self.battery_cover.removed # I can see inside the battery compartment
  def take_out_old_batteries(self):
    self.remote.has_battery = False
    self.event1 = self.remote.has_battery # The remote can turn on a TV.
  def put_in_new_batteries(self):
    self.remote.has_battery = True
    self.event1 = self.remote.has_battery # The remote can turn on a TV.
  def close_battery_cover(self):
    self.battery_cover.removed = False
    self.event0 = self.battery_cover.removed # I can see inside the battery compartment

class Cook_Salmon_In_Oven:
  # Init
  # Choose a good cut of salmon
  # Pat dry the salmon.
  # Brush the salmon with sauce.
  # Put the salmon on the foil.
  # Put the salmon in an oven preheated to 350 degrees for 20 minutes.
  # Serve the salmon.
  def __init__(self, event0, event1):
    self.salmon = Salmon()
    self.event0 = event0 # The salmon can be easliy flaked by a fork.
    self.event1 = event1 # I touch the salmon and my fingers stay dry.
  def choose_good_cut_of_salmon(self):
    pass
  def pat_dry_salmon(self):
    self.salmon.wet = False
    self.event1 = not self.salmon.wet # I touch the salmon and my fingers stay dry.
  def brush_salmon_with_sauce(self):
    self.salmon.wet = True
    self.event1 = not self.salmon.wet # I touch the salmon and my fingers stay dry.
  def cover_salmon_with_foil(self):
    pass
  def put_salmon_in_oven_preheated_to_350_degrees_for_20_minutes(self):
    self.salmon.cooked = True
    self.salmon.wet = False
    self.event0 = self.salmon.cooked # The salmon can be easliy flaked by a fork.
    self.event1 = not self.salmon.wet # I touch the salmon and my fingers stay dry.
  def serve_salmon(self):
    pass

