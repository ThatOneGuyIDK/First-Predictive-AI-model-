# Architecture Overview

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Self-Driving Car System                  │
└─────────────────────────────────────────────────────────────┘

┌───────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│   Game Engine     │      │  Neural Network   │      │ Training System  │
│   (pygame)        │◄────►│   (PyTorch)      │◄────►│  (Genetic Algo)  │
└───────────────────┘      └──────────────────┘      └──────────────────┘
         │                          │                          │
         │                          │                          │
         ▼                          ▼                          ▼
┌─────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  Track & Car    │      │  Decision Making  │      │  Evolution       │
│  Physics        │      │  (4 outputs)      │      │  (Population)    │
└─────────────────┘      └──────────────────┘      └──────────────────┘
```

## Data Flow

### Training Mode
```
1. Initialize Population (20 cars with random neural networks)
                    ↓
2. Simulate Generation (all cars drive simultaneously)
                    ↓
3. For each car:
   ┌──────────────────────────────────────────────┐
   │  Sensors → Neural Network → Actions → Update │
   └──────────────────────────────────────────────┘
                    ↓
4. Calculate Fitness (distance + time - crashes)
                    ↓
5. Evolution:
   - Keep top 25% performers (Elite)
   - Breed new individuals by mutation
   - Replace population
                    ↓
6. Repeat for N generations
```

### Play Mode
```
1. Load trained model
        ↓
2. Game Loop:
   ┌────────────────────────────────────────┐
   │ Sensors → Neural Network → Actions     │
   │             ↓                          │
   │    Update Car → Check Collision        │
   │             ↓                          │
   │         Render Scene                   │
   └────────────────────────────────────────┘
```

## Neural Network Architecture

```
Input Layer (6 neurons)
    ├─ Sensor 1 (-60°)    ─┐
    ├─ Sensor 2 (-30°)    ─┤
    ├─ Sensor 3 (0°)      ─┤──► Hidden Layer 1 (16 neurons, ReLU)
    ├─ Sensor 4 (30°)     ─┤           ↓
    ├─ Sensor 5 (60°)     ─┤   Hidden Layer 2 (16 neurons, ReLU)
    └─ Current Speed      ─┘           ↓
                                Output Layer (4 neurons, Sigmoid)
                                    ├─ Accelerate (0-1)
                                    ├─ Brake (0-1)
                                    ├─ Turn Left (0-1)
                                    └─ Turn Right (0-1)
```

## Sensor System

```
        Car Direction →
              ↑
             ╱│╲
        -60° │ │ 60°
           ╱ │ │ ╲
      -30°   │ │   30°
            ╱│ │ ╲
           │ │ │ │ │
           └─┴─┴─┴─┘
             Car

Each sensor:
- Casts a ray in its direction
- Measures distance to track boundary
- Returns normalized value (0-1)
- Shorter distance = closer to boundary
```

## Car Physics

```
Movement:
  velocity = speed × direction
  position += velocity × dt
  speed *= friction (0.95)

Steering:
  angle += rotation_speed × (speed/max_speed) × input
  
Actions:
  ┌─────────────┬──────────────────────┐
  │ Action      │ Effect               │
  ├─────────────┼──────────────────────┤
  │ Accelerate  │ speed += 0.5         │
  │ Brake       │ speed -= 0.8         │
  │ Turn Left   │ angle -= rotation°   │
  │ Turn Right  │ angle += rotation°   │
  └─────────────┴──────────────────────┘
```

## Genetic Algorithm

```
Generation N:
    Population (20 individuals)
          ↓
    Evaluate Fitness
          ↓
    Sort by Performance
          ↓
    ┌───────────────────┐
    │ Elite (top 25%)   │ ──→ Keep unchanged
    └───────────────────┘
          ↓
    ┌───────────────────┐
    │ Selection         │ ──→ Choose parents from top 50%
    └───────────────────┘
          ↓
    ┌───────────────────┐
    │ Mutation          │ ──→ Add random noise to weights
    └───────────────────┘      (10% probability per weight)
          ↓
    Generation N+1

Fitness Function:
    fitness = (distance × 0.1) + (time × 0.5) - (10 if crashed)
```

## File Structure

```
src/
├── game/
│   ├── car.py           # Car physics, sensors, state
│   ├── track.py         # Track generation, collision detection
│   └── environment.py   # Game loop, rendering, event handling
│
└── model/
    └── neural_network.py # Neural network, genetic algorithm

Scripts:
├── train.py             # Training loop
├── play.py              # Play/test interface
├── test_setup.py        # Validation script
└── config.py            # Configuration settings
```

## Key Classes

### Car
- **Properties**: position, angle, speed, sensors
- **Methods**: update(), get_state(), accelerate(), brake(), turn()
- **Sensors**: 5 raycasts for distance measurement

### Track
- **Properties**: waypoints, boundaries, width
- **Methods**: draw(), is_on_track(), get_start_position()

### Environment
- **Properties**: screen, track, cars, clock
- **Methods**: reset(), step(), render(), manual_control()

### CarNet (Neural Network)
- **Properties**: layers (fc1, fc2, fc3)
- **Methods**: forward(), get_action(), mutate(), clone()

### GeneticAlgorithm
- **Properties**: population, generation, mutation_rate
- **Methods**: evolve(), get_best_network(), save_best()

## Performance Considerations

- **Parallel Simulation**: All cars in a generation run simultaneously
- **Efficient Collision**: Simple distance-to-waypoint calculation
- **Early Termination**: Generation ends when all cars crash
- **Model Saving**: Only best model saved, not entire population

## Customization Points

1. **Track Shape**: Modify `_create_oval_track()` in `track.py`
2. **Fitness Function**: Edit `_calculate_reward()` in `environment.py`
3. **Network Architecture**: Change layers in `CarNet.__init__()`
4. **Sensor Configuration**: Adjust angles and count in `car.py`
5. **Training Parameters**: Modify values in `config.py`
