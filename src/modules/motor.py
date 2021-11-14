from gpiozero import Motor as m

GPIO_FORWARD_PIN = 4
GPIO_BACKWARD_PIN = 14
MOTOR_SPEED = 0.5

class Motor:
    """Handle controlling motor to turn turnable"""

    def __init__(self):
        self.motor = m(forward=GPIO_FORWARD_PIN, backward=GPIO_BACKWARD_PIN, pwm=True)

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