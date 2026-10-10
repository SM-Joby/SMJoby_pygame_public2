import pygame, random, sys
pygame.init()

gravity = 0.5

class Bird:
    def __init__(self):#not putting atributes because we are giving the actual values, like parameters in a function
        self.x = 80
        self.y = 250
        self.radius = 20
        self.velocity = 0
        self.gravity = 0.5
        self.jumpstrength = -10
        # initisalising atributes, all of the above
        
    def jump (self):
        self.velocity = self.jumpstrength
            
    def update(self):
        self.velocity += self.gravity #incrementing gravity to allow bird to fall down
        self.y += self.velocity #showing that the velocity is bringing the ball down

    def draw(self,surface,yellow):
        pygame.draw.circle(surface,yellow,(self.x,int(self.y)),self.radius)# we are not putting x as an integer because x is already an integer
            #initially both x and y are integers however y is affected by the velocity which inturn is affected by gravity
            #gravity is decreasing by 0.5 which which affects y by turning it into a float number instead of an integer
            #we must replace y as an interger since it is a co-ordinate and co-ordinates cannot be floats

    def get_rect(self):
        return pygame.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)#a rectangle for the ball (x,y,width,height)
#when we want to draw a rectangle OBJECT its pygame.Rect with a capital r instead of drawing a rectangle using pygame.draw.rect
         
    
#pipes
class Pipe:
    WIDTH = 70
    gap = 180
    pipespeed = 4 # makes the screen appear as if it is by moving the pipes across the screen
    def __init__(self,screenheight, screenwidth):
        height = random.randint(120,screenheight-250)
        self.top = pygame.Rect(screenwidth,0,self.WIDTH,height)#x,y,l,w
        self.bottom = pygame.Rect(screenwidth, height+self.gap, self.WIDTH, screenheight-height-self.gap)#x,y,l,w
        self.passed = False
    
    def update(self):
        self.top.x = self.top.x - self.pipespeed  
        self.bottom.x = self.bottom.x - self.pipespeed

    def draw(self,surface,green):
        pygame.draw.rect(surface,green,self.top)
        pygame.draw.rect(surface,green,self.bottom)

    def collide(self,bird):
        return(bird.get_rect().colliderect(self.top)or bird.get_rect().colliderect(self.bottom))

    def offscreen(self):
        return(self.top.right<0)#if self.top goes past 0 on the x axis it means the pipes are off the screen

class game:
    def __init__(self):
        self.WIDTH = 500
        self.HEIGHT = 700
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption("Flappybird!")
        self.clock = pygame.time.Clock()#used to control the pace of the game
        self.font = pygame.font.SysFont("Calibri",30)
        self.red = (255,0,0)
        self.blue = (0,0,255)
        self.green = (0,255,0)
        self.yellow = (255,255,0)
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.bgblue = (26,189,230)
        self.bird = Bird()
        self.score = 0
        self.pipes = [Pipe(self.HEIGHT,self.WIDTH)] # the reason the class is in the [] is because we have taken a list of the pipes further in the code
        self.running = True

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.jump()

    def update(self):
        self.bird.update()
        #for pipe in self.pipes just means the pipes in our list pipe!
        for pipe in self.pipes:#to update the pipes!!!!
            pipe.update()
            if pipe.collide(self.bird):#only give brackets after giving function nam
                self.running = False
            if(not pipe.passed and pipe.top.right<self.bird.x):
                pipe.passed = True
                self.score = self.score+1
        self.pipes = [pipe for pipe in self.pipes if not pipe.offscreen()]
        #self.pipes can be multiple(2),each has its own offscreen function, which tells us if its on the screen
        #keep the pipe on screen if it is visible, if not keep it out of the list /screen
        #we are using offscreen function to allow us to know which pipes to keep in or kick out of the list
        if (len(self.pipes) == 0 or self.pipes[-1].top.x < self.WIDTH-250):
            self.pipes.append(Pipe(self.HEIGHT,self.WIDTH))
        if (self.bird.y +self.bird.radius> self.HEIGHT or self.bird.y-self.bird.radius<0):#error, must take radius into account
            self.running = False
        pygame.display.update()

    def draw(self):
        #pipes,bg, bird, score
        self.screen.fill(self.bgblue)
        self.bird.draw(self.screen,self.yellow)
        for pipe in self.pipes:
            pipe.draw(self.screen,self.green)
        text = self.font.render("Score"+ str(self.score), True, self.black)#error, forgot last two parameters
        self.screen.blit(text,(25,25))
        pygame.display.update()

    def game_over(self):
        self.screen.fill(self.black)
        over = self.font.render("GAME OVER - FINAL SCORE" +str(self.score),True, self.red)
        self.screen.blit(over,(100,400))
        pygame.display.update()
        pygame.time.wait(3000)#pausing time, note forgotten, time is wirtten in milliseconds therefore 3000 = 3 sec

    def run(self):
        while self.running:
            self.clock.tick(20)#limiting the frame to 20 t/sec
            self.handling_events()
            self.update()
            self.draw()
        self.game_over()
        sys.exit()

if __name__ == "__main__":#name is an existing python variable, name is its stored value when we execute the file directly
    #it will create the game object and then run the game class from its object if the game is run like its suppoesed to
    g = game()
    g.run()
    




            