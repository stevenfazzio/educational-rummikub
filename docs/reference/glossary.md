# Programming Terms Glossary

This glossary explains programming terms you'll encounter in the Rummikub codebase. Terms are listed alphabetically with simple explanations and examples.

## A

### Argument
Information you give to a function when you call it.
```python
create_tile(5, 'red')  # 5 and 'red' are arguments
```

### Assert
A test that checks if something is true. Used in testing.
```python
self.assertEqual(2 + 2, 4)  # Asserts that 2+2 equals 4
```

### Attribute
A variable that belongs to an object.
```python
player.name  # 'name' is an attribute of player
```

## B

### Boolean
A value that's either True or False.
```python
has_melded = True
is_valid = False
```

### Bug
An error in code that makes it work incorrectly.

## C

### Class
A blueprint for creating objects. Like a cookie cutter.
```python
class Player:  # This is a class definition
    pass
```

### Comment
Text in code that explains things but doesn't run.
```python
# This is a comment
"""This is also a comment"""
```

### Constant
A value that shouldn't change during the program.
```python
MAX_PLAYERS = 4  # Usually in UPPER_CASE
```

### Constructor
The special method that creates new objects (`__init__`).
```python
def __init__(self, name):
    self.name = name
```

## D

### Dataclass
A special Python decorator that makes classes easier to write.
```python
@dataclass
class Tile:
    number: int
    color: str
```

### Debug
Finding and fixing problems in code.

### Decorator
Special syntax that modifies functions or classes (starts with @).
```python
@dataclass  # This is a decorator
class MyClass:
    pass
```

### Dictionary (Dict)
A collection that stores key-value pairs.
```python
scores = {'Alice': 10, 'Bob': 15}
```

### Docstring
A special comment that documents what a function does.
```python
def add(a, b):
    """Add two numbers together."""
    return a + b
```

## E

### Edge Case
An unusual situation that might break your code.
- Empty lists
- Very large numbers
- None values

### Enum
A set of named constants.
```python
class GamePhase(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
```

### Exception
An error that happens when code runs.
```python
raise ValueError("Invalid tile!")
```

## F

### Function
A reusable set of instructions.
```python
def say_hello():
    print("Hello!")
```

### For Loop
Code that repeats for each item in a collection.
```python
for tile in tiles:
    print(tile)
```

## G

### Global
A variable available throughout the entire program.

## H

### Helper Function
A small function that helps other functions do their job.

## I

### Import
Bringing code from another file to use.
```python
from tiles import Tile
```

### Indentation
The spaces at the start of lines that Python uses to organize code.
```python
if True:
    print("This is indented")
```

### Index
The position of an item in a list (starts at 0).
```python
tiles[0]  # First tile (index 0)
tiles[1]  # Second tile (index 1)
```

### Instance
A specific object created from a class.
```python
player1 = Player("Alice")  # player1 is an instance
```

### Integer (int)
A whole number.
```python
score = 42
```

## J

### JSON
A format for storing data that both humans and computers can read.
```json
{
    "name": "Alice",
    "score": 10
}
```

## K

### Keyword
Special words Python understands (if, for, def, class, etc.).

## L

### List
An ordered collection of items.
```python
tiles = [tile1, tile2, tile3]
```

### Local Variable
A variable only available inside a function.

### Loop
Code that repeats multiple times.

## M

### Method
A function that belongs to a class.
```python
player.draw_tile()  # draw_tile is a method
```

### Module
A Python file containing code you can import.

### Mutable
Something that can be changed after creation (like lists).

## N

### None
Python's way of saying "nothing" or "no value".
```python
result = None
```

### Nested
Something inside something else.
```python
nested_list = [[1, 2], [3, 4]]
```

## O

### Object
A specific instance created from a class.
```python
my_tile = Tile(5, 'red')  # my_tile is an object
```

### Optional
Something that might or might not be provided.
```python
Optional[str]  # Might be a string or None
```

## P

### Parameter
What a function expects to receive (in the definition).
```python
def greet(name):  # 'name' is a parameter
    print(f"Hello {name}")
```

### Pass
A placeholder that does nothing.
```python
def future_feature():
    pass  # TODO: implement later
```

## Q

### Query
Asking for information without changing anything.

## R

### Return
What a function gives back.
```python
def add(a, b):
    return a + b  # Returns the sum
```

### Refactor
Improving code without changing what it does.

## S

### Self
How an object refers to itself in methods.
```python
def get_name(self):
    return self.name  # self refers to this object
```

### String (str)
Text in quotes.
```python
message = "Hello, World!"
```

### Syntax
The rules for how to write code correctly.

## T

### Tuple
An unchangeable list.
```python
position = (x, y)  # Can't be modified
```

### Type
What kind of data something is (int, str, list, etc.).

### Type Hint
Telling Python what type of data to expect.
```python
def add(a: int, b: int) -> int:
    return a + b
```

## U

### Unit Test
A test for one small piece of code.

## V

### Variable
A name that stores a value.
```python
player_name = "Alice"
```

### Validation
Checking if something is correct before using it.

## W

### While Loop
Code that repeats while a condition is true.
```python
while game_running:
    play_turn()
```

## Common Phrases

### "Raise an exception"
Make an error happen on purpose.
```python
raise ValueError("Something went wrong!")
```

### "Call a function"
Use a function.
```python
result = calculate_score()  # Calling the function
```

### "Instantiate an object"
Create a new object from a class.
```python
player = Player("Alice")  # Instantiating a Player
```

### "Iterate over"
Go through each item one by one.
```python
for item in items:  # Iterating over items
    print(item)
```

### "Pass by reference/value"
How Python gives information to functions.

### "Snake case"
Naming style with underscores: `player_name`

### "Camel case"
Naming style with capitals: `playerName`

### "Pascal case"
Naming style for classes: `PlayerClass`

---

## Tips for Learning Terms

1. **Don't memorize everything** - Look them up when needed
2. **Learn by using** - Write code to understand terms
3. **Context helps** - See how terms are used in real code
4. **Ask questions** - If confused, the term might be poorly explained

Remember: Every programmer was confused by these terms at first. It gets easier with practice!