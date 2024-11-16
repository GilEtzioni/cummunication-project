import time
import subprocess
subprocess.Popen(["python3","src/RecvTestAudio.py"])
time.sleep(0.5)
subprocess.Popen(["python3","src/SendTestAudio.py"])