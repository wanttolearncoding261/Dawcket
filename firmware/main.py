import kivy.app
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from hardware_io import HardwareIO
from midi_handler import MIDIHandler
from audio_engine import AudioEngine

class LoopMakerMain(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # 1. Initialize Engines
        self.audio = AudioEngine()

        # Define callbacks for Hardware and MIDI
        # These functions are called when a button is pressed or MIDI note is received
        self.callbacks = {
            'REC': self.handle_record,
            'PLAY': self.handle_play,
            'STOP': self.handle_stop,
            'LOOP_1': lambda: self.audio.play_loop('LOOP_1'),
            'LOOP_2': lambda: self.audio.play_loop('LOOP_2'),
            'LOOP_3': lambda: self.audio.play_loop('LOOP_3'),
            'LOOP_4': lambda: self.audio.play_loop('LOOP_4'),
            'BPM': self.handle_bpm_change,
            'VOL': self.handle_volume_change
        }

        # 2. Start Hardware and MIDI Listeners
        try:
            self.hw = HardwareIO(self.callbacks)
            self.midi = MIDIHandler(self.callbacks)
        except Exception as e:
            print(f"Hardware not detected (Normal on PC): {e}")

        # 3. Build UI
        self.add_widget(Label(text="LOOP MAKER HALF LIFE", font_size='32sp', size_hint_y=0.2))

        self.status_label = Label(text="Status: Ready", font_size='20sp', size_hint_y=0.1)
        self.add_widget(self.status_label)

        # Grid of Loop Buttons
        self.btn_grid = BoxLayout(orientation='horizontal')
        for i in range(1, 5):
            btn = Button(text=f"Loop {i}")
            btn.bind(on_press=lambda instance, idx=i: self.audio.play_loop(f'LOOP_{idx}'))
            self.btn_grid.add_widget(btn)
        self.add_widget(self.btn_grid)

        # Master Controls
        self.ctrl_grid = BoxLayout(orientation='horizontal')
        rec_btn = Button(text="RECORD", background_color=(1, 0, 0, 1))
        rec_btn.bind(on_press=self.handle_record)

        stop_btn = Button(text="STOP ALL")
        stop_btn.bind(on_press=self.handle_stop)

        self.ctrl_grid.add_widget(rec_btn)
        self.ctrl_grid.add_widget(stop_btn)
        self.add_widget(self.ctrl_grid)

    def handle_record(self, *args):
        self.status_label.text = "Status: RECORDING..."
        # We'll record Loop 1 by default for this demo
        self.audio.record_sample('LOOP_1')
        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Status: Ready'), 4)

    def handle_play(self, *args):
        self.status_label.text = "Status: Playing All"
        for i in range(1, 5):
            self.audio.play_loop(f'LOOP_{i}')

    def handle_stop(self, *args):
        self.status_label.text = "Status: Stopped"
        for i in range(1, 5):
            self.audio.stop_loop(f'LOOP_{i}')

    def handle_bpm_change(self, direction):
        # Encoder rotation: +1 or -1
        current_bpm = self.audio.master_bpm
        new_bpm = current_bpm + (direction * 1)
        self.audio.set_bpm(new_bpm)
        self.status_label.text = f"BPM: {new_bpm}"

    def handle_volume_change(self, direction):
        # Simplified volume control
        print(f"Volume changed: {direction}")

class LoopMakerApp(kivy.app.App):
    def build(self):
        return LoopMakerMain()

if __name__ == '__main__':
    LoopMakerApp().run()
