"""
Game environment for training and playing the self-driving car.
"""
import pygame
import sys
from .track import Track
from .car import Car


class Environment:
    """Game environment manager."""
    
    def __init__(self, width=800, height=600, fps=60):
        """Initialize the game environment."""
        pygame.init()
        
        self.width = width
        self.height = height
        self.fps = fps
        
        # Create display
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Self-Driving Car Training")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Create track
        self.track = Track(width, height)
        
        # Initialize cars list (for multiple cars in training)
        self.cars = []
        
        self.paused = False
        self.show_sensors = True
        
    def reset(self, num_cars=1):
        """Reset the environment with new cars."""
        self.cars = []
        start_x, start_y, start_angle = self.track.get_start_position()
        
        for _ in range(num_cars):
            car = Car(start_x, start_y, start_angle)
            self.cars.append(car)
        
        return self.cars
    
    def step(self, actions=None):
        """
        Perform one step of the simulation.
        
        Args:
            actions: List of actions for each car (optional)
        
        Returns:
            tuple: (states, rewards, done)
        """
        dt = 1.0 / self.fps
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_s:
                    self.show_sensors = not self.show_sensors
        
        if not self.paused:
            # Update cars
            for i, car in enumerate(self.cars):
                if car.alive:
                    # Apply actions if provided
                    if actions and i < len(actions):
                        action = actions[i]
                        if action[0]:  # accelerate
                            car.accelerate()
                        if action[1]:  # brake
                            car.brake()
                        if action[2]:  # turn left
                            car.turn_left(dt)
                        if action[3]:  # turn right
                            car.turn_right(dt)
                    
                    car.update(dt, self.track)
        
        # Get states and rewards
        states = [car.get_state() for car in self.cars]
        rewards = [self._calculate_reward(car) for car in self.cars]
        done = all(not car.alive for car in self.cars)
        
        return states, rewards, done
    
    def _calculate_reward(self, car):
        """Calculate reward for a car."""
        if not car.alive:
            return -10
        
        # Reward based on distance traveled and time alive
        reward = car.distance_traveled * 0.1 + car.time_alive * 0.5
        
        return reward
    
    def render(self, generation=None, best_fitness=None, alive_count=None):
        """Render the environment."""
        # Draw track
        self.track.draw(self.screen)
        
        # Draw cars
        for car in self.cars:
            if self.show_sensors:
                car.draw(self.screen)
            else:
                # Draw simplified car without sensors
                if car.alive:
                    pygame.draw.circle(self.screen, car.color, 
                                     (int(car.x), int(car.y)), 10)
        
        # Draw info
        y_offset = 10
        
        if generation is not None:
            text = self.font.render(f"Generation: {generation}", True, (255, 255, 255))
            self.screen.blit(text, (10, y_offset))
            y_offset += 40
        
        if best_fitness is not None:
            text = self.small_font.render(f"Best Fitness: {best_fitness:.2f}", 
                                         True, (255, 255, 255))
            self.screen.blit(text, (10, y_offset))
            y_offset += 30
        
        if alive_count is not None:
            text = self.small_font.render(f"Alive: {alive_count}/{len(self.cars)}", 
                                         True, (255, 255, 255))
            self.screen.blit(text, (10, y_offset))
            y_offset += 30
        
        # Show controls
        controls = [
            "SPACE: Pause/Resume",
            "S: Toggle Sensors",
            "ESC: Quit"
        ]
        
        y_control = self.height - 90
        for control in controls:
            text = self.small_font.render(control, True, (255, 255, 255))
            self.screen.blit(text, (10, y_control))
            y_control += 25
        
        if self.paused:
            text = self.font.render("PAUSED", True, (255, 255, 0))
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(text, text_rect)
        
        pygame.display.flip()
        self.clock.tick(self.fps)
    
    def manual_control(self):
        """Allow manual control of the first car."""
        if not self.cars:
            return
        
        car = self.cars[0]
        keys = pygame.key.get_pressed()
        dt = 1.0 / self.fps
        
        car.acceleration = 0
        
        if keys[pygame.K_UP]:
            car.accelerate()
        if keys[pygame.K_DOWN]:
            car.brake()
        if keys[pygame.K_LEFT]:
            car.turn_left(dt)
        if keys[pygame.K_RIGHT]:
            car.turn_right(dt)
    
    def close(self):
        """Close the environment."""
        pygame.quit()
