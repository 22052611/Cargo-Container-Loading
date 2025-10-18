"""
Evolutionary Algorithm implementation for cargo container loading
"""

import random
import time
from solution import Solution

class EvolutionaryAlgorithm:
    """
    Genetic Algorithm for solving the cargo container loading problem
    """
    
    def __init__(self, container, cylinders, population_size=50, generations=200, 
                 crossover_rate=0.8, mutation_rate=0.2, elitism_rate=0.1):
        """
        Initialize the evolutionary algorithm
        
        Args:
            container (Container): The container to pack into
            cylinders (list): List of cylinders to pack
            population_size (int): Size of the population
            generations (int): Number of generations to run
            crossover_rate (float): Probability of crossover
            mutation_rate (float): Probability of mutation
            elitism_rate (float): Fraction of best solutions to preserve
        """
        self.container = container
        self.cylinders = cylinders
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism_rate = elitism_rate
        
        # Calculate elitism count
        self.elitism_count = max(1, int(population_size * elitism_rate))
        
        # Initialize population
        self.population = []
        self.best_solution = None
        self.best_fitness = float('inf')
        self.generation_stats = []
        
        # Local search parameters
        self.local_search_prob = 0.1
        self.local_search_iterations = 5
        
    def initialize_population(self):
        """Initialize the population with random solutions"""
        self.population = []
        
        for _ in range(self.population_size):
            solution = Solution(self.container, self.cylinders)
            solution.decode_and_evaluate()
            self.population.append(solution)
        
        # Find initial best solution
        self._update_best_solution()
    
    def _update_best_solution(self):
        """Update the best solution found so far"""
        for solution in self.population:
            if solution.fitness < self.best_fitness:
                self.best_fitness = solution.fitness
                self.best_solution = solution
    
    def selection(self):
        """
        Select parents for the next generation using tournament selection
        
        Returns:
            list: Selected parent solutions
        """
        selected = []
        
        for _ in range(self.population_size - self.elitism_count):
            # Tournament selection
            tournament_size = 3
            tournament = random.sample(self.population, tournament_size)
            winner = min(tournament, key=lambda x: x.fitness)
            selected.append(winner)
        
        return selected
    
    def crossover(self, parent1, parent2):
        """
        Perform crossover between two parents
        
        Args:
            parent1 (Solution): First parent
            parent2 (Solution): Second parent
            
        Returns:
            tuple: Two child solutions
        """
        if random.random() < self.crossover_rate:
            child1 = parent1.crossover(parent2)
            child2 = parent2.crossover(parent1)
        else:
            child1 = Solution(self.container, self.cylinders, parent1.permutation[:])
            child2 = Solution(self.container, self.cylinders, parent2.permutation[:])
            child1.decode_and_evaluate()
            child2.decode_and_evaluate()
        
        return child1, child2
    
    def mutate(self, solution):
        """
        Apply mutation to a solution
        
        Args:
            solution (Solution): Solution to mutate
        """
        solution.mutate(self.mutation_rate)
        solution.decode_and_evaluate()
    
    def local_search(self, solution):
        """
        Apply local search to improve a solution
        
        Args:
            solution (Solution): Solution to improve
        """
        if not solution.valid:
            return
        
        # Try different local search operations
        for _ in range(self.local_search_iterations):
            # Create a copy of the current solution
            original_fitness = solution.fitness
            original_permutation = solution.permutation[:]
            
            # Try swap mutation
            i, j = random.sample(range(len(solution.permutation)), 2)
            solution.permutation[i], solution.permutation[j] = solution.permutation[j], solution.permutation[i]
            solution.decode_and_evaluate()
            
            # Keep the improvement
            if solution.fitness < original_fitness:
                continue
            else:
                # Revert if no improvement
                solution.permutation = original_permutation
                solution.decode_and_evaluate()
    
    def create_new_generation(self):
        """Create a new generation from the current population"""
        # Sort population by fitness
        self.population.sort(key=lambda x: x.fitness)
        
        # Elitism: keep best solutions
        new_population = self.population[:self.elitism_count]
        
        # Selection
        selected_parents = self.selection()
        
        # Crossover and mutation
        while len(new_population) < self.population_size:
            # Select two parents
            parent1, parent2 = random.sample(selected_parents, 2)
            
            # Create children
            child1, child2 = self.crossover(parent1, parent2)
            
            # Apply mutation
            self.mutate(child1)
            self.mutate(child2)
            
            # Apply local search with probability
            if random.random() < self.local_search_prob:
                self.local_search(child1)
            if random.random() < self.local_search_prob:
                self.local_search(child2)
            
            # Add to new population
            new_population.extend([child1, child2])
            
            # Ensure we don't exceed population size
            if len(new_population) > self.population_size:
                new_population = new_population[:self.population_size]
                break
        
        self.population = new_population
        self._update_best_solution()
    
    def run(self):
        """
        Run the evolutionary algorithm
        
        Returns:
            Solution: Best solution found
        """
        print(f"Running EA with population_size={self.population_size}, generations={self.generations}")
        
        # Initialize population
        self.initialize_population()
        
        print(f"Initial best fitness: {self.best_fitness:.6f}")
        
        # Evolution loop
        for generation in range(self.generations):
            # Create new generation
            self.create_new_generation()
            
            # Record statistics
            avg_fitness = sum(s.fitness for s in self.population) / len(self.population)
            best_fitness = self.best_fitness
            
            self.generation_stats.append({
                'generation': generation,
                'avg_fitness': avg_fitness,
                'best_fitness': best_fitness
            })
            
            # Print progress
            if generation % 10 == 0:
                print(f"Generation {generation}: Best = {best_fitness:.6f}, Avg = {avg_fitness:.6f}")
            
            # Early stopping if perfect solution found
            if self.best_fitness < 1e-6:
                print(f"Perfect solution found at generation {generation}")
                break
        
        print(f"Final best fitness: {self.best_fitness:.6f}")
        return self.best_solution
    
    def get_statistics(self):
        """
        Get statistics about the run
        
        Returns:
            dict: Statistics about the evolutionary run
        """
        if not self.generation_stats:
            return None
        
        return {
            'best_fitness': self.best_fitness,
            'avg_final_fitness': self.generation_stats[-1]['avg_fitness'],
            'generations_run': len(self.generation_stats),
            'convergence_rate': self._calculate_convergence_rate()
        }
    
    def _calculate_convergence_rate(self):
        """Calculate how quickly the algorithm converged"""
        if len(self.generation_stats) < 10:
            return 0.0
        
        # Calculate fitness improvement over first 50% of generations
        mid_point = len(self.generation_stats) // 2
        initial_fitness = self.generation_stats[0]['avg_fitness']
        mid_fitness = self.generation_stats[mid_point]['avg_fitness']
        
        if initial_fitness > 0:
            return (initial_fitness - mid_fitness) / initial_fitness
        return 0.0