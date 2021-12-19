import re

class Simulation:
    def __init__(self, target):
        m = re.match(r'target area: x=(.+)\.\.(.+), y=(.+)\.\.(.+)', target)
        self.target_x_min = int(m[1])
        self.target_x_max = int(m[2])
        self.target_y_min = int(m[3])
        self.target_y_max = int(m[4])

    def is_inside_target(self, x, y):
        return (self.target_x_min <= x <= self.target_x_max) and \
               (self.target_y_min <= y <= self.target_y_max)

    # Assumes the probe is fired from up and to the left of the target.
    def past_target(self, x, y):
        return (x > self.target_x_max) or (y < self.target_y_min)

    def fire(self, x_velocity, y_velocity):
        x,y = 0,0
        steps = []
        while True:
            x += x_velocity
            y += y_velocity
            steps.append((x,y))

            if self.is_inside_target(x,y):
                return True, steps
            elif self.past_target(x,y):
                return False, steps
            
            if x_velocity > 0:
                x_velocity -= 1
            elif x_velocity < 0:
                x_velocity += 1

            y_velocity -= 1


    def fire_with_diagram(self, x_velocity, y_velocity):
        hit, steps = self.fire(x_velocity, y_velocity)
        min_y = min(min(y for x,y in steps), self.target_y_min)
        max_y = max(max(y for x,y in steps), 0)
        min_x = 0
        max_x = max(max(x for x,y in steps), self.target_x_max)

        diagram = []
        for y in range(max_y, min_y-1, -1):
            ln = ''
            for x in range(min_x, max_x+1):
                if (x,y) == (0,0):
                    ln += 'S'
                elif (x,y) in steps:
                    ln += '#'
                elif self.is_inside_target(x,y):
                    ln += 'T'
                else:
                    ln += '.'
            diagram.append(ln)
        return hit, max_y, diagram         
        

    def interact(self):
        while True:
            vals = input('\nx,y velocity (or any letter to quit): ')
            try:
                x_velocity, y_velocity = [int(d) for d in vals.split(',')]
            except:
                print('Finished, thanks')
                return
            
            hit, max_y, diagram = sim.fire_with_diagram(x_velocity, y_velocity)
            print(f'\n  {x_velocity, y_velocity} {"Hits" if hit else "Misses"}, max y: {max_y}\n')
            for ln in diagram:
                print(ln)
            print('\n')
    
  

    def find_highest_y_position(self):
        # Works both for "How high does probe rise before slowing to 0"
        # And "How far in x direction before slowing to zero"
        displacement_before_reaching_zero = lambda n: ((n+1) * n) / 2

        # Assumption: we'll be going high enough that x_velocity will drop to zero.
        # Here is a horrible algorithm. We can use root finding if this is too slow!
        x_velocity = 1
        while displacement_before_reaching_zero(x_velocity) < self.target_x_min: 
            x_velocity += 1
        if displacement_before_reaching_zero(x_velocity) > self.target_x_max:
            # Clever maths needed here to go up a bit and start drop to target before x hits zero.
            raise Exception("Current algorithm can't make x hit the target")

        # Probe will rise, come back to y=0, then take another step. That step'll be initial
        # velocity +1. We want a step as big as possible without missing the target.
        y_velocity = (self.target_y_min +1) * -1
        highest_y_position = displacement_before_reaching_zero(y_velocity)
        return (x_velocity, y_velocity), highest_y_position


    def find_every_initial_velocity_that_hits(self):
        # We worked out some limits in part 1:
        # Any initial x lower than this won't reach the target area.
        # Any initial y higher than this won't hit the target.
        (min_x, max_y), _ = self.find_highest_y_position()

        # Rule out the limits that would overshoot target in first step.
        max_x = self.target_x_max 
        min_y = self.target_y_min

        velocities = set()
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                hit, _ = self.fire(x,y)
                if hit:
                    velocities.add((x,y))
        return velocities


#--------------------- tests -------------------------#

def test_first_example():
    sim = Simulation('target area: x=20..30, y=-10..-5')
    hit, steps = sim.fire(7,2)
    assert hit
    assert steps == [(7,2), (13,3), (18, 3), (22,2), (25,0), (27,-3), (28,-7)]

def test_second_example():
    sim = Simulation('target area: x=20..30, y=-10..-5')
    hit, steps = sim.fire(6,3)
    assert hit
    assert len(steps) == 9

def test_third_example():
    sim = Simulation('target area: x=20..30, y=-10..-5')
    hit, steps = sim.fire(9,0)
    assert hit
    assert len(steps) == 4

def test_fourth_example():
    sim = Simulation('target area: x=20..30, y=-10..-5')
    hit, steps = sim.fire(17,-4)
    assert not hit
    assert len(steps) == 2  

def test_fire_with_diagram():
    sim = Simulation('target area: x=20..30, y=-10..-5')
    _, _, diagram = sim.fire_with_diagram(7,2)
    assert diagram[0] == '.............#....#............'
    assert diagram[-1] == '....................TTTTTTTTTTT'
    
def test_find_highest_y_position():
    sim = Simulation('target area: x=20..30, y=-10..-5')
    initial_velocity, highest_y_position = sim.find_highest_y_position()
    assert initial_velocity == (6,9)
    assert highest_y_position == 45

def test_find_every_initial_velocity_that_hits():
    sim = Simulation('target area: x=20..30, y=-10..-5')
    velocities = sim.find_every_initial_velocity_that_hits()
    assert len(velocities) == 112

#-----------------------------------------------------#

if __name__ == "__main__":
    sample_data = 'target area: x=20..30, y=-10..-5'
    puzzle_input = 'target area: x=70..96, y=-179..-124'
    sim = Simulation(puzzle_input)
    initial_velocity, highest_y_position = sim.find_highest_y_position()
    print(f'\nPredicted highest shot: {initial_velocity} hits, with max y of {highest_y_position}\n')
    velocities = sim.find_every_initial_velocity_that_hits()
    print(f'Found {len(velocities)} ways to hit target\n')
    
