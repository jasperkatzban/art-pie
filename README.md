# Surface Player
### An interactive turntable for exploring the sounds of everyday objects.

## About the Project
This was a final project for the Fall 2021 iteration of the Principles of Integrated Engineering (PIE) course @olin

Check out the full project writeup and website [here](https://olincollege.github.io/pie-2021-03/ArtPie/)

## Setup
While this project is intended for use on a Raspberry Pi integrated with the rest of our mechanical and electrical systems, it may still be run locally with limited functionality.

For best results, we suggest having
- a webcam
- a red laser line
- a means of playing audio
- a Fadecandy board with some WS2812b LEDs

## Installation
This project was developed for UNIX-based python environments. As such, we do not guarantee that all dependences are Windows tested, nor that the core source code is compatible with the audio rendering or usb device interfacing on that OS.

### Local Setup
1. First, clone the repository to your computer:
    ```
    git clone https://github.com/jasperkatzban/surface-player.git
    ```

2. It's recommended that you run this project from a Python virtual environment, which can be set up like this:
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. If you don't already have pip installed, run this command from your new virtual environment:
    ```
    python -m ensurepip --upgrade
    ```

4. Finally, use pip to install the required packages:
    ```
    pip install -r requirements.txt
    ```

5. You'll need to install the Fadecandy pre-compiled binaries according to [these instructions](https://learn.adafruit.com/led-art-with-fadecandy/installing-software). Note: you do not need to install Processing (although it's an awesome tool!), and you do not need to create your own configuration json file, as one is included in this project. You will, however, need to swap out the board serial number listed in [`ledconfig.json`](/ledconfig.json) with that of your own if you choose to use this board.

### Raspberry Pi Setup
For this project, we used a fresh Raspbian Lite install on a [Raspberry Pi 3 Model B+](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/). For downloads and more information, [see this page](https://www.raspberrypi.com/software/operating-systems/). Note that you may install the project in a virtual environment if you wish, however this may not be necessary if you only plan on using the Raspberry Pi to run this program.

1. (Optional) Install Xserver and your desktop environment of choice for easier working.
2. Run `sudo apt-get update` to get everything in tip-top shape.
3. Install `git`, so we can grab our code from GitHub.
    ```
    sudo apt install git
    ```
4. Clone the `surface-player` repository.
    ```
    git clone https://github.com/jasperkatzban/surface-player
    ```
5. Install `pip` so we can get Python packages.
    ```
    sudo apt install python3-pip
    ```
6. Install the `jackd` audio server.
    ```
    sudo apt install libjack-dev
    ```
    When prompted to bring realtime priorities to the audio group, select `yes`. The drawbacks of enabling realtime priorities are moot because you are simply running one script on a single-user setup.
    <br><br>
7. Install `portaudio`, `portmidi`, `libsndfile`, and `liblo` so `pyo` will install properly.
    ```
    sudo apt install portaudio19-dev libportmidi-dev libsndfile1-dev liblo-dev
    ```
8. Install `pyo` from source so it works with `jack`.
    In your home directory, ```git clone https://github.com/belangeo/pyo.git``` into a new directory.
    Then `cd` to this directory before running ```sudo python3 setup.py install --use-jack```.
    This will take a while (30-45 minutes) as it is installing from source.
9. Install `libatlas` to prevent an error when importing Numpy later.
    ```
    sudo apt install libatlas-base-dev
    ```
10. Install the Python packages from the `requirements_raspi.txt` file.
    ```
    python3 -m pip install -r requirements_raspi.txt
    ```
11. Install OpenCV and Numpy using `apt`.
    ```
    sudo apt install python3-opencv python3-numpy
    ```
    These are installed separately to ensure better installation speed. `pip` will try and fail to find pre-compiled wheels that work on Raspbian and will need to build from source, which takes multiple hours for packages as large as OpenCV and Numpy. `apt` is much faster.
12. Install the Fadecandy pre-compiled binaries according to [these instructions](https://learn.adafruit.com/1500-neopixel-led-curtain-with-raspberry-pi-fadecandy/fadecandy-server-setup). Note: you do not need to create your own configuration json file, as one is included in this project. You will, however, need to swap out the board serial number listed in [`ledconfig.json`](/ledconfig.json) with that of your own if you choose to use this board.

## Running the Code

### On your local machine
1. From a new terminal, navigate to the `bin` folder of your Fadecandy repo, and start the Fadecandy server with the provided `ledconfig.json` file. (Note that you may need to run a different version of the executable depending on your environment)
    ```
    cd [your-path-to-fadecandy]/bin
    fcserver-osx [your-path-to-this-repo]/ledconfig.json
    ```

3. In a new terminal, run the main app from the root directory:
    ```
    python3 src/surface_player.py
    ```

Run the main app from the root directory with the following command:
    ```
    python3 src/surface_player.py -h
    ```

This will show the allowed options and commands for running the program. For most local installations, passing the `-l` or `--local` argument should be sufficient.

### On a Raspberry Pi
1. To start the jack audio server, run:
    ```
    jackd -m -d alsa -d default
    ```
2. From a new terminal, start the Fadecandy server with the provided `ledconfig.json` file:
    ```
    cd [your-path-to-fadecandy]/bin
    fcserver-rpi [your-path-to-this-repo]/ledconfig.json
    ```

3. From yet another terminal, run the main app:
    ```
    python3 src/surface_player.py
    ```

## Software Design
Since this project interfaces between multiple inputs and outputs – a laser, motor, camera, speakers, and addressable LEDs – it made sense to split each of these modules into separate classes and call simpler update functions from a central executable.

### Main Executable
Each module is initialized and connected together in [`src/surface_player.py`](src/surface_player.py). When this file is run, it handles the following:

- argument parsing to support various features and options
- initialization of modules to control each physical component
- continuous looping to capture an image, process it, and send the processed data to the audio and LEDs modules
- shutdown of modules upon program quit

Modules can be found in the [`src/modules/`](src/modules/) directory. A brief overview of each module and how it interacts with the system is listed below. Note that helper functions and most internal functions are omitted here, but documented in their respective classes.

### Camera
The `Camera` module handles detection and isolation of the laser line from the camera's raw video feed, and generates a `profile` object based on the side profile of the object on the turn table. This profile is then passed to the `Audio` and `Leds`modules as input data for their respective operations.

- `capture_frame()` - captures an image from the camera
- `get_profile()` - generates a `profile` – a list of floats, from 0 to 1 representative of the the detected profile of the object on the turntable, as measured by the laser line shining on it
- `set_profile_size(profile_size)` - sets the desired output length of the `profile` object, which should be based on the audio buffer's length
- `show_frame()` - shows the current processed frame, including any processing and annotations to it

### Audio
The `Audio` module generates playable audio using the `pyo` server based on a profile generated by the `Camera` module. It converts the `profile` object into a wavetable, a playable sample which is looped as the program runs. It also applies audio effects to the generated signal.

- `set_samples_from_profile(profile)` - sets the current waveform to 
- `get_buffer_size()` - returns the current audio buffer size, used in sizing the `profile` object from the camera module

### Laser
The `Laser` module controls the laser diode, which is attached to a GPIO pin of the Raspberry Pi. When the program is initialized, the laser turns on; when it is quit the laser turns off.

- controls the laser via the `on()`, `off()`, and `toggle()` methods
- provides current laser state via the `is_lit()` method

### Motor
The `Motor` module handles control of the stepper motor. The motor begins rotation when the main executable is run.

- `start_spin()` - begins motor rotation in a separate thread
- `stop_spin()` - stops motor rotation, joining that thread with main
- `step(num_steps, backwards)` - steps the motor forward or backwards by `n` steps
- `release()` - releases the motor's hold on a specific position

### Leds
The `Leds` module handles control of the addressable LEDs mounted throughout the physical enclosure. 

- `method()` - brief description as it pertains to the rest of the software subsystem

Finally, various constants and macros are listed in [`src/utils/constants.py`](src/utils/constants.py).

## External Dependencies
The following are required to run this program. Note that requirements may already be satisfied and additional platform-specific dependencies may be required depending on your target environment.

### General Use
- [pip3](https://pypi.org/project/pip/)
- [Numpy](https://numpy.org)

### Camera & Image Processing
- [OpenCV](https://github.com/opencv/opencv)

### Audio
- [pyo](http://ajaxsoundstudio.com/software/pyo/)
- [portaudio](http://www.portaudio.com)
- [portmidi](https://github.com/mixxxdj/portmidi)
- [libsndfile](https://github.com/libsndfile/libsndfile)
- [liblo](https://github.com/radarsat1/liblo)
- [jack](https://jackaudio.org)

### Motor Control
- [Adafruit Motorkit](https://circuitpython.readthedocs.io/projects/motorkit/en/latest/)

### Laser Control
- [GPIOZero](https://gpiozero.readthedocs.io/en/stable/)

### Led Control
- [Fadecandy](https://github.com/scanlime/fadecandy)