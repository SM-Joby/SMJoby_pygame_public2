import pygame, random, sys
pygame.init()

gravity = 0.5

class Balloon:
    def __init__(self):
        self.x = 80
        self.y = 250
        self.radius = 20
        self.velocity = 0
        self.gravity = 0.5
        self.jumpstrength = -10
        
    def jump (self):
        self.velocity = self.jumpstrength
            
    def update(self):
        self.velocity += self.gravity 
        self.y += self.velocity 

    def draw(self,surface,red):
        pygame.draw.circle(surface,red,(self.x,int(self.y)),self.radius) 
           
    def get_rect(self):
        return pygame.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)
    
class Pin:
    WIDTH = 70
    gap = 180
    pinspeed = 4
    def __init__(self,screenheight, screenwidth):
        height = random.randint(120,screenheight-250)
        self.top = pygame.Rect(screenwidth,0,self.WIDTH,height)
        self.bottom = pygame.Rect(screenwidth, height+self.gap, self.WIDTH, screenheight-height-self.gap)
        self.passed = False
    
    def update(self):
        self.top.x = self.top.x - self.pinspeed  
        self.bottom.x = self.bottom.x - self.pinspeed

    def draw(self,surface,black):
        pygame.draw.rect(surface,black,self.top)
        pygame.draw.rect(surface,black,self.bottom)

    def collide(self,balloon):
        return(balloon.get_rect().colliderect(self.top)or balloon.get_rect().colliderect(self.bottom))

    def offscreen(self):
        return(self.top.right<0)
    
class game:
    def __init__(self):
        self.WIDTH = 500
        self.HEIGHT = 700
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption("Don't POP the Balloon!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Calibri",30)
        self.red = (255,0,0)
        self.blue = (0,0,255)
        self.green = (0,255,0)
        self.yellow = (255,255,0)
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.bgblue = (26,189,230)
        self.balloon = Balloon()
        self.score = 0
        self.pins = [Pin(self.HEIGHT,self.WIDTH)] 
        self.running = True

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.balloon.jump()

    def update(self):
        self.balloon.update()
        for pin in self.pins:
            pin.update()
            if pin.collide(self.balloon):
                self.running = False
            if(not pin.passed and pin.top.right<self.balloon.x):
                pin.passed = True
                self.score = self.score+1
        self.pins = [pin for pin in self.pins if not pin.offscreen()]

        if (len(self.pins) == 0 or self.pins[-1].top.x < self.WIDTH-250):
            self.pins.append(Pin(self.HEIGHT,self.WIDTH))
        if (self.balloon.y +self.balloon.radius> self.HEIGHT or self.balloon.y-self.balloon.radius<0):
            self.running = False
        pygame.display.update()

    def draw(self):
        self.screen.fill(self.bgblue)
        self.balloon.draw(self.screen,self.red)
        for pin in self.pins:
            pin.draw(self.screen,self.black)
        text = self.font.render("Score"+ str(self.score), True, self.blue)
        self.screen.blit(text,(25,25))
        pygame.display.update()

    def game_over(self):
        self.screen.fill(self.black)
        over = self.font.render("GAME OVER - FINAL SCORE: " +str(self.score),True, self.red)
        self.screen.blit(over,(100,400))
        pygame.display.update()
        pygame.time.wait(3000)

    def run(self):
        while self.running:
            self.clock.tick(20)
            self.handling_events()
            self.update()
            self.draw()
        self.game_over()
        sys.exit()

if __name__ == "__main__": 
    g = game()
    g.run()
    




            