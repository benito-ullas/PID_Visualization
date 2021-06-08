import pygame
from vector import vector2D
import matplotlib.pyplot as plt

pygame.init()
key = pygame.key.get_pressed()

t = 0
t_pos = []
y_pos = []

fps = 60
fpsClock = pygame.time.Clock()

screen = None
scr_width = 600
scr_height = 400

d = None

# comments below are values u can try out
kp = 0.5 #0.07 : 5
ki = 0  #0.6 : 1.01
kd = 0    #8 : 60


################################################

class Drone:
        def __init__(self,a,b):
                self.pos = vector2D(a,b)
                self.vel = vector2D(0,0)
                self.acc = vector2D(0,0)
                self.width = 100
                self.height = 5
                self.integral = vector2D(0,0) 
                self.prev_error = vector2D(0,0)
                self.dt = 50
        def update(self):
                #self.acc.mult(self.dt)
                self.vel.add(self.acc)
                
                #self.vel.mult(self.dt)
                self.pos.add(self.vel)
                
                self.acc.mult(0)
                
        def show(self):
                pygame.draw.rect(screen,(255,255,255),(self.pos.x,self.pos.y,self.width,self.height),0)
                
        def edges(self):
                if (self.pos.y + self.height) >= scr_height:
                        self.pos.y = scr_height - self.height
                
        def add_g(self):
                gravity = vector2D(0,0.7)
                #gravity.mult(self.dt)
                self.acc.add(gravity)
        
        def thrust(self):
                power = vector2D(0,-0.6)
                #power.mult(self.dt)
                self.acc.add(power)
        
        def pid_controller(self,setp,kp,ki,kd):
                error = vector2D(0,0)
                error.subtract(setp,self.pos)
                
                proportional = vector2D(error.x,error.y)
                proportional.mult(kp)
                
                self.integral.add(error)
                #print(f"{self.integral.x}  {self.integral.y}")
                self.integral.mult(ki)
                
                derivative = vector2D(0,0)
                derivative.subtract(error, self.prev_error)
                self.prev_error = vector2D(error.x,error.y)
                derivative.mult(kd)
                
                u_t = vector2D(0,0)
                u_t.add(proportional)
                u_t.add(self.integral)
                u_t.add(derivative) 
                
                
                steering = vector2D(0,0)
                steering.subtract(u_t,self.vel)
                steering.div(self.dt)
                self.acc.add(steering)
                
                
                 
                

################################################

def setup():
        global screen, scr_width, scr_height
        global text, textRect
        screen = pygame.display.set_mode((scr_width,scr_height))
        
        global d
        d = Drone(scr_width/2,scr_height - 15)
        
def draw():
        global d,screen,y_pos,kp,ki,kd
        setp = scr_height/2
        
        screen.fill((51,51,51))
        d.add_g()
        d.pid_controller(vector2D(scr_width/2,setp),kp,ki,kd)
        #print(f"{d.pos.x} : {d.pos.y}")
        
        #for ploting graph 
        y_pos.append(scr_height - d.pos.y)
        
        d.update()
        d.edges()
        d.show()
        pygame.draw.line(screen,(0,255,0),[0,setp],[scr_width,setp])
        

        pygame.display.flip()
################################################        
setup()
running = True
while running:
        # Quiting program when pygame window is closed
        for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
                        running = False
        draw()
        pygame.display.update()
        
        #for ploting graph
        t_pos.append(t)
        t += 1
         
        fpsClock.tick(fps)
t1_pos = []
for i in range(t):
        t1_pos.append(200)
         
plt.plot(t_pos,y_pos)

plt.plot(t_pos,t1_pos)
plt.savefig("2.png")
###################################################
