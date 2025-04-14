import time
import threading

class Clock_timer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = True
        self.bit = 0
        self.prev_bit = 0
        self.mode = 0  # 0 = astable, 1 = manual
        self.hlt = 0
        self.button_halt = 0
        self.color = "gray"

    def run(self):
        print("Starting Clock...")
        interval = 1.0
        next_time = time.perf_counter()
        while self.running:
            if not self.button_halt and not self.hlt and self.mode == 0:
                self.clock_tick()
                next_time += interval
                time.sleep(interval)

    def clock_tick(self):
        self.bit ^= 1
        self.color = "#FFD700" if self.bit else "gray"
        if self.bit == 1 and self.prev_bit == 0:
            self.on_rising_edge()
        self.prev_bit = self.bit
        print(self.bit)

    def end(self):
        self.running = False

    def pause(self):
        self.button_halt ^= 1

    def halt(self):
        self.hlt ^= 1

    def select_switch(self):
        self.mode ^= 1  # only change mode

    def manual_pulse(self):
        if self.mode == 1 and not self.hlt:
            self.clock_tick()

    def on_rising_edge(self):
        print("RISING EDGE detected")

    def clock_logic(self, manual_pulse_input):
        A = self.bit
        S = self.mode
        H = self.hlt
        M = manual_pulse_input

        CLK_OUT = (not H) and ((A and not S) or (M and S))
        HLT_LED = H
        SELECT_LED = S
        MANUAL_LED = M and S and not H

        return CLK_OUT, HLT_LED, SELECT_LED, MANUAL_LED