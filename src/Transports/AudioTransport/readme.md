# Explained audio transport layer

## Encoding

    We transfer data over audio using 258 different frequencies.
    256 data frequencies represent one byte of data, 
    2 control frequencies are used to control frame start and timing.

### Frequency configuration

    The frequencies used are based on the resolution of fft for a given number of samples in the receiving window and a starting frequency
    For example given:
        START_FREQUENCY = 10000Hz
        RECV_WINDOW_MS = 50
        RECV_SAMPLE_PER_S = 41200
    We would get (Hz):
        10000, 10020, 10040, 10060, 10080,...  15360. 15380.

### Byte level encoding

    I order to better sample the sent data on the receiving end each byte is sent with a short control signal before and after it.
    For example if sending 4 bytes [1,2,3] 
    Represented by F[1],F[2],F[3]
    We prepend and append F[257] to each byte
    The sending waveform would look something like this:
        F[257] F[1]F[1]F[1] F[257] F[2]F[2]F[2] F[257] F[3]F[3]F[3] F[257]
    this enables the receiving end to recognize a window that starts and ends with F[257]

### Frame Level

    Each frame consists of
        FRAME_HEADER FRAME_LENGTH DATA CHECKSUM_256
    Where:
        FRAME_HEADER is 4 bytes 258,258,258,258
        FRAME_LENGTH is a value between 0 and 40
        DATA is and array of up to 40 bytes
        CHECKSUM = sum(DATA)%256

### Stop and Wait

    After each frame a response frame will be sent from the receiver to the transmitter containing a one byte code.
    This byte will represent success or failure of transmission.
    Each frame transmission can end with one of these codes 
        SUCCESS: transmission completed successfully
        RECV_TIMEOUT: Receiver did not receive the complete frame in time
        BAD_CHECKSUM: Receiver checksum didn't match
        TRANSMITTER_TIMEOUT: transmitter did not receive response frame in time.
    On transmission failure the transmitter will retry up to X times before giving up

### Configurations and transmission speed
    Sender/ receiver sampling rate: 41200/1192000
    Microphone Frequency response: 200Hz ~19000Hz (it drops at higher frequencies)
    Reciever fft block size
    Reciever window size (TODO explain this)
    Receiver fft calc rate
    

