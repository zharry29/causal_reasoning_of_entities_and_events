# Description
- The best prompt we have found until 10/10/2022, before EACL submission
- A procedure is represented as a Python class
- For entity_and_event, the entity is represented as `ENTITY.ATTRIBUTE = STATE`, namely a hard representation

# Developer's changelog
- This is aka `harry1.2`
- The entities are NOT given to the models in init, aka `hainiu1.5`
- The `init` function is changed to `__init__`
- To minimize computation cost, `at_once` is default unless gold entity is provided