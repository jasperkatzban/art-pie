# Surface Player
Final project for Principles of Integrated Engineering at Olin College

## Setup
It's recommended that you run this project from a python virtual environment to avoid any conflicts with your system's python installation.

You can setup your virtual environment by running the following in the root directory:

```python3 -m venv .venv```

Next, activate the environment:

```source .venv/bin/activate```

Your command prompt should now look something like this:

```(.venv) $```

If you don't already have pip installed, run this command from your new virtual environment:

`python -m ensurepip --upgrade`

Finally, use pip to install the required packages:

```pip install -r requirements.txt```

## Running the Code
Run the main app from the root directory with the following command:

```python3 src/surface_player.py```

### Testing Laser Tracking
To test the laser tracker script, run the following from the root directory:

```$ python3 tests/track_laser.py```