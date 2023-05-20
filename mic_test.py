import queue
import sys
import sounddevice as sd
import ast
from vosk import Model, KaldiRecognizer
import time

class MicrophoneListener:
    def int_or_str(self, text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.queue.put(bytes(indata))

    def __init__(self):
        self.queue = queue.Queue()
        
    def run(self):
        try:
            device_info = sd.query_devices(None, "input")
            samplerate = int(device_info["default_samplerate"])
            model = Model(lang="pl")

            with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=None, dtype="int16", channels=1, callback=self.callback):
                rec = KaldiRecognizer(model, samplerate)
                while True:
                    if rec.AcceptWaveform(self.queue.get()):
                        print(f'___full: {ast.literal_eval(rec.Result())["text"]}')
                    else:
                        print(f'partial: {ast.literal_eval(rec.PartialResult())["partial"]}')

        except KeyboardInterrupt:
            print("\nDone")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    MicrophoneListener().run()