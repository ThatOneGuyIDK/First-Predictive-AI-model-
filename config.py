"""
Configuration settings for the self-driving car project.
Modify these values to customize the training and game behavior.
"""

# Display settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Track settings
TRACK_WIDTH = 80  # Width of the track (half-width from center line)

# Car settings
CAR_MAX_SPEED = 10
CAR_ROTATION_SPEED = 5
CAR_ACCELERATION_RATE = 0.5
CAR_BRAKE_RATE = 0.8
CAR_FRICTION = 0.95

# Sensor settings
NUM_SENSORS = 5
SENSOR_LENGTH = 150
SENSOR_ANGLES = [-60, -30, 0, 30, 60]  # Degrees relative to car direction

# Neural network settings
INPUT_SIZE = NUM_SENSORS + 1  # Sensors + speed
HIDDEN_SIZE = 16
OUTPUT_SIZE = 4  # forward, brake, left, right

# Training settings
POPULATION_SIZE = 20
GENERATIONS = 50
MAX_TIME_PER_GENERATION = 30  # seconds
MUTATION_RATE = 0.1

# Fitness settings
DISTANCE_REWARD_WEIGHT = 0.1
TIME_REWARD_WEIGHT = 0.5
CRASH_PENALTY = -10

# Model save path
MODEL_DIR = 'models'
BEST_MODEL_PATH = f'{MODEL_DIR}/best_model.pth'
FINAL_MODEL_PATH = f'{MODEL_DIR}/final_model.pth'

# Colors (RGB)
TRACK_COLOR = (100, 100, 100)
BOUNDARY_COLOR = (255, 0, 0)
GRASS_COLOR = (34, 139, 34)
CAR_COLOR = (0, 0, 255)
SENSOR_COLOR = (255, 255, 0)
