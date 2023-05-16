import numpy as np
import pygame as pg
from random import randint, gauss
import math

pg.init()
pg.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (89, 203, 232)
GREEN = (0, 110, 51)

SCREEN_SIZE = (800, 600)


def rand_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))

class GameObject:

    def move(self):
        pass
    
    def draw(self, screen):
        pass  

class Tank(GameObject):
    def __init__(self, coord=[SCREEN_SIZE[0]//2, SCREEN_SIZE[1]-30], angle=0, maxSpeed = 10, color = BLACK, health = 100, score_table=None):
        '''
        Constructor method
        '''
        self.coord = coord
        self.angle = angle
        self.maxSpeed = maxSpeed
        self.color = color
        self.active = False
        self.moving = False
        self.health = health
        self.score_table = score_table 
        self.inc = 0
        self.alive = True
    def draw(self, screen):
        '''
        Draws the tank on the screen
        '''
        # pg.draw.rect(screen, WHITE, [10, 20, 30, 40])
        if (self.alive):
            pg.draw.rect(screen, WHITE, [self.coord[0]-15,self.coord[1]-10,30,20])
            self.move(self.inc)
    def move(self, inc):
        '''
        Changes the horizontal position of the tank
        '''
        self.inc = inc
        if (self.moving):
            if (self.coord[0] > 30 or inc > 0) and (self.coord[0] < SCREEN_SIZE[0] - 30 or inc < 0):
                self.coord[0] += inc
    
    def checkCollision(self, bomb):
        '''
        Checks collision of the tank with bombs
        '''
        if (bomb.coord[0] > self.coord[0] - 15 and bomb.coord[0] < self.coord[0] + 15):
            if (bomb.coord[1] > self.coord[1] - 10):
                return True
        return False

    
    def explosion(self, x, y, size=150):
        explode = True

        explosion_surface = pg.Surface(screen.get_size())  # Create a surface with the same size as the screen
        explosion_surface.set_colorkey((0, 0, 0))  # Set black color as the transparent color

        color_choices = [(255, 0, 0), (255, 128, 128), (255, 255, 0), (255, 255, 128)]

        while explode:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

            magnitude = 1

            while magnitude < size:
                exploding_bit_x = x + randint(-1 * magnitude, magnitude)
                exploding_bit_y = y + randint(-1 * magnitude, magnitude)

                pg.draw.circle(explosion_surface, color_choices[randint(0, 3)], (exploding_bit_x, exploding_bit_y),
                            randint(1, 5))
                magnitude += 1

            explode = False

        screen.blit(explosion_surface, (0, 0))  # Blit the explosion surface onto the screen
        pg.display.update()
    
    def decrease_health(self, amount):
        '''
        Decreases the tank's health by the specified amount.
        '''
        self.health -= amount
        print(self.health)



class Shell(GameObject):
    '''
    The ball class. Creates a ball, controls it's movement and implement it's rendering.
    '''
    def __init__(self, coord, vel, rad=20, color=None):
        '''
        Constructor method. Initializes ball's parameters and initial values.
        '''
        self.coord = coord
        self.vel = vel
        if color == None:
            color = rand_color()
        self.color = color
        self.rad = rad
        self.is_alive = True

    def check_corners(self, refl_ort=0.8, refl_par=0.9):
        '''
        Reflects ball's velocity when ball bumps into the screen corners. Implemetns inelastic rebounce.
        '''
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1-i] = int(self.vel[1-i] * refl_par)
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1-i] = int(self.vel[1-i] * refl_par)

    def move(self, time=1, grav=0):
        '''
        Moves the ball according to it's velocity and time step.
        Changes the ball's velocity due to gravitational force.
        hahahshds
        '''
        self.vel[1] += grav
        for i in range(2):
            self.coord[i] += time * self.vel[i]
        self.check_corners()
        if self.vel[0]**2 + self.vel[1]**2 < 2**2 and self.coord[1] > SCREEN_SIZE[1] - 2*self.rad:
            self.is_alive = False

    def draw(self, screen):
        '''
        Draws the ball on appropriate surface.
        '''
        pg.draw.circle(screen, self.color, self.coord, self.rad)

class Laser(GameObject):
    '''
    Create alternate Shell shot that is a straight line.
    '''
    def __init__(self, coord, angle, rad=100,  color=None):
        '''
        Constructor method. Initializes ball's parameters and initial values.
        '''
        self.coord = coord
        self.angle = angle
        if color == None:
            color = rand_color()
        self.rad = rad
        self.color = color
        self.is_alive = True
       
    def move(self, grav=0):
        '''
        Keeps laser trail stationary
        '''
        '''
         current_time = pg.time.get_ticks() 
        remove_laser_time = pg.time.get_ticks() + 1000
        while remove_laser_time >= current_time:
            current_time = pg.time.get_ticks()
            if remove_laser_time <= current_time:
                self.is_alive = False
        '''
       
        pass

    def draw(self, screen):
        '''
        Draws line straight from cannon angle
        '''
        laser_shape = []
        vec_1 = np.array([int(5*np.cos(self.angle - np.pi/2)), int(5*np.sin(self.angle - np.pi/2))])
        vec_2 = np.array([int(800*np.cos(self.angle)), int(800*np.sin(self.angle))])
        gun_pos = np.array(self.coord)
        laser_shape.append((gun_pos + vec_1).tolist())
        laser_shape.append((gun_pos + vec_1 + vec_2).tolist())
        laser_shape.append((gun_pos + vec_2 - vec_1).tolist())
        laser_shape.append((gun_pos - vec_1).tolist())
        pg.draw.polygon(screen, self.color, laser_shape)

class Cannon(GameObject):
    '''
    Cannon class. Manages it's renderring, movement and striking.
    '''
    def __init__(self, coord=[SCREEN_SIZE[0]//2, SCREEN_SIZE[1]-30], angle=0, max_pow=50, min_pow=10, color=RED):
        '''
        Constructor method. Sets coordinate, direction, minimum and maximum power and color of the gun.
        '''
        self.coord = coord
        self.angle = angle
        self.max_pow = max_pow
        self.min_pow = min_pow
        self.color = color
        self.active = False
        self.pow = min_pow
        self.moving = False
        self.inc = 0
        self.alive = True
    
    def activate(self):
        '''
        Activates gun's charge.
        '''
        self.active = True

    def gain(self, inc=2):
        '''
        Increases current gun charge power.
        '''
        if self.active and self.pow < self.max_pow:
            self.pow += inc

    def strike(self):
        '''
        Creates ball, according to gun's direction and current charge power.
        '''
        if self.alive:
            vel = self.pow
            angle = self.angle
            ball = Shell(list(self.coord), [int(vel * np.cos(angle)), int(vel * np.sin(angle))])
            self.pow = self.min_pow
            self.active = False
        return ball
    
    def strike_laser(self):
        '''
        Creates laser, according to gun's direction and current charge power.
        Must be max power to shoot laser, otherwise shoot blank.
        '''
        angle = self.angle
        if self.pow == 50:
            ball = Laser(list(self.coord), angle)
            self.pow = self.min_pow
            self.active = False
            
        else:
            ball = Shell(list([0,0]), [int(0), int(0)], 0)
            self.pow = self.min_pow
            self.active = False     
        # add new shell
        return ball
    
    def strike_scatter(self, vel, angle):
        '''
        Creates 3 balls, according to gun's direction and current charge power.
        '''
        ball = Shell(list(self.coord), [int(vel * np.cos(angle)), int(vel * np.sin(angle))], 10)
        # add new shell
        return ball
        
    def set_angle(self, target_pos):
        '''
        Sets gun's direction to target position.
        '''
        self.angle = np.arctan2(target_pos[1] - self.coord[1], target_pos[0] - self.coord[0])

    def move(self, inc):
        '''
        Changes vertical position of the gun.
        '''
        self.inc = inc
        if (self.moving):
            if (self.coord[0] > 30 or inc > 0) and (self.coord[0] < SCREEN_SIZE[0] - 30 or inc < 0):
                self.coord[0] += inc

    def draw(self, screen):
        '''
        Draws the gun on the screen.
        '''
        if (self.alive):
            gun_shape = []
            vec_1 = np.array([int(5*np.cos(self.angle - np.pi/2)), int(5*np.sin(self.angle - np.pi/2))])
            vec_2 = np.array([int(self.pow*np.cos(self.angle)), int(self.pow*np.sin(self.angle))])
            gun_pos = np.array(self.coord)
            gun_shape.append((gun_pos + vec_1).tolist())
            gun_shape.append((gun_pos + vec_1 + vec_2).tolist())
            gun_shape.append((gun_pos + vec_2 - vec_1).tolist())
            gun_shape.append((gun_pos - vec_1).tolist())
            pg.draw.polygon(screen, self.color, gun_shape)
            self.move(self.inc)
class Target(GameObject):
    '''
    Target class. Creates target, manages it's rendering and collision with a ball event.
    '''
    def __init__(self, coord=None, color=None, rad=30):
        '''
        Constructor method. Sets coordinate, color and radius of the target.
        '''
        if coord == None:
            coord = [randint(rad, SCREEN_SIZE[0] - rad), randint(rad, SCREEN_SIZE[1] - rad)]
        self.coord = coord
        self.rad = rad
        self.dropsBombs = False

        if color == None:
            color = rand_color()
        self.color = color
        
        

    def check_collision(self, ball):
        '''
        Checks whether the ball bumps into target.
        '''
        dist = sum([(self.coord[i] - ball.coord[i])**2 for i in range(2)])**0.5
        min_dist = self.rad + ball.rad
        return dist <= min_dist

    def draw(self, screen):
        '''
        Draws the target on the screen
        '''
        pg.draw.circle(screen, self.color, self.coord, self.rad)

    def move(self):
        """
        This type of target can't move at all.
        :return: None
        """
        pass
class LinearMovingTargets(Target):
    def __init__(self, coord=None, color=None, rad=30):
        super().__init__(coord, color, rad)
        self.vx = randint(-2, +2)
        self.vy = randint(-2, +2)
    
    def move(self):
        self.coord[0] += self.vx
        self.coord[1] += self.vy
        self.check_corners()
    def check_corners(self):
        '''
        Reflects ball's velocity when ball bumps into the screen corners.
        '''
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                if i == 0:
                    self.vx = -int(self.vx)
                else:
                    self.vy = -int(self.vy)
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                if i == 0:
                    self.vx = -int(self.vx)
                else:
                    self.vy = -int(self.vy)
class RandomMovingTargets(Target):
    def __init__(self, coord=None, color=None, rad=30):
        super().__init__(coord, color, rad)
    
    def move(self):
        self.vx = randint(-2, +2)
        self.vy = randint(-2, +2)
        self.coord[0] += self.vx
        self.coord[1] += self.vy
        self.check_corners()
    def check_corners(self):
        '''
        Reflects ball's velocity when ball bumps into the screen corners. Implemetns inelastic rebounce.
        '''
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                if i == 0:
                    self.vx = -int(self.vx)
                else:
                    self.vy = -int(self.vy)
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                if i == 0:
                    self.vx = -int(self.vx)
                else:
                    self.vy = -int(self.vy)
class SmoothRandomMovingTargets(Target):
    def __init__(self, coord=None, color=None, rad=30):
        super().__init__(coord, color, rad)
        self.vx = randint(-2, +2)
        self.vy = randint(-2, +2)
    
    def move(self):
        '''
        Moves randomly but doesn't fo back and forth
        '''
        if self.vx >= 0 and self.vy >= 0:
            self.vx = randint(0, +2)
            self.vy = randint(0, +2)
        if self.vx <= 0 and self.vy >= 0:
            self.vx = randint(-2, 0)
            self.vy = randint(0, +2)
        if self.vx <= 0 and self.vy <= 0:
            self.vx = randint(-2, 0)
            self.vy = randint(-2, 0)
        if self.vx >= 0 and self.vy <= 0:
            self.vx = randint(0, +2)
            self.vy = randint(-2, 0)
        self.coord[0] += self.vx
        self.coord[1] += self.vy
        self.check_corners()
    def check_corners(self):
        '''
        Reflects ball's velocity when ball bumps into the screen corners. Implemetns inelastic rebounce.
        '''
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                if i == 0:
                    self.vx = -int(self.vx)
                else:
                    self.vy = -int(self.vy)
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                if i == 0:
                    self.vx = -int(self.vx)
                else:
                    self.vy = -int(self.vy)
class CircularMovingTargets(Target):
    def __init__(self, coord=None, color=None, rad=30):
        super().__init__(coord, color, rad)
        self.time = 0
        self.offset = randint(-8, 8)
        if self.offset == 0:
            self.offset = self.offset + 1
    
    def move(self):
        '''
        Moves in a circle
        '''
        self.time = self.time + 1
        self.coord[0] += self.offset*math.sin(self.time/self.offset)
        self.coord[1] += self.offset*math.cos(self.time/self.offset)
        self.check_corners()
    
    def check_corners(self):
        '''
        Reflects ball's velocity when ball bumps into the screen corners. Implemetns inelastic rebounce.
        '''
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
class BombDroppingTarget(Target):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    def __init__(self, coord=None, color=None, rad=30):
        super().__init__(coord, color, rad)
        self.vx = randint(-2, +2)
        self.vy = randint(-2, +2)
        self.bombs = []  # Initialize the bombs attribute as an empty list
        self.tank = Tank()

    def move(self):
        self.coord[0] += self.vx
        self.coord[1] = self.rad  # Restrict vertical movement to the top of the screen
        self.checkCorners()
        
        # Drop a bomb at a certain probability
        if randint(1, 100) < 2:  # 5% chance of dropping a bomb
            self.dropBombs()
        
         # Apply gravity to the bombs
        for bomb in self.bombs:
            bomb.move(time=1, grav=0.5)  # Adjust the gravity value as needed
        
    def checkCorners(self):

        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                if i == 0:
                    self.vx = -int(self.vx)
                else:
                    self.vy = -int(self.vy)
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                if i == 0:
                    self.vx = -int(self.vx)
                else:
                    self.vy = -int(self.vy)

        # Check if the bomb touches the ground or the tank
        for bomb in self.bombs:
            if bomb.coord[1] >= SCREEN_SIZE[1] - bomb.rad:
                # Bomb explodes when it touches the ground or collides with the tank
                bomb.is_alive = False
                if self.tank.checkCollision(bomb):
                    self.tank.explosion(self.tank.coord[0], self.tank.coord[1])  # Trigger the tank's explosion
                    self.tank.decrease_health(50)
                    self.tank.alive = False
                    self.dead = True
                    print("boom!")
                else:
                    self.explosion(bomb.coord[0], bomb.coord[1])  # Call the explosion method with bomb coordinates

        # Remove the bombs that have exploded
        self.bombs = [bomb for bomb in self.bombs if bomb.is_alive]


    def dropBombs(self):
        # Create a new bomb object at the current position of the target
        bomb = Shell(list(self.coord), [0, 5], rad=10, color=RED)  # Customize the bomb properties as needed
        self.bombs.append(bomb)  # Add the bomb to the bombs list

    def draw(self, screen):
        super().draw(screen)  # Call the draw method of the parent class

        
        # Draw the bombs on the screen with flashing colors
        for bomb in self.bombs:
            if randint(1, 2) == 1:  # Randomly select between red and yellow color
                color = RED
            else:
                color = YELLOW
            bomb.color = color
            bomb.draw(screen)
    
    def explosion(self, x, y, size=50):
        explode = True

        explosion_surface = pg.Surface(screen.get_size())  # Create a surface with the same size as the screen
        explosion_surface.set_colorkey((0, 0, 0))  # Set black color as the transparent color

        color_choices = [(255, 0, 0), (255, 128, 128), (255, 255, 0), (255, 255, 128)]

        while explode:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

            magnitude = 1

            while magnitude < size:
                exploding_bit_x = x + randint(-1 * magnitude, magnitude)
                exploding_bit_y = y + randint(-1 * magnitude, magnitude)

                pg.draw.circle(explosion_surface, color_choices[randint(0, 3)], (exploding_bit_x, exploding_bit_y),
                            randint(1, 5))
                magnitude += 1

            explode = False

        screen.blit(explosion_surface, (0, 0))  # Blit the explosion surface onto the screen
        pg.display.update()

class ScoreTable:
    def __init__(self, t_destr=0, b_used=0, tank=None):
        self.t_destr = t_destr
        self.b_used = b_used
        self.tank = tank
        self.font = pg.font.SysFont("dejavusansmono", 25)
        self.score_surf = []

    def score(self):
        return self.t_destr - self.b_used

    def draw(self, screen):
        self.score_surf = []
        self.score_surf.append(self.font.render("Q Normal | W Scatter | E Laser" , True, WHITE))
        self.score_surf.append(self.font.render("Destroyed: {}".format(self.t_destr), True, WHITE))
        self.score_surf.append(self.font.render("Balls used: {}".format(self.b_used), True, WHITE))
        self.score_surf.append(self.font.render("Total: {}".format(self.score()), True, RED))
        if self.tank:
            self.score_surf.append(self.font.render("Health: {}".format(self.tank.health), True, RED))

        for i in range(len(self.score_surf)):
            screen.blit(self.score_surf[i], [10, 10 + 30 * i])



class Manager:
    '''
    Class that manages events' handling, ball's motion and collision, target creation, etc.
    '''
    def __init__(self, n_targets=1):
        self.balls = []
        self.gun = Cannon()
        self.targets = []
        self.score_t = ScoreTable()
        self.n_targets = n_targets
        self.new_mission()
        self.tank = Tank()
        self.score_t = ScoreTable(tank=self.tank)
        self.dead = False

    def new_mission(self):
        '''
        Adds new targets.
        '''
        for i in range(self.n_targets):
            self.targets.append(LinearMovingTargets(rad=randint(max(1, 30 - 2*max(0, self.score_t.score())),30 - max(0, self.score_t.score()))))
            self.targets.append(Target(rad=randint(max(1, 30 - 2*max(0, self.score_t.score())), 30 - max(0, self.score_t.score()))))
            self.targets.append(SmoothRandomMovingTargets(rad=randint(max(1, 30 - 2*max(0, self.score_t.score())),30 - max(0, self.score_t.score()))))
            self.targets.append(CircularMovingTargets(rad=randint(max(1, 30 - 2*max(0, self.score_t.score())),30 - max(0, self.score_t.score()))))
            self.targets.append(BombDroppingTarget(rad=randint(max(1, 30 - 2*max(0, self.score_t.score())), 30 - max(0, self.score_t.score()))))

    def process(self, events, screen):
        '''
        Runs all necessary method for each iteration. Adds new targets, if previous are destroyed.
        '''
        done = self.handle_events(events)

        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)
        self.move()
        self.collide()
        self.draw(screen)

        if len(self.targets) == 0 and len(self.balls) == 0:
            self.new_mission()

        return done

    def handle_events(self, events):
        '''
        Handles events from keyboard, mouse, etc.
        '''
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN: #move up
                if event.key == pg.K_UP:
                    self.gun.moving = True
                    self.gun.move(-5)
                    self.tank.moving = True
                    self.tank.move(-5)
                elif event.key == pg.K_DOWN: #move down
                    self.gun.moving = True
                    self.gun.move(5)
                    self.tank.moving = True
                    self.tank.move(5)
                elif event.key == pg.K_q: #normal Q
                    self.gun.color = RED
                    self.gun.activate()
                elif event.key == pg.K_w: #scatter W
                    self.gun.color = GREEN
                    self.gun.activate()
                elif event.key == pg.K_e: #laser E
                    self.gun.color = BLUE
                    self.gun.activate()
            elif event.type == pg.KEYUP:
                self.gun.moving = False
                self.tank.moving = False
                if not self.dead:
                    if event.key == pg.K_q:
                        self.balls.append(self.gun.strike())
                        self.score_t.b_used += 1
                    elif event.key == pg.K_w:
                        self.balls.append(self.gun.strike_scatter(self.gun.pow, self.gun.angle))
                        self.balls.append(self.gun.strike_scatter(self.gun.pow, self.gun.angle-0.1))
                        self.balls.append(self.gun.strike_scatter(self.gun.pow, self.gun.angle+0.1))
                        self.gun.pow = self.gun.min_pow
                        self.gun.active = False
                        self.score_t.b_used += 1
                    elif event.key == pg.K_e:
                        self.balls.append(self.gun.strike_laser())
                        self.score_t.b_used += 1
            #elif self.dead:
                #clock.tick(60000)
                #done = True
        return done

    def draw(self, screen):
        '''
        Runs balls', gun's, targets' and score table's drawing method.
        '''
        for ball in self.balls:
            ball.draw(screen)
        for target in self.targets:
            target.draw(screen)
        self.tank.draw(screen)
        self.gun.draw(screen)
        self.score_t.draw(screen)
        

    def move(self):
        '''
        Runs balls' and gun's movement method, removes dead balls.
        '''
        dead_balls = []
        for i, ball in enumerate(self.balls):
            ball.move(grav=2)
            if not ball.is_alive:
                dead_balls.append(i)
        for i in reversed(dead_balls):
            self.balls.pop(i)
        for i, target in enumerate(self.targets):
            target.move()
        self.gun.gain()

    def collide(self):
        collisions = []
        targets_c = []
        for i, ball in enumerate(self.balls):
            for j, target in enumerate(self.targets):
                if target.check_collision(ball):
                    collisions.append([i, j])
                    targets_c.append(j)
        targets_c.sort()
        for j in reversed(targets_c):
            self.score_t.t_destr += 1
            self.targets.pop(j)


        dead_balls = []
        for i, ball in enumerate(self.balls):
            if not ball.is_alive:
                dead_balls.append(i)
        for i in reversed(dead_balls):
            self.balls.pop(i)


        

        


screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Our gun")

done = False
clock = pg.time.Clock()

mgr = Manager(n_targets=2)  # number of targets per type
mgr.score_t = ScoreTable(tank=mgr.tank)  # Pass the tank instance to the ScoreTable constructor


while not done:
    clock.tick(15)
    screen.fill(BLACK)

    done = mgr.process(pg.event.get(), screen)

    pg.display.flip()


pg.quit()
