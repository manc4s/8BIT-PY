#my library
from clock_timer import Clock_timer




#libraries
import time
import threading
import tkinter as tk








class Mainboard(threading.Thread):



    def __init__(self, root):
        

        #self.root
        #self.canvas
        #self.hlt_led self.hlt_button
        #self.select_led self.select_button
        #self.manual_led self.manual_button


        self.root = root

        """
        The line below is important because there needs a way for the clock to end
        when the program is closed. Otherwise if you are running from command line 
        or elsewhere there will be issues when testing and running and it will get stuck.
        """
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)   #on close method has the closing rotocol.



        #--------------------------- INIT OF THE MAIN CLOCK -------------------------------------------------------------------------------


        #1hz clock instance
        self.onehz_clock = Clock_timer()    
        self.onehz_clock.start()  #initiates onehz_clock.run


        self.onehz_clock.set_callback(self.update_main_tick)



        # --------------------------- FORMATING OF THE MAIN BOARD BELOW in INIT -------------------------------------------------------------

        root.title("main computer board")
        self.canvas = tk.Canvas(root, width=700, height=700, bg='white')
        self.canvas.pack()



        # Main clock LED
        self.clock_led = self.canvas.create_oval(20, 20, 36, 36, fill="gray")

        # HLT
        self.hlt_led = self.canvas.create_oval(60, 20, 76, 36, fill="gray")
        self.hlt_button = tk.Button(root, text="HLT", width=6, height=1, command=self.mhlt_button)
        self.hlt_button.place(x=55, y=40)

        # SELECT
        self.select_led = self.canvas.create_oval(105, 20, 121, 36, fill="gray")
        self.select_button = tk.Button(root, text="SELECT", width=7, height=1, command=self.mselect_button)
        self.select_button.place(x=98, y=40)

        # MANUAL
        self.manual_led = self.canvas.create_oval(160, 20, 176, 36, fill="gray")
        self.manual_button = tk.Button(root, text="MANUAL", width=7, height=1, command=self.mmanual_button)
        self.manual_button.place(x=153, y=40)




        self.syncing_connections()





    def update_main_tick(self, color):
        self.root.after(0, lambda: self.canvas.itemconfig(self.clock_led, fill=color))

        


    
    def mhlt_button(self):
        self.onehz_clock.pause()        



    def mselect_button(self):
        self.onehz_clock.select_switch()




    def mmanual_button(self):
        
        if self.onehz_clock.button_halt == 0 and self.onehz_clock.mode == 1:
            self.canvas.itemconfig(self.manual_led, fill="#FFD700")
            
            
            self.onehz_clock.manual_pulse()
            
            #small break just to show manual button was pressed, so it goes green for a sec or two in this case.
            self.root.after(200, lambda: self.canvas.itemconfig(self.manual_led, fill="gray"))
    


            






    def syncing_connections(self, force_manual_gray = False):
        halted = self.onehz_clock.button_halt
        manual = self.onehz_clock.mode

        # Clock LED
        if halted:
            self.canvas.itemconfig(self.clock_led, fill="red")
        else:
            self.canvas.itemconfig(self.clock_led, fill=self.onehz_clock.color)

        # Manual LED — ONLY SET when not blinking yellow
        current_color = self.canvas.itemcget(self.manual_led, "fill")
        if current_color != "#FFD700":
            if manual == 1 and halted == 0:
                self.canvas.itemconfig(self.manual_led, fill="gray")  # ready
            else:
                self.canvas.itemconfig(self.manual_led, fill="red")   # blocked

        # HLT LED
        self.canvas.itemconfig(self.hlt_led, fill="#FFD700" if halted else "gray")

        # SELECT LED
        self.canvas.itemconfig(self.select_led, fill="#FFD700" if manual else "gray")

        self.root.after(100, self.syncing_connections)




    def on_close(self):

        print("Stopping Process")


        
        self.root.destroy()
        self.onehz_clock.end()





        

