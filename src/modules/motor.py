import threading
import logging
import time

from utils.constants import MOTOR_NUM_STEPS_REVOLUTION, MOTOR_STEP_DELAY_MS

logger = logging.getLogger(__name__)

try:
    from adafruit_motor import stepper as stepper
    from adafruit_motorkit import MotorKit
except:
    logger.warn('Unable to import motor libraries! Assuming program is not running on a raspberry pi.')

class Motor:
    """Handle controlling motor to turn turnable"""

    def __init__(self, env_raspi=True):
        self.env_raspi = env_raspi
        """Initializes motor object on motor shield"""
        logger.info('Initializing motor module!')
        if self.env_raspi:
            self.kit = MotorKit()

    def start_spin(self):
        """Start spinning (on separate thread)"""
        self.thread = threading.Thread(target=self.step_loop) # specify which thread to start
        # self.thread = threading.Thread(target=self.step)
        self.thread.start() # start it
        # self.thread.join()
    
    def stop_spin(self):
        """Stop spinning"""
        self.thread.join() # join thread with main process and kill it

    def step_loop(self):
        """Loops continuously and steps motor forward"""
        while True:
            self.step()
            # could also try only trigger stepping every so often
            # if int(time.time() * 1000) % 1000 == 0:
            #     logger.debug('Triggered motor movement cycle!')
            #     self.step(num_steps)
    
    def step_num(self, num_steps=5, backwards=False):
        """Move the motor a specified number of steps"""
        if self.env_raspi:
            for _ in range(num_steps):
                logger.debug('Steping Motor!')
                if backwards:
                    self.kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
                else:
                    self.kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
                time.sleep(MOTOR_STEP_DELAY_MS / 1000)

    def step(self, backwards=False):
        """Move the motor a specified number of steps"""
        logger.debug('Steping Motor!')
        if self.env_raspi:
            if backwards:
                self.kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
            else:
                self.kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
            time.sleep(MOTOR_STEP_DELAY_MS / 1000)
        
    def full_turn(self, backwards=False):
        """Moves the motor one revolution. Set `backwards` flag to change direction"""
        logger.debug('Starting full revolution of motor!')
        if self.env_raspi:
            self.step(num_steps=MOTOR_NUM_STEPS_REVOLUTION, backwards=backwards)
        logger.debug('Motor revolution complete!')

    def release(self):
        """Release motor hold"""
        logger.debug('Releasing motor hold!')
        if self.env_raspi:
            self.kit.stepper1.release()