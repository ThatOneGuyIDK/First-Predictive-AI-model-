"""
Car class with physics simulation and sensor system.
"""
import pygame
import math
import numpy as np


class Car:
    """Represents a car with physics and sensors for self-driving."""
    
    def __init__(self, x, y, angle=0):
        self.x = x
        self.y = y
        self.angle = angle  # in degrees
        self.speed = 0
        self.acceleration = 0
        self.max_speed = 10
        self.rotation_speed = 5
        
        # Car dimensions
        self.width = 30
        self.height = 20
        
        # Physics
        self.friction = 0.95
        self.acceleration_rate = 0.5
        self.brake_rate = 0.8
        
        # Sensors (radar distances)
        self.num_sensors = 5
        self.sensor_length = 150
        self.sensor_angles = [-60, -30, 0, 30, 60]  # degrees relative to car
        self.sensor_readings = [self.sensor_length] * self.num_sensors
        
        # Status
        self.alive = True
        self.distance_traveled = 0
        self.time_alive = 0
        
        # Color
        self.color = (0, 0, 255)
        
    def update(self, dt, track):
        """Update car physics."""
        if not self.alive:
            return
        
        # Update speed with friction
        self.speed *= self.friction
        self.speed += self.acceleration
        self.speed = max(-self.max_speed/2, min(self.speed, self.max_speed))
        
        # Update position
        rad_angle = math.radians(self.angle)
        dx = math.cos(rad_angle) * self.speed * dt
        dy = math.sin(rad_angle) * self.speed * dt
        
        self.x += dx
        self.y += dy
        self.distance_traveled += abs(self.speed) * dt
        self.time_alive += dt
        
        # Check if still on track
        if not track.is_on_track(self.x, self.y):
            self.alive = False
        
        # Update sensors
        self.update_sensors(track)
        
    def update_sensors(self, track):
        """Update sensor readings by raycasting."""
        for i, sensor_angle in enumerate(self.sensor_angles):
            total_angle = self.angle + sensor_angle
            rad_angle = math.radians(total_angle)
            
            # Raycast to find distance to track boundary
            distance = self._raycast(
                self.x, self.y, 
                math.cos(rad_angle), 
                math.sin(rad_angle), 
                track
            )
            self.sensor_readings[i] = distance
    
    def _raycast(self, start_x, start_y, dx, dy, track):
        """Cast a ray and return distance to track boundary."""
        max_distance = self.sensor_length
        step_size = 5
        
        for distance in range(0, max_distance, step_size):
            x = start_x + dx * distance
            y = start_y + dy * distance
            
            # Check if out of bounds
            if x < 0 or x >= track.width or y < 0 or y >= track.height:
                return distance
            
            # Check if off track
            if not track.is_on_track(x, y):
                return distance
        
        return max_distance
    
    def accelerate(self):
        """Apply acceleration."""
        self.acceleration = self.acceleration_rate
    
    def brake(self):
        """Apply brakes."""
        self.acceleration = -self.brake_rate
    
    def turn_left(self, dt):
        """Turn the car left."""
        self.angle -= self.rotation_speed * (abs(self.speed) / self.max_speed) * dt * 10
    
    def turn_right(self, dt):
        """Turn the car right."""
        self.angle += self.rotation_speed * (abs(self.speed) / self.max_speed) * dt * 10
    
    def get_state(self):
        """Get the current state for neural network input."""
        # Normalize sensor readings
        normalized_sensors = [r / self.sensor_length for r in self.sensor_readings]
        
        # Normalize speed
        normalized_speed = self.speed / self.max_speed
        
        return np.array(normalized_sensors + [normalized_speed], dtype=np.float32)
    
    def draw(self, screen):
        """Draw the car and sensors."""
        if not self.alive:
            return
        
        # Draw sensors
        for i, sensor_angle in enumerate(self.sensor_angles):
            total_angle = self.angle + sensor_angle
            rad_angle = math.radians(total_angle)
            
            distance = self.sensor_readings[i]
            end_x = self.x + math.cos(rad_angle) * distance
            end_y = self.y + math.sin(rad_angle) * distance
            
            # Color based on distance
            color_intensity = int(255 * (1 - distance / self.sensor_length))
            color = (255, color_intensity, 0)
            
            pygame.draw.line(screen, color, 
                           (int(self.x), int(self.y)), 
                           (int(end_x), int(end_y)), 1)
        
        # Draw car body
        rad_angle = math.radians(self.angle)
        
        # Calculate car corners
        corners = []
        for dx, dy in [(-self.height/2, -self.width/2), 
                       (self.height/2, -self.width/2),
                       (self.height/2, self.width/2), 
                       (-self.height/2, self.width/2)]:
            rotated_x = dx * math.cos(rad_angle) - dy * math.sin(rad_angle)
            rotated_y = dx * math.sin(rad_angle) + dy * math.cos(rad_angle)
            corners.append((self.x + rotated_x, self.y + rotated_y))
        
        pygame.draw.polygon(screen, self.color, corners)
        
        # Draw direction indicator
        front_x = self.x + math.cos(rad_angle) * self.height
        front_y = self.y + math.sin(rad_angle) * self.height
        pygame.draw.circle(screen, (255, 255, 0), 
                         (int(front_x), int(front_y)), 3)
    
    def reset(self, x, y, angle):
        """Reset the car to initial position."""
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 0
        self.acceleration = 0
        self.alive = True
        self.distance_traveled = 0
        self.time_alive = 0
        self.sensor_readings = [self.sensor_length] * self.num_sensors
