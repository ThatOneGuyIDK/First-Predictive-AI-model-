# Quick Start Guide

Get up and running with the self-driving car in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

If you have issues with torch, install it separately:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

## Step 2: Try Manual Control

First, try driving the car yourself to understand the game:

```bash
python play.py --mode manual
```

**Controls:**
- ⬆️ UP: Accelerate
- ⬇️ DOWN: Brake  
- ⬅️ LEFT: Turn left
- ➡️ RIGHT: Turn right
- SPACE: Pause
- S: Toggle sensors

Try to stay on the gray track! If you go off-track (into the green), the car crashes.

## Step 3: Train the AI

Now let the AI learn to drive:

```bash
python train.py
```

This will:
- Create 20 cars per generation
- Let them try to drive around the track
- Keep the best drivers and evolve them
- Save the best model to `models/best_model.pth`

**Training Tips:**
- Let it run for at least 10-20 generations to see improvement
- Press SPACE to pause and watch specific cars
- Press S to toggle sensor visualization
- The best fitness score will increase over time

## Step 4: Watch the AI Drive

After training, watch your AI drive:

```bash
python play.py --mode ai --model models/best_model.pth
```

## Understanding the Sensors

The car has 5 "radar" sensors:
- **Center (0°)**: Looks straight ahead
- **Left 30° and 60°**: Look to the left
- **Right 30° and 60°**: Look to the right

These sensors measure distance to the track edge. The neural network uses these distances to decide how to drive.

## Common Issues

### Black screen or frozen display
This can happen in some environments. The training is still working! Check the console output to see progress.

### Car immediately crashes
This is normal at first! The AI starts with random behaviors. After a few generations, you'll see improvement.

### Training is slow
- Reduce population size: Edit `train.py` and change `population_size=20` to `10`
- Reduce time per generation: Change `max_time=30` to `15`
- Close sensor visualization: Press `S` during training

## Next Steps

- **Modify the track**: Edit `src/game/track.py` to create different track shapes
- **Adjust fitness**: Edit the `_calculate_reward()` function in `src/game/environment.py`
- **Change network architecture**: Modify `src/model/neural_network.py` to add more layers
- **Increase population**: Train with more cars per generation for better results

## Tips for Better Results

1. **Train longer**: 50-100 generations often produces much better results
2. **Watch the sensors**: Toggle them on (press S) to understand what the car "sees"
3. **Manual baseline**: Try driving manually to get a fitness score to beat
4. **Incremental training**: Train for 20 generations, save, then train more on the same model

Enjoy watching your AI learn to drive! 🚗💨
