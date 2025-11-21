# Self-Driving Car ML Project

This is my go at learning machine learning by building a self-driving car simulation!

## Overview

This project implements a self-driving car that learns to navigate a race track using a genetic algorithm and neural networks. The car uses sensors (like radar) to detect the track boundaries and learns optimal driving behavior through evolutionary training.

## Features

- **Racing Game Environment**: Built with Pygame, featuring an oval track with realistic boundaries
- **Car Physics**: Realistic car movement with acceleration, braking, friction, and steering
- **Sensor System**: 5 distance sensors (radar) to detect track boundaries
- **Neural Network**: Feedforward neural network that controls the car based on sensor inputs
- **Genetic Algorithm**: Population-based training that evolves better drivers over generations
- **Manual Control**: Play the game yourself to test the track
- **AI Control**: Watch trained models drive autonomously

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ThatOneGuyIDK/First-Predictive-AI-model-.git
cd First-Predictive-AI-model-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Training the Model

Train a new model using the genetic algorithm:

```bash
python train.py
```

The training will:
- Create a population of 20 cars
- Simulate each generation for up to 30 seconds
- Evolve the population based on fitness (distance traveled + time alive)
- Save the best model to `models/best_model.pth`

Controls during training:
- `SPACE` - Pause/Resume
- `S` - Toggle sensor visualization
- `ESC` - Quit (saves final model)

### Playing Manually

Test the track yourself with manual controls:

```bash
python play.py --mode manual
```

Controls:
- `UP ARROW` - Accelerate
- `DOWN ARROW` - Brake
- `LEFT ARROW` - Turn Left
- `RIGHT ARROW` - Turn Right
- `SPACE` - Pause/Resume
- `S` - Toggle sensor display

### Watching the AI Drive

Watch a trained model drive:

```bash
python play.py --mode ai --model models/best_model.pth
```

## Project Structure

```
.
├── src/
│   ├── game/
│   │   ├── car.py          # Car physics and sensors
│   │   ├── track.py        # Track definition
│   │   └── environment.py  # Game environment manager
│   └── model/
│       └── neural_network.py  # Neural network and genetic algorithm
├── train.py                # Training script
├── play.py                 # Play/test script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## How It Works

### The Car

Each car has:
- 5 distance sensors at different angles (-60°, -30°, 0°, 30°, 60°)
- Speed and acceleration physics
- Collision detection with track boundaries

### The Neural Network

- **Input**: 6 values (5 sensor readings + current speed)
- **Hidden Layers**: 2 layers with 16 neurons each
- **Output**: 4 actions (accelerate, brake, turn left, turn right)
- **Activation**: ReLU for hidden layers, Sigmoid for output

### The Genetic Algorithm

1. **Initialize**: Create a population of random neural networks
2. **Simulate**: Let each car drive until it crashes or time runs out
3. **Evaluate**: Calculate fitness based on distance traveled and survival time
4. **Select**: Keep the top 25% performers
5. **Breed**: Create new individuals by mutating top performers
6. **Repeat**: Continue for multiple generations

### Fitness Function

```
fitness = distance_traveled × 0.1 + time_alive × 0.5 - 10 (if crashed)
```

## Tips for Better Training

1. **Longer training**: Increase the number of generations
2. **Larger population**: More diversity can help find better solutions
3. **Adjust mutation rate**: Balance between exploration and exploitation
4. **Modify fitness function**: Reward staying on track or completing laps

## Future Improvements

- [ ] Add checkpoints for lap completion
- [ ] Implement multiple track layouts
- [ ] Add obstacles and other cars
- [ ] Use reinforcement learning (Q-learning, PPO)
- [ ] Add turbo/power-ups
- [ ] Create a more complex neural network architecture

## Requirements

- Python 3.7+
- pygame 2.5.2
- numpy 1.24.3
- torch 2.1.0
- matplotlib 3.7.2

## License

This project is for educational purposes.

## Acknowledgments

This project was created to learn machine learning fundamentals through a fun, visual application!
