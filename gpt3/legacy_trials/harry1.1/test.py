gen_text = """I choose the right vase. After this,
"The flowers fall apart." is less likely to happen.
"The flowers are wet." is equally likely to happen.

I use a clear elastic hair tie to gather flowers together. After this,
"The flowers fall apart." is less likely to happen.
"The flowers are wet." is equally likely to happen.

I pour fresh, cool water in your vase. After this,
"The flowers fall apart." is equally likely to happen.
"The flowers are wet." is more likely to happen.

I add a couple of drops of bleach to the water. After this,
"The flowers fall apart." is equally likely to happen.
"The flowers are wet." is less likely to happen.

I organize your flowers and trim off leaves. After this,
"The flowers fall apart." is less likely to happen.
"The flowers are wet." is equally likely to happen.

I cut the flower stems with a sharp knife or garden clippers. After this,
"The flowers fall apart." is less likely to happen.
"The flowers are wet." is equally likely to happen.

I insert the flowers into the vase. After this,
"The flowers fall apart." is more likely to happen.
"The flowers are wet." is equally likely to happen.
"""

step_changes = []
current_step_changes = []
initial = True
for line in gen_text.split('\n'):
    line = line.strip()
    if line.startswith('I '):
        if not initial:
            step_changes.append(current_step_changes) 
            current_step_changes = []
        initial = False
    elif line.startswith('"I '):
        print(line)
        if 'is less likely to happen' in line:
            change = "less"
        elif 'is more likely to happen' in line:
            change = "more"
        elif 'is equally likely to happen' in line:
            continue
        else:
            print(line)
            raise ValueError()
        current_step_changes.append((line.split('"')[1], change))
    #elif not line:
    #    break
step_changes.append(current_step_changes) 
print(step_changes)