"""
Track definition and management for the self-driving car game.
"""
import pygame
import math


class Track:
    """Defines the racing track with boundaries and checkpoints."""
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.track_color = (100, 100, 100)
        self.boundary_color = (255, 0, 0)
        self.grass_color = (34, 139, 34)
        
        # Define track as a list of waypoints (center line)
        self.waypoints = self._create_oval_track()
        
        # Track width (half-width from center)
        self.track_width = 80
        
    def _create_oval_track(self):
        """Create an oval track using waypoints."""
        waypoints = []
        center_x = self.width // 2
        center_y = self.height // 2
        radius_x = 250
        radius_y = 180
        
        # Create oval with 50 points
        for i in range(50):
            angle = (i / 50) * 2 * math.pi
            x = center_x + radius_x * math.cos(angle)
            y = center_y + radius_y * math.sin(angle)
            waypoints.append((x, y))
        
        return waypoints
    
    def draw(self, screen):
        """Draw the track on the screen."""
        # Fill background with grass
        screen.fill(self.grass_color)
        
        # Draw track surface
        if len(self.waypoints) > 2:
            # Draw inner track
            inner_points = []
            outer_points = []
            
            for i, point in enumerate(self.waypoints):
                # Calculate perpendicular direction
                next_point = self.waypoints[(i + 1) % len(self.waypoints)]
                dx = next_point[0] - point[0]
                dy = next_point[1] - point[1]
                length = math.sqrt(dx*dx + dy*dy)
                if length > 0:
                    dx /= length
                    dy /= length
                
                # Perpendicular vectors
                perp_x = -dy
                perp_y = dx
                
                inner_points.append((
                    point[0] + perp_x * self.track_width,
                    point[1] + perp_y * self.track_width
                ))
                outer_points.append((
                    point[0] - perp_x * self.track_width,
                    point[1] - perp_y * self.track_width
                ))
            
            # Draw track surface
            all_points = inner_points + outer_points[::-1]
            pygame.draw.polygon(screen, self.track_color, all_points)
            
            # Draw boundaries
            pygame.draw.lines(screen, self.boundary_color, True, inner_points, 3)
            pygame.draw.lines(screen, self.boundary_color, True, outer_points, 3)
    
    def is_on_track(self, x, y):
        """Check if a point is on the track."""
        # Find closest waypoint
        min_dist = float('inf')
        closest_idx = 0
        
        for i, waypoint in enumerate(self.waypoints):
            dist = math.sqrt((x - waypoint[0])**2 + (y - waypoint[1])**2)
            if dist < min_dist:
                min_dist = dist
                closest_idx = i
        
        # Check if within track width
        return min_dist <= self.track_width
    
    def get_start_position(self):
        """Get the starting position and angle for the car."""
        if len(self.waypoints) < 2:
            return self.width // 2, self.height // 2, 0
        
        # Start at first waypoint
        start_x, start_y = self.waypoints[0]
        
        # Calculate initial angle
        next_x, next_y = self.waypoints[1]
        angle = math.atan2(next_y - start_y, next_x - start_x)
        
        return start_x, start_y, math.degrees(angle)
