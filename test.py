# from dataclasses import dataclass, field

# @dataclass
# class Cell:
#     walls: dict[str, bool] = field(
#         default_factory=lambda: {
#             "N": True,
#             "E": True,
#             "S": True,
#             "W": True,
#         }
#     )
#     visited: bool = False

# c1 = Cell()
# c2 = Cell()

# c1.walls["N"] = False
# print(c1.walls)
# print(c2.walls)

# print("----------------------")
# class Cell2:
#     def __init__(self):
#         self.walls = {
#             "N": True,
#             "E": True,
#             "S": True,
#             "W": True,
#         }
#         self.visited = False

# t1 = Cell2()
# t2 = Cell2()

# t1.walls["N"] = False
# print(t1.walls)
# print(t2.walls)


import random

random.seed(42)
print(random.randint(1, 10))
print(random.randint(1, 10))
print(random.randint(1, 10))