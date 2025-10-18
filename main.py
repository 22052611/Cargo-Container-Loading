"""
Main entry point for the Cargo Container Loading Evolutionary Algorithm
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evolutionary_algorithm import EvolutionaryAlgorithm
from container import Container
from cylinder import Cylinder
from problem_instances import load_reference_instances, load_challenging_instances
from visualization import Visualization
import time

def main():
    """Main function to run the evolutionary algorithm"""
    
    # Load problem instances
    print("Loading problem instances...")
    reference_instances = load_reference_instances()
    challenging_instances = load_challenging_instances()
    
    # Initialize visualization
    viz = Visualization()
    
    # Run evolutionary algorithm on reference instances
    print("\n=== Running Evolutionary Algorithm on Reference Instances ===")
    results = {}
    
    for instance_name, instance_data in reference_instances.items():
        print(f"\nSolving {instance_name}...")
        
        # Create container and cylinders
        container = Container(
            width=instance_data['container_width'],
            height=instance_data['container_height'],
            max_weight=instance_data['max_weight']
        )
        
        cylinders = []
        for i, cyl_data in enumerate(instance_data['cylinders']):
            cylinder = Cylinder(
                diameter=cyl_data['diameter'],
                weight=cyl_data['weight'],
                id=i
            )
            cylinders.append(cylinder)
        
        # Initialize and run evolutionary algorithm
        ga = EvolutionaryAlgorithm(
            container=container,
            cylinders=cylinders,
            population_size=50,
            generations=200,
            crossover_rate=0.8,
            mutation_rate=0.2
        )
        
        start_time = time.time()
        best_solution = ga.run()
        end_time = time.time()
        
        # Store results
        results[instance_name] = {
            'best_fitness': best_solution.fitness,
            'solution': best_solution,
            'time': end_time - start_time,
            'instance_data': instance_data
        }
        
        print(f"Best fitness: {best_solution.fitness}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        
        # Visualize best solution
        viz.display_solution(best_solution, instance_name)
    
    # Run on challenging instances if available
    if challenging_instances:
        print("\n=== Running Evolutionary Algorithm on Challenging Instances ===")
        
        for instance_name, instance_data in challenging_instances.items():
            print(f"\nSolving {instance_name}...")
            
            # Create container and cylinders
            container = Container(
                width=instance_data['container_width'],
                height=instance_data['container_height'],
                max_weight=instance_data['max_weight']
            )
            
            cylinders = []
            for i, cyl_data in enumerate(instance_data['cylinders']):
                cylinder = Cylinder(
                    diameter=cyl_data['diameter'],
                    weight=cyl_data['weight'],
                    id=i
                )
                cylinders.append(cylinder)
            
            # Initialize and run evolutionary algorithm
            ga = EvolutionaryAlgorithm(
                container=container,
                cylinders=cylinders,
                population_size=100,
                generations=500,
                crossover_rate=0.8,
                mutation_rate=0.2
            )
            
            start_time = time.time()
            best_solution = ga.run()
            end_time = time.time()
            
            # Store results
            results[instance_name] = {
                'best_fitness': best_solution.fitness,
                'solution': best_solution,
                'time': end_time - start_time,
                'instance_data': instance_data
            }
            
            print(f"Best fitness: {best_solution.fitness}")
            print(f"Time taken: {end_time - start_time:.2f} seconds")
            
            # Visualize best solution
            viz.display_solution(best_solution, instance_name)
    
    # Display summary
    print("\n=== Summary ===")
    for instance_name, result in results.items():
        print(f"{instance_name}: Fitness = {result['best_fitness']:.4f}, Time = {result['time']:.2f}s")
    
    # Keep visualization window open
    print("\nPress any key in the visualization window to exit...")
    viz.wait_for_exit()

if __name__ == "__main__":
    main()