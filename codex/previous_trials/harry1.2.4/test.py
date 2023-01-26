gen_code = """    event0.change = "less likely" # Dropping the glassware makes the floor wet.
    event1.change = "more likely" # The glassware looks like new.
  def fill_bottom_of_dish_with_warm_water(self):
    event0.change = "more likely" # Dropping the glassware makes the floor wet.
    event1.change = "equally likely" # The glassware looks like new.
  def pour_pea-sized_amount_of_dish_soap_into_water(self):
    event0.change = "equally likely" # Dropping the glassware makes the floor wet.
    event1.change = "equally likely" # The glassware looks like new.
  def place_1_dryer_sheet_into_glass_dish(self):
    event0.change = "equally likely" # Dropping the glassware makes the floor wet.
    event1.change = "equally likely" # The glassware looks like new.
  def leave_sheet_in_glassware_for_at_least_10_minutes(self):
    event0.change = "equally likely" # Dropping the glassware makes the floor wet.
    event1.change = "equally likely" # The glassware looks like new.
  def wipe_off_baked_on_grease_with_sponge_and_dry(self):
    event0.change = "less likely" # Dropping the glassware makes the floor wet.
    event1.change = "more likely" # The glassware looks like new."""

step_changes = []
current_step_changes = []
initial = True
for line in gen_code.split('\n'):
    line = line.strip()
    if line.startswith('def '):
        if not initial:
            step_changes.append(current_step_changes) 
            current_step_changes = []
        initial = False
    elif not line.startswith('event'):
        if ' = False' in line:
            change = "less likely"
        elif ' = True' in line:
            change = "more likely"
        else:
            continue
        current_step_changes.append((line.split('.')[1], line.split('.')[2].split(' = ')[0], line.split(' = ')[1].strip('"')))
    elif line.startswith('event'):
        if '.change = "less likely"' in line:
            change = "less likely"
        elif '.change = "more likely"' in line:
            change = "more likely"
        elif '.change = "equally likely"' in line:
            continue
        else:
            print(line)
            raise ValueError()
        current_step_changes.append((line[0:6], change))
    elif not line:
        break
step_changes.append(current_step_changes) 
print(step_changes)