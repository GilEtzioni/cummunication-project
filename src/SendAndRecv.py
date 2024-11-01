import time
import threading
from SendTest import Send
from RecvTest import Recv



# Create threads for writing and reading
writer_thread = threading.Thread(target=Send)
reader_thread = threading.Thread(target=Recv)

# Start the threads

reader_thread.start()
time.sleep(0.5)
writer_thread.start()

# Wait for the threads to finish
writer_thread.join()
reader_thread.join()