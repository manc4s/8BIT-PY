import time
import threading 
import pygame       #for visuals
import os




#parent class is a new thread.
class Clock_timer(threading.Thread):
    
    def __init__(self, screen):
        #if you want class variables here uncomment the line below before 
        super().__init__()

        
        self.screen = screen
        
        #Circle Dimensions
        self.rect = self.screen.get_rect()
        self.radius = min(self.rect.width, self.rect.height) // 2

        self.running = True
        

        self.bit = 0
        

    def run(self):
        #built in for classes that runs immediately on thread when .start() is called on instance
        
        print("Starting Clock...")
        




        interval = 1.0
        next_time = time.perf_counter()

        while self.running:
            self.clock_tick()
            next_time += interval
            sleep_time = next_time - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)



    def clock_tick(self):
        self.screen.fill((0, 0, 0))  # black

        if self.bit == 0:

            pygame.draw.circle(self.screen, (255, 255, 255), self.rect.center, self.radius)
            pygame.display.flip()
            self.bit = 1
        
        else:
            pygame.draw.circle(self.screen, (255, 0, 0), self.rect.center,self.radius)
            pygame.display.flip()
            self.bit = 0




    def end(self):
        self.running  = False




#clock_visual initiated with pygame
pygame.init()
clock_visual_screen = pygame.display.set_mode((200, 100))


#1hz clock instance
onehz_clock = Clock_timer(clock_visual_screen)    
onehz_clock.start()






running = True
while running:
    print("The main loop is also running here")


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            onehz_clock.end()
            print("main loop and program have ended")
            
    time.sleep(0.01)

pygame.quit()