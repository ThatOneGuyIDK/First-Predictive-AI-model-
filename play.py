#!/usr/bin/env python3
"""
Play script for testing trained models or manual control.
"""
import os
import sys
import argparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game.environment import Environment
from model.neural_network import CarNet
import torch


def play_manual():
    """Play the game with manual control."""
    print("=" * 50)
    print("Manual Control Mode")
    print("=" * 50)
    print("Controls:")
    print("  UP ARROW - Accelerate")
    print("  DOWN ARROW - Brake")
    print("  LEFT ARROW - Turn Left")
    print("  RIGHT ARROW - Turn Right")
    print("  SPACE - Pause/Resume")
    print("  S - Toggle sensor display")
    print("  ESC - Quit")
    print("=" * 50)
    
    env = Environment()
    cars = env.reset(num_cars=1)
    
    try:
        while True:
            # Manual control
            env.manual_control()
            
            # Step environment
            states, rewards, done = env.step()
            
            # Render
            car = cars[0]
            info_text = f"Speed: {car.speed:.1f} | Distance: {car.distance_traveled:.1f}"
            env.render()
            
            # Reset if car dies
            if done:
                print(f"Car crashed! Distance traveled: {car.distance_traveled:.1f}")
                cars = env.reset(num_cars=1)
    
    except KeyboardInterrupt:
        print("\n\nGame ended by user.")
    
    finally:
        env.close()


def play_ai(model_path):
    """Play the game with AI control."""
    print("=" * 50)
    print("AI Control Mode")
    print("=" * 50)
    print(f"Loading model: {model_path}")
    
    if not os.path.exists(model_path):
        print(f"Error: Model file not found: {model_path}")
        return
    
    # Load model
    network = CarNet()
    network.load_state_dict(torch.load(model_path))
    network.eval()
    
    print("Model loaded successfully!")
    print("\nControls:")
    print("  SPACE - Pause/Resume")
    print("  S - Toggle sensor display")
    print("  ESC - Quit")
    print("=" * 50)
    
    env = Environment()
    cars = env.reset(num_cars=1)
    car = cars[0]
    car.network = network
    
    try:
        while True:
            # Get action from network
            if car.alive:
                state = car.get_state()
                action = car.network.get_action(state)
            else:
                action = (False, False, False, False)
            
            # Step environment
            states, rewards, done = env.step([action])
            
            # Render
            env.render()
            
            # Reset if car dies
            if done:
                print(f"Car crashed! Distance traveled: {car.distance_traveled:.1f}")
                cars = env.reset(num_cars=1)
                car = cars[0]
                car.network = network
    
    except KeyboardInterrupt:
        print("\n\nGame ended by user.")
    
    finally:
        env.close()


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Play the self-driving car game"
    )
    parser.add_argument(
        '--mode',
        type=str,
        choices=['manual', 'ai'],
        default='manual',
        help='Play mode: manual or ai'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='models/best_model.pth',
        help='Path to trained model (for ai mode)'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'manual':
        play_manual()
    else:
        play_ai(args.model)


if __name__ == "__main__":
    main()
