def wash_hands(event0, event1):
  # Init
  # Turn on the tap water.
  # Put hands under running water.
  # Apply soap and rub hands.
  # Turn off the tap water.
  # Dry my hands using a towel.
  event0 = event0 # I can safely touch a light switch.
  event1 = event1 # Water streaming sound can be heard.
  water = Water()
  hands = Hands()
  def turn_on_tap_water():
    water.on = True
    event0.change = "equally likely" # I can safely touch a light switch.
    event1.change = "more likely" # Water streaming sound can be heard.
  def put_hands_under_running_water():
    hands.dry = False
    event0.change = "less likely" # I can safely touch a light switch.
    event1.change = "equally likely" # Water streaming sound can be heard.
  def apply_soap_and_rub_hands():
    event0.change = "equally likely" # I can safely touch a light switch.
    event1.change = "equally likely" # Water streaming sound can be heard.
  def turn_off_tap_water():
    water.on = False
    event0.change = "equally likely" # I can safely touch a light switch.
    event1.change = "less likely" # Water streaming sound can be heard.
  def dry_hands_with_towel():
    hands.dry = True
    event0.change = "more likely" # I can safely touch a light switch.
    event1.change = "equally likely" # Water streaming sound can be heard.

def change_battery_of_tv_remote_control(event0, event1):
  # Init
  # Pop open the battery cover.
  # Take out the old batteries.
  # Put in the new batteries.
  # Close the battery cover.
  remote = Remote()
  battery_cover = Battery_Cover()
  event0 = event0 # I can see inside the battery compartment
  event1 = event1 # The remote can turn on a TV.
  def pop_open_battery_cover():
    battery_cover.removed = True
    event0.change = "more likely" # I can see inside the battery compartment
    event1.change = "equally likely" # The remote can turn on a TV.
  def take_out_old_batteries():
    remote.has_battery = False
    event0.change = "equally likely" # I can see inside the battery compartment
    event1.change = "less likely" # The remote can turn on a TV.
  def put_in_new_batteries():
    remote.has_battery = True
    event0.change = "equally likely" # I can see inside the battery compartment
    event1.change = "more likely" # The remote can turn on a TV.
  def close_battery_cover():
    battery_cover.removed = False
    event0.change = "less likely" # I can see inside the battery compartment
    event1.change = "equally likely" # The remote can turn on a TV.

def cook_salmon_in_oven(event0, event1):
  # Init
  # Choose a good cut of salmon
  # Pat dry the salmon.
  # Brush the salmon with sauce.
  # Put the salmon on the foil.
  # Put the salmon in an oven preheated to 350 degrees for 20 minutes.
  # Serve the salmon.
  salmon = Salmon()
  event0 = event0 # The salmon can be easliy flaked by a fork.
  event1 = event1 # I touch the salmon and my fingers stay dry.
  def choose_good_cut_of_salmon():
    event0.change = "equally likely" # The salmon can be easliy flaked by a fork.
    event1.change = "equally likely" # I touch the salmon and my fingers stay dry.
  def pat_dry_salmon():
    salmon.wet = False
    event0.change = "equally likely" # The salmon can be easliy flaked by a fork.
    event1.change = "less likely" # I touch the salmon and my fingers stay dry.
  def brush_salmon_with_sauce():
    salmon.wet = True
    event0.change = "equally likely" # The salmon can be easliy flaked by a fork.
    event1.change = "more likely" # I touch the salmon and my fingers stay dry.
  def put_salmon_on_foil():
    event0.change = "equally likely" # The salmon can be easliy flaked by a fork.
    event1.change = "equally likely" # I touch the salmon and my fingers stay dry.
  def put_salmon_in_oven_preheated_to_350_degrees_for_20_minutes():
    salmon.wet = False
    salmon.cooked = True
    event0.change = "more likely" # The salmon can be easliy flaked by a fork.
    event1.change = "less likely" # I touch the salmon and my fingers stay dry.
  def serve_salmon():
    event0.change = "equally likely" # The salmon can be easliy flaked by a fork.
    event1.change = "equally likely" # I touch the salmon and my fingers stay dry.
