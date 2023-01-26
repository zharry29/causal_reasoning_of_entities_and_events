class Wash_Hands:
  # Init
  # Turn on the tap water.
  # Put hands under running water.
  # Apply soap and rub hands.
  # Turn off the tap water.
  # Dry my hands using a towel.
  def init(self, event0, event1):
    self.event0 = event0 # I can safely touch a light switch.
    self.event1 = event1 # Water streaming sound can be heard.
    self.water = Water()
    self.hands = Hands()
  def turn_on_tap_water(self):
    self.water.on = True
    self.event1 = True # Water streaming sound can be heard.
  def put_hands_under_running_water(self):
    self.hands.wet = True
    self.event0 = False # I can safely touch a light switch.
  def apply_soap_and_rub_hands(self):
    pass
  def turn_off_tap_water(self):
    self.water.on = False
    self.event1 = False # Water streaming sound can be heard.
  def dry_hands_with_towel(self):
    self.hands.wet = False
    self.event0 = True # I can safely touch a light switch.

class Refuel_Car:
  # Init
  # Go to a gas station.
  # Insert credit card into the gas pump and pay.
  # Remove nozzle and select fuel grade.
  # Insert the nozzle into the car's gas tank.
  # Pull the handle until the gas meter starts running.
  # When done, put the nozzle back.
  def init(self, event0):
    self.event0 = event0 # I pull the handle of the fuel nozzle and fuel comes out.
    self.nozzle = Nozzle()
  def go_to_gas_station(self):
    pass
  def insert_credit_card_into_gas_pump_and_pay(self):
    pass
  def remove_nozzle_and_select_fuel_grade(self):
    self.nozzle.locked = False
    self.event0 = True # I pull the handle of the fuel nozzle and fuel comes out.
  def insert_the_nozzle_into_car_gas_tank(self):
    pass
  def pull_handle_until_gas_meter_starts_running(self):
    pass
  def when_done_put_nozzle_back(self):
    self.nozzle.locked = True
    self.event0 = False # I pull the handle of the fuel nozzle and fuel comes out.

class Change_Battery_of_TV_Remote_Control:
  # Init
  # Pop open the battery cover.
  # Take out the old batteries.
  # Put in the new batteries.
  # Close the battery cover.
  def init(self, event0, event1):
    self.event0 = event0 # I can see inside the battery compartment
    self.event1 = event1 # The remote can turn on a TV.
    self.remote = Remote()
    self.battery_cover = Battery_Cover()
  def pop_open_battery_cover(self):
    self.battery_cover.removed = True
    self.event0 = True # I can see inside the battery compartment
  def take_out_old_batteries(self):
    self.remote.has_battery = False
    self.event1 = False # The remote can turn on a TV.
  def put_in_new_batteries(self):
    self.remote.has_battery = True
    self.event1 = True # The remote can turn on a TV.
  def close_battery_cover(self):
    self.battery_cover.removed = False
    self.event0 = False # I can see inside the battery compartment

class Cook_Salmon_In_Oven:
  # Init
  # Pat dry the salmon.
  # Brush the salmon with sauce.
  # Cover the salmon with foil.
  # Put the salmon in an oven preheated to 350 degrees for 20 minutes.
  # Serve the salmon.
  def init(self, event0, event1):
    self.event0 = event0 # The salmon can be easliy flaked by a fork.
    self.event1 = event1 # I touch the salmon and my fingers get wet.
    self.salmon = Salmon()
  def pat_dry_salmon(self):
    self.salmon.wet = False
    self.event1 = False # I touch the salmon and my fingers get wet.
  def brush_salmon_with_sauce(self):
    self.salmon.wet = True
    self.event1 = True # I touch the salmon and my fingers get wet.
  def cover_salmon_with_foil(self):
    pass
  def put_salmon_in_oven_preheated_to_350_degrees_for_20_minutes(self):
    self.salmon.cooked = True
    self.event0 = True # The salmon can be easliy flaked by a fork.
    self.salmon.wet = False
    self.event1 = False # I touch the salmon and my fingers get wet.
  def serve_salmon(self):
    pass

