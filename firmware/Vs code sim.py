import time
import keyboard
import threading
import os

# --- SETTINGS ---
BPM = 60
CHANNELS = 12


class LoopMakerHalfLife:
    def __init__(self):
        self.bpm = BPM
        self.playing = {i: False for i in range(1, CHANNELS + 1)}

        # Clear the screen to make it look like a real machine 
        os.system('cls' if os.name == 'nt' else 'clear')

        print("==========================================")
        print("       LOOP MAKER HALF LIFE (v1.0)        ")
        print("==========================================")
        print(" STATUS: READY")
        print(" BPM:    ", self.bpm)
        print("------------------------------------------")
        print(" CONTROLS:")
        print("  Keys [1] through [0, -, =] -> Trigger Loops")
        print("  Key [S]                    -> Stop All")
        print("  Key [Q]                    -> Quit Program")
        print("==========================================")

    def trigger(self, channel):
        if self.playing[channel]:
            print(f" [OFF] Loop {channel} Stopped")
            self.playing[channel] = False
        else:
            print(f" [ON ] Loop {channel} started at {self.bpm} BPM")
            self.playing[channel] = True
            # Start the "beat" in a separate background thread
            threading.Thread(target=self._beat_engine, args=(channel,), daemon=True).start()

    def _beat_engine(self, channel):
        while self.playing[channel]:
            # This simulates the audio beat visually in the terminal
            print(f"  >>> BEAT {channel} <<<")
            time.sleep(60 / self.bpm)

    def stop_all(self):
        print("\n!!! EMERGENCY STOP: All Loops Killed !!!")
        for i in self.playing:
            self.playing[i] = False


# --- MAIN PROGRAM ---
machine = LoopMakerHalfLife()

while True:
    try:
        # Mapping keys to channels
        keys = ['1','2','3','4','5','6','7','8','9','0','-','=']
        for i, key in enumerate(keys):
            if keyboard.is_pressed(key):
                machine.trigger(i + 1)
                time.sleep(0.3) # Prevents one press from triggering 100 times

        if keyboard.is_pressed('s'):
            machine.stop_all()
            time.sleep(0.3)

        if keyboard.is_pressed('q'):
            print("Shutting down...")
            break

        time.sleep(0.05)
    except Exception as e:
        print(f"Error: {e}")
        break
