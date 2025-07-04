# Computer Science Final Project in Computer Communication (by Gil Etzioni and Zack Portnoy)

This project demonstrates a system designed to transmit data between two computers using speakers and microphones. The sender produces tones, and the receiver listens and decodes the signals. This project highlights skills in audio processing, data transmission, and computer networking.

# Project Overview
The system enables audio-based communication between two computers. The sender generates specific tones that are decoded by the receiver, showcasing an innovative approach to data transmission using sound waves.


![image_alt](https://github.com/GilEtzioni/cummunication-project/blob/main/description/3-classDiagram.jpg?raw=true)
# User Interface
Left Screen - Sender Computer.
Right Screen - Reciever Computer.
![image_alt](https://github.com/GilEtzioni/cummunication-project/blob/main/description/2-demo.jpg?raw=true)
# Theoretical Background & Protocols
The system relies on well-established theories and protocols in audio processing and computer networking. These principles form the foundation for encoding and decoding the transmitted data via sound waves.
![image_alt](https://github.com/GilEtzioni/cummunication-project/blob/main/description/4-theoretic.jpg?raw=true)
![image_alt](https://github.com/GilEtzioni/cummunication-project/blob/main/description/5-theoretic.jpg?raw=true)
![image_alt](https://github.com/GilEtzioni/cummunication-project/blob/main/description/6-theoretic.jpg?raw=true)
![image_alt](https://github.com/GilEtzioni/cummunication-project/blob/main/description/7-theoretic.jpg?raw=true)


## Prerequisites

Make sure you have the following installed on your system:

- Python (>= 3.x)
- Git

## Cloning the Repository

To clone this project, run the following command in your terminal or command prompt:

```sh
git clone https://github.com/GilEtzioni/cummunication-project.git
cd cummunication-project
```

## Setting Up the Virtual Environment (Recommended)

To avoid dependency conflicts, it is recommended to create a virtual environment:

```sh
python -m venv venv
```

Activate the virtual environment:

- **Windows:**
  ```sh
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```sh
  source venv/bin/activate
  ```

## Installing Dependencies

Once inside the project directory, install the required dependencies using:

```sh
pip install -r dependencies.txt
```

## Running the Project

Execute the main script to start the application:

```sh
python main.py
```

## Troubleshooting

If you encounter any issues, try the following:

- Ensure all dependencies are correctly installed.
- Check if the virtual environment is activated.
- Verify that Python is installed and correctly added to your system path.
