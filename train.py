#!/usr/bin/env python3
"""
Training script for the self-driving car using genetic algorithm.
"""
import os
import sys
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game.environment import Environment
from model.neural_network import GeneticAlgorithm


def train(generations=100, population_size=20, max_time=30):
    """
    Train the self-driving car using genetic algorithm.
    
    Args:
        generations: Number of generations to train
        population_size: Number of cars per generation
        max_time: Maximum time (seconds) per generation
    """
    print("=" * 50)
    print("Self-Driving Car Training")
    print("=" * 50)
    print(f"Generations: {generations}")
    print(f"Population: {population_size}")
    print(f"Max time per generation: {max_time}s")
    print("\nControls:")
    print("  SPACE - Pause/Resume")
    print("  S - Toggle sensor display")
    print("  ESC - Quit")
    print("=" * 50)
    
    # Create environment
    env = Environment()
    
    # Create genetic algorithm
    ga = GeneticAlgorithm(population_size=population_size)
    
    # Training loop
    best_fitness_ever = 0
    
    try:
        for gen in range(generations):
            print(f"\n--- Generation {gen + 1}/{generations} ---")
            
            # Reset environment with population
            cars = env.reset(num_cars=population_size)
            
            # Assign neural networks to cars
            for i, car in enumerate(cars):
                car.network = ga.population[i]
            
            # Simulate generation
            fitness_scores = np.zeros(population_size)
            frame_count = 0
            max_frames = max_time * env.fps
            
            while frame_count < max_frames:
                # Get actions from neural networks
                actions = []
                for i, car in enumerate(cars):
                    if car.alive:
                        state = car.get_state()
                        action = car.network.get_action(state)
                        actions.append(action)
                    else:
                        actions.append((False, False, False, False))
                
                # Step environment
                states, rewards, done = env.step(actions)
                
                # Update fitness scores
                for i, reward in enumerate(rewards):
                    fitness_scores[i] = reward
                
                # Render
                alive_count = sum(1 for car in cars if car.alive)
                current_best = np.max(fitness_scores)
                env.render(
                    generation=gen + 1,
                    best_fitness=current_best,
                    alive_count=alive_count
                )
                
                frame_count += 1
                
                # Early stop if all cars are dead
                if done:
                    break
            
            # Calculate final fitness
            best_fitness = np.max(fitness_scores)
            avg_fitness = np.mean(fitness_scores)
            
            print(f"Best Fitness: {best_fitness:.2f}")
            print(f"Average Fitness: {avg_fitness:.2f}")
            
            # Save best model if improved
            if best_fitness > best_fitness_ever:
                best_fitness_ever = best_fitness
                print(f"New best model! Saving...")
                if not os.path.exists('models'):
                    os.makedirs('models')
                ga.save_best(fitness_scores, 'models/best_model.pth')
            
            # Evolve population
            ga.evolve(fitness_scores)
    
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user.")
    
    finally:
        # Save final model
        print("\nSaving final model...")
        if not os.path.exists('models'):
            os.makedirs('models')
        ga.save_best(fitness_scores, 'models/final_model.pth')
        
        print(f"\nTraining complete!")
        print(f"Best fitness achieved: {best_fitness_ever:.2f}")
        print(f"Models saved in 'models/' directory")
        
        env.close()


if __name__ == "__main__":
    train(generations=50, population_size=20, max_time=30)
