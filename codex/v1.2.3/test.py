gen_code = """  def turn_on_computer(self):
    self.computer.on = True
  def turn_on_monitor(self):
    self.monitor.on = True
  def select_correct_source_of_monitor(self):
    self.monitor.source = self.HDMI_cable
    self.event2 = self.monitor.source == self.HDMI_cable # The monitor projects images from the computer."""

step_changes = []
current_step_changes = []
current_variables = []
initial = True
for line in gen_code.split('\n'):
    line = line.strip()
    if line.startswith('def '):
        if not initial:
            step_changes.append(current_step_changes) 
            current_step_changes = []
        initial = False
    elif line.startswith('self.') and not line.startswith('self.event'):
        line = line.replace('.','_')
        variable = line.split(' = ')[0]
        try:
            variable_value = eval(line.split(' = ')[1])
        except (NameError, IndexError) as e:
            print(e)
            continue
        if isinstance(variable_value, str):
            variable_value = '"' + variable_value + '"'
        elif isinstance(variable_value, bool):
            variable_value = str(variable_value)
        current_variables.append((variable,variable_value))
        #current_step_changes.append((line.split('.')[1], line.split('.')[2].split(' = ')[0], line.split(' = ')[1].strip('"')))
    elif line.startswith('self.event'):
        line = line.replace('.','_').split('#')[0]
        print(current_variables)
        for variable, variable_value in current_variables:
            line = line.replace(variable, variable_value)
        change = "more likely" if eval(line.split(' = ')[1]) else "less likely"
        current_step_changes.append((line[5:11], change))
    elif not line:
        break
step_changes.append(current_step_changes) 
print(step_changes)