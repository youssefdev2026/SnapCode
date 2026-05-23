from engine import Transpiler

test_code = """
out hello world
fn calculate x y
    loop 10
        out doing work
    return x + y
"""

engine = Transpiler()
print("Original Shorthand:")
print("-------------------")
print(test_code.strip())
print("\nTranspiled Python Code:")
print("-----------------------")
print(engine.transpile_text(test_code, "python"))
