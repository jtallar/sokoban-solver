import enum
import objects as obj

# Possible elements in space
# Eg:   for el in (Element):
#           print(el.name + ' ' + el.value)
class Element(enum.Enum):
    Box = "\U0001F5C2"
    BoxInGoal = "\U0001F5C3"
    Goal = "\U0001F3C1"
    Wall = "\U0001F5FB"
    Player = "\U0001F920"
    PlayerInGoal = "\U0001F929"
    Space = "  "

    

