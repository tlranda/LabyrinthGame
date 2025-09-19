import numpy as np
np.random.seed(1)

class TextArena():
    def __init__(self, xy, chardict):
        self.size = xy
        self.chardict = chardict
        self.state = []
        for y in range(xy[1]):
            row = []
            for x in range(xy[0]):
                if x == 0 or x == xy[0]-1:
                    if y == 0 or y == xy[1]-1:
                        row.append(chardict['wall_connect'])
                    else:
                        row.append(chardict['vwall'])
                elif y == 0 or y == xy[1]-1:
                    row.append(chardict['hwall'])
                else:
                    row.append(chardict['empty'])
            self.state.append(row)

    def place(self, key, xy):
        self.state[xy[1]+1][xy[0]+1] = self.chardict[key]

    def applymove(self, move, xy):
        # Get symbol
        symbol = self.state[xy[1]+1][xy[0]+1]
        # Reset
        self.state[xy[1]+1][xy[0]+1] = self.chardict['empty']
        # Lookup destination
        newxy = (min(self.size[0]-1, max(1,xy[0]+move.off_x+1)),
                 min(self.size[1]-1, max(1,xy[1]+move.off_y+1)))
        if self.state[newxy[1]][newxy[0]] != self.chardict['empty']:
            return False
        # Place symbol
        self.state[newxy[1]][newxy[0]] = symbol
        return True

    def render(self):
        for y in self.state:
            for x in y:
                print(x,end='')
            print()

states = {'vwall': '|',
          'hwall': '-',
          'wall_connect': '+',
          'empty': ' ',
          'object': 'O',
          'object_destroyed': '/',
          'player': 'P',
          'enemy': 'E',
          'enemy_dead': 'X',
          }

ta = TextArena((20,20), states)
n_objects = 3
n_destroyed_objects = 1
enemies = 2
dead_enemies = 1
positions = np.random.randint(0,19, 2*(n_objects+n_destroyed_objects+1+enemies+dead_enemies))
offset, end_offset = 0, 0
for n_items, key in zip([n_objects, n_destroyed_objects, 1, enemies, dead_enemies],
                        ['object','object_destroyed','player','enemy','enemy_dead']):
    end_offset += 2*n_items
    for px, py in zip(positions[offset:end_offset:2], positions[offset+1:end_offset:2]):
        ta.place(key, (px,py))
    offset = end_offset
frame = 1
print(f"Frame {frame}: TextArena")
ta.render()
frame += 1

class Move():
    def __init__(self, off_x, off_y):
        self.off_x, self.off_y = off_x, off_y

move_player = Move(2,-2)
ok = ta.applymove(move_player, positions[2*(n_objects+n_destroyed_objects):][:2])
print("Move was ok?", ok)
print(f"Frame {frame}: TextArea")
ta.render()

