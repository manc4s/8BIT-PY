import time
import threading 




#parent class is a new thread.
class Clock_timer(threading.Thread):
    
    def __init__(self):
        #if you want class variables here uncomment the line below before 
        super().__init__()
        
        self.running = True
        
        #value of clock
        self.bit = 0

        
        self.mode = 0 #select or switch, 1hz = 0, manual = 1
        self.hlt = 0 #0 running, 1 halted


        self.button_halt = 0

        self.color = "grey"
     
        self.gui_callback = None


    def set_callback(self, callback):
        self.gui_callback = callback




    def run(self):
        #built in for classes that runs immediately on thread when .start() is called on instance
        
        print("Starting Clock...")
        




        interval = 1.0
        next_time = time.perf_counter()
        
        
        while self.running:

            if not self.button_halt:
                if not self.hlt:
                    self.clock_tick()
                    next_time += time.perf_counter() + interval
                    time.sleep(interval)



    def clock_tick(self):

        if self.bit == 0:
            self.bit = 1
            self.color = "green"
        
        else:
            self.bit = 0
            self.color = "gray"

        self.gui_callback(self.color)

        print(self.bit)


    def end(self):
        self.running  = False


    def pause(self):
        self.button_halt = not self.button_halt


    
    def halt(self):
        
        self.hlt = not self.hlt


    
    

    def select_switch(self):

        if not self.mode:
            self.mode = 1 # manual

            if not self.hlt:
                self.halt()

            

        else:
            self.mode = 0

            if self.hlt:
                self.halt()

        



    def manual_pulse(self):

        if self.hlt and self.mode:
            self.clock_tick()
            
            



