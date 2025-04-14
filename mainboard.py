from clock_timer import Clock_timer
import tkinter as tk

class Mainboard:
    def __init__(self, root):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.onehz_clock = Clock_timer()
        self.onehz_clock.start()
        
        #size of background and root 700x700
        self.canvas = tk.Canvas(root, width=700, height=700, bg='white')
        self.canvas.pack()
        
        # LEDS AND BUTTONS FOR CLOCK ----------------------------------------------------------------
        tk.Label(root, text="Clock", font=("Arial", 14, "bold")).place(x=20, y=0)
        self.clock_led = self.canvas.create_oval(20, 40, 36, 56, fill="gray")
        self.hlt_led = self.canvas.create_oval(60, 40, 76, 56, fill="gray")
        self.hlt_button = tk.Button(root, text="HLT", width=6, height=1, command=self.mhlt_button)
        self.hlt_button.place(x=55, y=60)
    
        self.select_led = self.canvas.create_oval(105, 40, 121, 56, fill="gray")
        self.select_button = tk.Button(root, text="SELECT", width=7, height=1, command=self.mselect_button)
        self.select_button.place(x=98, y=60)
    
        self.manual_led = self.canvas.create_oval(160, 40, 176, 56, fill="gray")
        self.manual_button = tk.Button(root, text="MANUAL", width=7, height=1, command=self.mmanual_button)
        self.manual_button.place(x=153, y=60)
        
        # LEDS AND BUTTONS FOR INPUT A --------------------------------------------------------------------------------------------------
        tk.Label(root, text="Register A", font=("Arial", 14, "bold")).place(x=400, y=0)
        
        self.regA_leds = []
        for i in range(8):
            x = 400 + i * 30
            led = self.canvas.create_oval(x, 40, x + 16, 56, fill="gray")
            self.regA_leds.append(led)
    
            btn = tk.Button(root, text=str(i), width=2)
            btn.place(x=x, y=60)
        
        
        
        self.syncing_connections()        
        

    def mhlt_button(self):
        """
        on hlt button press
        """
        self.onehz_clock.halt()
        
        
        
        

    def mselect_button(self):
        """
        on select button press
        """
        self.onehz_clock.select_switch()



    def mmanual_button(self):
        """
        on manual button press
        """
        self.onehz_clock.manual_pulse()
        
        
        self.canvas.itemconfig(self.manual_led, fill="#FFD700")
        self.root.after(250, lambda: self.canvas.itemconfig(self.manual_led, fill="gray"))        



    def syncing_connections(self):
        """
        proper LED following every 100ms just checking over and recoloring.
        """
        clk_out, hlt_led, select_led, manual_led = self.onehz_clock.clock_logic(manual_pulse_input=0)

        self.canvas.itemconfig(self.clock_led, fill=self.onehz_clock.color if not self.onehz_clock.hlt else "gray")
        self.canvas.itemconfig(self.hlt_led, fill="#FFD700" if hlt_led else "gray")
        self.canvas.itemconfig(self.select_led, fill="#FFD700" if select_led else "gray")
        

        self.root.after(100, self.syncing_connections)



    def on_close(self):
        """
        on root close called in __init__ as the funcitno to call on close of window
        """
        print("Stopping Process")
        self.root.destroy()
        self.onehz_clock.end()