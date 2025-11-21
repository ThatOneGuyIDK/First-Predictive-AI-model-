"""
Neural network model for the self-driving car.
"""
import torch
import torch.nn as nn
import numpy as np


class CarNet(nn.Module):
    """Neural network for controlling the car."""
    
    def __init__(self, input_size=6, hidden_size=16, output_size=4):
        """
        Initialize the neural network.
        
        Args:
            input_size: Number of inputs (5 sensors + 1 speed)
            hidden_size: Number of neurons in hidden layers
            output_size: Number of outputs (4 actions: forward, brake, left, right)
        """
        super(CarNet, self).__init__()
        
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        """Forward pass through the network."""
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.sigmoid(self.fc3(x))
        return x
    
    def get_action(self, state):
        """
        Get action from state.
        
        Returns:
            tuple: (accelerate, brake, turn_left, turn_right) as booleans
        """
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            output = self.forward(state_tensor)
            output = output.squeeze().numpy()
            
            # Threshold for actions
            threshold = 0.5
            actions = output > threshold
            
            return tuple(actions)
    
    def mutate(self, mutation_rate=0.1):
        """
        Mutate the network weights for genetic algorithm.
        
        Args:
            mutation_rate: Probability of mutating each weight
        """
        with torch.no_grad():
            for param in self.parameters():
                if np.random.random() < mutation_rate:
                    # Add random noise to weights
                    noise = torch.randn_like(param) * 0.5
                    param.add_(noise)
    
    def clone(self):
        """Create a copy of this network."""
        clone = CarNet()
        clone.load_state_dict(self.state_dict())
        return clone


class GeneticAlgorithm:
    """Genetic algorithm for training the neural network."""
    
    def __init__(self, population_size=20, mutation_rate=0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = [CarNet() for _ in range(population_size)]
        self.generation = 0
        
    def evolve(self, fitness_scores):
        """
        Evolve the population based on fitness scores.
        
        Args:
            fitness_scores: List of fitness scores for each individual
        """
        # Sort population by fitness
        sorted_indices = np.argsort(fitness_scores)[::-1]
        
        # Keep top performers
        elite_count = self.population_size // 4
        new_population = []
        
        # Elite selection
        for i in range(elite_count):
            idx = sorted_indices[i]
            new_population.append(self.population[idx].clone())
        
        # Breed new individuals
        while len(new_population) < self.population_size:
            # Select parents from top half
            parent1_idx = sorted_indices[np.random.randint(0, self.population_size // 2)]
            parent2_idx = sorted_indices[np.random.randint(0, self.population_size // 2)]
            
            # Create child (clone one parent and mutate)
            child = self.population[parent1_idx].clone()
            child.mutate(self.mutation_rate)
            
            new_population.append(child)
        
        self.population = new_population
        self.generation += 1
    
    def get_best_network(self, fitness_scores):
        """Get the best performing network."""
        best_idx = np.argmax(fitness_scores)
        return self.population[best_idx]
    
    def save_best(self, fitness_scores, path):
        """Save the best network to file."""
        best_network = self.get_best_network(fitness_scores)
        torch.save(best_network.state_dict(), path)
    
    def load_best(self, path):
        """Load a saved network."""
        network = CarNet()
        network.load_state_dict(torch.load(path))
        return network
