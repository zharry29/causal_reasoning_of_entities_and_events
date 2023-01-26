def build_prompt(goal, steps, event):
  prompt = ""
  prompt += f'"{goal.lower().capitalize()}" involves the followings steps:\n'
  for i, step in enumerate(steps):
    prompt += f"{i+1}: {step}\n"
  prompt += f"\nFor every step, find out whether {event.lower()}. Answer as (A) very likely (B) likely (C) not very likely (D) unlikely.\n\nStep 1: ("
  return prompt