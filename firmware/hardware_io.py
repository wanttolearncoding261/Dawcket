import RPi.GPIO as GPIO
import time
from threading import Thread

class HardwareIO:
    """
    Handles all physical inputs for the Loop Maker Half Life.
    Maps Buttons and Rotary Encoders to Raspberry Pi GPIO pins.
    """
    def __init__(self, callback_map):
        # Pin Mapping
        self.BUTTONS = {
            'REC': 17, 'PLAY': 27, 'STOP': 22,
            'LOOP_1': 10, 'LOOP_2': 9, 'LOOP_3': 11,
            'LOOP_4': 5, 'SYNC': 6
        }
        self.ENCODERS = {
            'BPM': {'CLK': 13, 'DT': 19},
            'FX':  {'CLK': 26, 'DT': 20},
            'VOL': {'CLK': 21, 'DT': 16}
        }

        self.callback_map = callback_map # Dictionary of functions to call on event

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Initialize Buttons (Pull-up resistors)
        for btn, pin in self.BUTTONS.items():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # Add interrupt for each button
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=lambda ch, b=btn: self._on_button_press(b), bouncetime=200)

        # Initialize Encoders
        for enc, pins in self.ENCODERS.items():
            GPIO.setup(pins['CLK'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(pins['DT'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # Encoders are polled in a separate thread for precision

        self.running = True
        self.poll_thread = Thread(target=self._poll_encoders, daemon=True)
        self.poll_thread.start()

    def _on_button_press(self, button_name):
        if button_name in self.callback_map:
            self.callback_map[button_name]()

    def _poll_encoders(self):
        # Keep track of previous state
        last_clk = {enc: GPIO.input(pins['CLK']) for enc, pins in self.ENCODERS.items()}

        while self.running:
            for enc, pins in self.ENCODERS.items():
                clk_val = GPIO.input(pins['CLK'])
                if clk_val != last_clk[enc]:
                    # Rotation detected
                    dt_val = GPIO.input(pins['DT'])
                    direction = 1 if clk_val != dt_val else -1

                    if enc in self.callback_map:
                        self.callback_map[enc](direction)

                    last_clk[enc] = clk_val
            time.sleep(0.001) # 1ms poll rate

    def stop(self):
        self.running = False
        GPIO.cleanup()
