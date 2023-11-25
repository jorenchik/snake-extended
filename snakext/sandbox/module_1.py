from snakext.sandbox import module_2
from snakext.sandbox import test_state

state = test_state.State.instance()
print(f"Module 2 initial state from ref.:{module_2.foo()}")

state.data[0] = 999
print(f"Module 1 ending state from ref.:{state.data}")

print(f"Module 2 ending state from ref.:{module_2.foo()}")
