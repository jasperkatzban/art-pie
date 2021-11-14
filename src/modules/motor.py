from gpiozero import Motor as m
from utils.constants import GPIO_MOTOR_FORWARD, GPIO_MOTOR_BACKWARD, MOTOR_SPEED

class Motor:
    """Handle controlling motor to turn turnable"""

    def __init__(self):
        self.motor = m(forward=GPIO_FORWARD, backward=GPIO_BACKWARD, pwm=True)

    def start(self):
        """Start turntable motor"""
        # TODO: smooth ramp up speed
        self.motor.forward(MOTOR_SPEED)

    def stop(self):
        """Start turntable motor"""
        # TODO: smooth ramp down speed
        self.motor.stop()
        

    def is_active(self):
        """Check if motor is active"""
        return self.motor.is_active