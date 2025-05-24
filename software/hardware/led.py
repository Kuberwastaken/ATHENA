"""
LED Control Module for Project ATHENA

This module handles control of the LED feedback system.
"""

import time
import threading
import logging
from enum import Enum
import math

# Set up logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("led_control")

class LEDEffect(Enum):
    """Enum representing different LED effects."""
    SOLID = 0
    PULSE = 1
    SPIN = 2
    BREATHE = 3
    RAINBOW = 4
    PROGRESS = 5
    CUSTOM = 6

class LEDColor(Enum):
    """Common color presets."""
    OFF = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    TEAL = (0, 128, 128)

class LEDController:
    """
    Controller for the LED feedback system.
    
    This class provides an interface for controlling the LED ring or strip
    used for visual feedback in the ATHENA system.
    """
    
    def __init__(self, led_count=24, brightness=0.5, gpio_pin=18, simulation=False):
        """
        Initialize the LED controller.
        
        Args:
            led_count: Number of LEDs in the strip
            brightness: Initial brightness (0.0-1.0)
            gpio_pin: GPIO pin connected to the LED data line
            simulation: If True, runs in simulation mode without hardware
        """
        self.led_count = led_count
        self.brightness = max(0.0, min(1.0, brightness))  # Clamp to 0.0-1.0
        self.gpio_pin = gpio_pin
        self.simulation = simulation
        
        self.pixels = [(0, 0, 0)] * led_count  # RGB values for each LED
        
        self.current_effect = None
        self.effect_thread = None
        self.running = False
        
        self._setup_hardware()
        logger.info(f"LED controller initialized with {led_count} LEDs")
    
    def _setup_hardware(self):
        """Set up the LED hardware interface."""
        if self.simulation:
            logger.info("Running in simulation mode (no hardware)")
            return
            
        try:
            # This is a placeholder for actual hardware initialization
            # In a real implementation, this would use a library like rpi_ws281x
            logger.info("Initializing LED hardware...")
            # Example with rpi_ws281x (commented out since it's hardware-dependent):
            # import board
            # import neopixel
            # self.strip = neopixel.NeoPixel(
            #     board.D18, self.led_count, brightness=self.brightness, auto_write=False
            # )
            
            logger.info("LED hardware initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize LED hardware: {e}")
            logger.info("Falling back to simulation mode")
            self.simulation = True
    
    def set_pixel(self, index, color):
        """
        Set the color of a specific LED.
        
        Args:
            index: LED index (0 to led_count-1)
            color: RGB tuple (r, g, b) with values 0-255
        """
        if 0 <= index < self.led_count:
            self.pixels[index] = color
    
    def set_all(self, color):
        """
        Set all LEDs to the same color.
        
        Args:
            color: RGB tuple (r, g, b) with values 0-255
        """
        for i in range(self.led_count):
            self.pixels[i] = color
    
    def clear(self):
        """Turn off all LEDs."""
        self.set_all((0, 0, 0))
        self.update()
    
    def update(self):
        """Update the physical LED strip with current pixel values."""
        if self.simulation:
            # In simulation mode, just log the state
            # In a real application, this could drive a visualization
            return
            
        try:
            # This is a placeholder for actual hardware update
            # In a real implementation, this would update the physical LEDs
            # Example with rpi_ws281x:
            # for i, (r, g, b) in enumerate(self.pixels):
            #     self.strip[i] = (r, g, b)
            # self.strip.show()
            
            pass
            
        except Exception as e:
            logger.error(f"Error updating LEDs: {e}")
    
    def start_effect(self, effect, color=None, duration=None, speed=1.0):
        """
        Start an LED effect.
        
        Args:
            effect: LEDEffect enum value
            color: RGB tuple (r, g, b) or LEDColor enum
            duration: Effect duration in seconds (None for indefinite)
            speed: Effect speed multiplier
        """
        # Stop any current effect
        self.stop_effect()
        
        # Convert LEDColor enum to RGB tuple if needed
        if isinstance(color, LEDColor):
            color = color.value
            
        # Default to white if no color specified
        if color is None:
            color = (255, 255, 255)
        
        self.current_effect = effect
        self.running = True
        
        # Start the effect in a separate thread
        self.effect_thread = threading.Thread(
            target=self._run_effect,
            args=(effect, color, duration, speed)
        )
        self.effect_thread.daemon = True
        self.effect_thread.start()
        
        logger.info(f"Started LED effect: {effect.name}")
    
    def stop_effect(self):
        """Stop the current effect and turn off LEDs."""
        if self.running:
            self.running = False
            if self.effect_thread:
                self.effect_thread.join(timeout=1.0)
            self.clear()
            logger.info("Stopped LED effect")
    
    def set_brightness(self, brightness):
        """
        Set the LED brightness.
        
        Args:
            brightness: Brightness value (0.0-1.0)
        """
        self.brightness = max(0.0, min(1.0, brightness))  # Clamp to 0.0-1.0
        
        # Update hardware brightness if applicable
        if not self.simulation:
            # Example with rpi_ws281x:
            # self.strip.brightness = self.brightness
            pass
            
        logger.info(f"Brightness set to {self.brightness:.2f}")
    
    def _run_effect(self, effect, color, duration, speed):
        """
        Run the specified effect.
        
        Args:
            effect: LEDEffect enum value
            color: RGB tuple (r, g, b)
            duration: Effect duration in seconds (None for indefinite)
            speed: Effect speed multiplier
        """
        start_time = time.time()
        
        try:
            while self.running:
                # Check if duration has elapsed
                if duration is not None and time.time() - start_time > duration:
                    break
                
                # Run the appropriate effect
                if effect == LEDEffect.SOLID:
                    self._solid_effect(color)
                elif effect == LEDEffect.PULSE:
                    self._pulse_effect(color, speed)
                elif effect == LEDEffect.SPIN:
                    self._spin_effect(color, speed)
                elif effect == LEDEffect.BREATHE:
                    self._breathe_effect(color, speed)
                elif effect == LEDEffect.RAINBOW:
                    self._rainbow_effect(speed)
                elif effect == LEDEffect.PROGRESS:
                    progress = min(1.0, (time.time() - start_time) / (duration or 10.0))
                    self._progress_effect(color, progress)
                
                # Small delay to limit update rate
                time.sleep(0.01)
                
        except Exception as e:
            logger.error(f"Error in LED effect: {e}")
            
        finally:
            # Make sure LEDs are cleared when the effect ends
            if self.running:  # Only if not externally stopped
                self.clear()
            self.running = False
    
    def _solid_effect(self, color):
        """Solid color effect (no animation)."""
        self.set_all(color)
        self.update()
        time.sleep(0.1)  # Reduce update frequency for solid effect
    
    def _pulse_effect(self, color, speed):
        """Pulse all LEDs in unison."""
        t = time.time() * speed * 2
        pulse = (math.sin(t) + 1) / 2  # 0.0 to 1.0
        
        r, g, b = color
        scaled_color = (
            int(r * pulse),
            int(g * pulse),
            int(b * pulse)
        )
        
        self.set_all(scaled_color)
        self.update()
    
    def _spin_effect(self, color, speed):
        """Spin a dot around the LED ring."""
        t = time.time() * speed * 2
        position = int(t % self.led_count)
        
        # Clear all LEDs
        self.clear()
        
        # Set the moving dot
        self.set_pixel(position, color)
        
        # Optional: set a dimmer trail
        trail_length = 5
        for i in range(1, trail_length + 1):
            trail_pos = (position - i) % self.led_count
            r, g, b = color
            dimmed_color = (
                int(r * (trail_length - i) / (trail_length * 2)),
                int(g * (trail_length - i) / (trail_length * 2)),
                int(b * (trail_length - i) / (trail_length * 2))
            )
            self.set_pixel(trail_pos, dimmed_color)
        
        self.update()
    
    def _breathe_effect(self, color, speed):
        """Breathing effect (slow pulse)."""
        t = time.time() * speed
        # Use a smoother sine wave for breathing
        pulse = (math.sin(t) + 1) / 2  # 0.0 to 1.0
        
        # Apply a power curve to make the effect more natural
        pulse = pulse ** 2
        
        r, g, b = color
        scaled_color = (
            int(r * pulse),
            int(g * pulse),
            int(b * pulse)
        )
        
        self.set_all(scaled_color)
        self.update()
    
    def _rainbow_effect(self, speed):
        """Rainbow effect cycling through all hues."""
        t = time.time() * speed
        
        for i in range(self.led_count):
            # Calculate hue based on position and time
            hue = (i / self.led_count + t) % 1.0
            
            # Convert HSV to RGB (simplified)
            h = hue * 6
            c = 255
            x = int(255 * (1 - abs(h % 2 - 1)))
            
            if 0 <= h < 1:
                rgb = (c, x, 0)
            elif 1 <= h < 2:
                rgb = (x, c, 0)
            elif 2 <= h < 3:
                rgb = (0, c, x)
            elif 3 <= h < 4:
                rgb = (0, x, c)
            elif 4 <= h < 5:
                rgb = (x, 0, c)
            else:
                rgb = (c, 0, x)
                
            self.set_pixel(i, rgb)
            
        self.update()
    
    def _progress_effect(self, color, progress):
        """Show a progress indicator."""
        # Calculate how many LEDs to light up
        lit_count = int(progress * self.led_count)
        
        # Clear all LEDs first
        self.clear()
        
        # Light up the progress LEDs
        for i in range(lit_count):
            self.set_pixel(i, color)
            
        self.update()


# Example usage
if __name__ == "__main__":
    # Create LED controller with 24 LEDs in simulation mode
    led = LEDController(led_count=24, simulation=True)
    
    try:
        # Demonstrate various effects
        print("Demonstrating solid effect...")
        led.start_effect(LEDEffect.SOLID, LEDColor.BLUE)
        time.sleep(2)
        
        print("Demonstrating pulse effect...")
        led.start_effect(LEDEffect.PULSE, LEDColor.GREEN)
        time.sleep(5)
        
        print("Demonstrating spin effect...")
        led.start_effect(LEDEffect.SPIN, LEDColor.RED)
        time.sleep(5)
        
        print("Demonstrating breathe effect...")
        led.start_effect(LEDEffect.BREATHE, LEDColor.PURPLE)
        time.sleep(5)
        
        print("Demonstrating rainbow effect...")
        led.start_effect(LEDEffect.RAINBOW)
        time.sleep(5)
        
        print("Demonstrating progress effect...")
        led.start_effect(LEDEffect.PROGRESS, LEDColor.CYAN, duration=10)
        time.sleep(10)
        
    except KeyboardInterrupt:
        print("Interrupted")
        
    finally:
        led.stop_effect()
        print("LED effects stopped")
