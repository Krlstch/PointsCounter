import queue
import sys
import sounddevice as sd
import ast
from vosk import Model, KaldiRecognizer
import time

class MicrophoneListener:
    def __init__(self):
        self.queue = queue.Queue()
        
    def run(self):
        try:
            device_info = sd.query_devices(None, "input")
            samplerate = int(device_info["default_samplerate"])
            model = Model(lang="pl")

            with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=None, dtype="int16", channels=1, callback=self.callback):
                recognizer = KaldiRecognizer(model, samplerate)
                begin_date = None
                while True:
                    current_date = time.localtime()
                    
                    if recognizer.AcceptWaveform(self.queue.get()):
                        text = ast.literal_eval(recognizer.Result())["text"]
                        if text:
                            sys.stdout.write(f'\r{self.format_date(begin_date)} - {self.format_date(current_date)}: {text}\n')
                            begin_date = None
                    else:
                        text = ast.literal_eval(recognizer.PartialResult())["partial"]

                        begin_date = current_date if not begin_date or not text else begin_date
                        sys.stdout.write(f'\r{self.format_date(begin_date)} - {self.format_date(current_date)}: {text}')

        except KeyboardInterrupt:
            print("\nDone")
        except Exception as e:
            print(e)

    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.queue.put(bytes(indata))

    def format_date(self, date: time.struct_time):
        return time.strftime("%Y.%m.%d %H:%M:%S", date)

if __name__ == "__main__":
    MicrophoneListener().run()