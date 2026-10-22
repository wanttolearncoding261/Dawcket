import pygame
import librosa
import soundfile as sf
from pydub import AudioSegment
import numpy as np
import os

class AudioEngine:
    """
    The Core Audio Brain of Loop Maker Half Life.
    Handles Sampling, Looping, and Real-time BPM Syncing.
    """
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.master_bpm = 120
        self.active_loops = {} # { 'LOOP_1': pygame.mixer.Channel }
        self.samples_dir = "samples"

        if not os.path.exists(self.samples_dir):
            os.makedirs(self.samples_dir)

    def set_bpm(self, new_bpm):
        self.master_bpm = new_bpm
        print(f"Master BPM set to: {self.master_bpm}")
        # In a full implementation, this would trigger a re-stretch of all active loops

    def record_sample(self, loop_id, duration=4):
        """
        Simulates recording from the PCM1808 ADC.
        In the final hardware, this uses the PyAudio/JACK stream.
        """
        print(f"Recording {loop_id} for {duration} seconds...")
        # Mock recording: normally we'd capture raw bytes from I2S
        # For the demo, we'll just save a dummy file or use a placeholder
        filename = f"{self.samples_dir}/{loop_id}.wav"
        # (Recording logic would go here)
        print(f"Sample saved to {filename}")

    def load_and_sync_sample(self, loop_id):
        """
        Loads a .wav file and time-stretches it to match the master BPM.
        """
        filename = f"{self.samples_dir}/{loop_id}.wav"
        if not os.path.exists(filename):
            print(f"No sample found for {loop_id}")
            return None

        # 1. Load audio
        y, sr = librosa.load(filename)

        # 2. Calculate time-stretch factor
        # This is a simplification: assumes sample was recorded at 120 BPM
        stretch_factor = 120 / self.master_bpm
        y_stretched = librosa.effects.time_stretch(y, rate=stretch_factor)

        # 3. Save stretched version to temp file for pygame
        temp_path = f"{self.samples_dir}/{loop_id}_synced.wav"
        sf.write(temp_path, y_stretched, sr)

        return pygame.mixer.Sound(temp_path)

    def play_loop(self, loop_id):
        sound = self.load_and_sync_sample(loop_id)
        if sound:
            channel = pygame.mixer.find_channel()
            if channel:
                channel.play(sound, loops=-1) # Loop indefinitely
                self.active_loops[loop_id] = channel
                print(f"Playing {loop_id} at {self.master_bpm} BPM")

    def stop_loop(self, loop_id):
        if loop_id in self.active_loops:
            self.active_loops[loop_id].stop()
            del self.active_loops[loop_id]
            print(f"Stopped {loop_id}")

    def set_volume(self, loop_id, volume):
        if loop_id in self.active_loops:
            self.active_loops[loop_id].set_volume(volume)
