"""
Test script to run and compare all algorithms
"""

import time
from container import Container
from cylinder import Cylinder
from evolutionary_algorithm import EvolutionaryAlgorithm
from greedy_algorithm import GreedyAlgorithm, BottomLeftAlgorithm
from problem_instances import load_reference_instances, load_challenging_instances
from visualization import Visualization

def run_algorithm_comparison():
    """
    Run all algorithms on all problem instances and compare results
    """
    print("=== Algorithm Comparison ===\n")
    
    # Load problem instances
    reference_instances = load_reference_instances()
    challenging_instances = load_challenging_instances()
    
    # Initialize visualization
    viz = Visualization()
    
    # Results storage
    all_results = {}
    
    # Test reference instances
    print("=== Reference Instances ===")
    for instance_name, instance_data in reference_instances.items():
        print(f"\n--- {instance_name} ---")
        
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
        
        instance_results = {}
        
        # Run Evolutionary Algorithm
        print("Running Evolutionary Algorithm...")
        ga = EvolutionaryAlgorithm(
            container=container,
            cylinders=cylinders,
            population_size=50,
            generations=100,
            crossover_rate=0.8,
            mutation_rate=0.2
        )
        start_time = time.time()
        ga_solution = ga.run()
        ga_time = time.time() - start_time
        
        instance_results['Evolutionary Algorithm'] = {
            'solution': ga_solution,
            'time': ga_time,
            'fitness': ga_solution.fitness
        }
        
        # Run Greedy Algorithms
        greedy_strategies = ['largest_first', 'smallest_first', 'heaviest_first', 'lightest_first']
        for strategy in greedy_strategies:
            print(f"Running Greedy Algorithm ({strategy})...")
            greedy = GreedyAlgorithm(container, cylinders.copy(), strategy)
            start_time = time.time()
            greedy_solution = greedy.run()
            greedy_time = time.time() - start_time
            
            instance_results[f'Greedy ({strategy})'] = {
                'solution': greedy_solution,
                'time': greedy_time,
                'fitness': greedy_solution.fitness
            }
        
        # Run Bottom-Left Algorithm
        print("Running Bottom-Left Algorithm...")
        bl = BottomLeftAlgorithm(container, cylinders.copy())
        start_time = time.time()
        bl_solution = bl.run()
        bl_time = time.time() - start_time
        
        instance_results['Bottom-Left'] = {
            'solution': bl_solution,
            'time': bl_time,
            'fitness': bl_solution.fitness
        }
        
        all_results[instance_name] = instance_results
        
        # Display results for this instance
        print(f"\nResults for {instance_name}:")
        print(f"{'Algorithm':<25} {'Fitness':<10} {'Time (s)':<10} {'Valid':<6}")
        print("-" * 55)
        
        for algo_name, result in instance_results.items():
            fitness = result['fitness']
            time_taken = result['time']
            valid = "YES" if result['solution'].valid else "NO"
            print(f"{algo_name:<25} {fitness:<10.4f} {time_taken:<10.2f} {valid:<6}")
        
        # Find best solution
        best_algo = min(instance_results.keys(), 
                       key=lambda k: instance_results[k]['fitness'])
        print(f"\nBest algorithm: {best_algo} (fitness: {instance_results[best_algo]['fitness']:.4f})")
    
    # Test challenging instances if available
    if challenging_instances:
        print("\n=== Challenging Instances ===")
        for instance_name, instance_data in challenging_instances.items():
            print(f"\n--- {instance_name} ---")
            
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
            
            instance_results = {}
            
            # Run Evolutionary Algorithm with larger parameters
            print("Running Evolutionary Algorithm...")
            ga = EvolutionaryAlgorithm(
                container=container,
                cylinders=cylinders,
                population_size=100,
                generations=200,
                crossover_rate=0.8,
                mutation_rate=0.2
            )
            start_time = time.time()
            ga_solution = ga.run()
            ga_time = time.time() - start_time
            
            instance_results['Evolutionary Algorithm'] = {
                'solution': ga_solution,
                'time': ga_time,
                'fitness': ga_solution.fitness
            }
            
            # Run Bottom-Left Algorithm
            print("Running Bottom-Left Algorithm...")
            bl = BottomLeftAlgorithm(container, cylinders.copy())
            start_time = time.time()
            bl_solution = bl.run()
            bl_time = time.time() - start_time
            
            instance_results['Bottom-Left'] = {
                'solution': bl_solution,
                'time': bl_time,
                'fitness': bl_solution.fitness
            }
            
            all_results[instance_name] = instance_results
            
            # Display results for this instance
            print(f"\nResults for {instance_name}:")
            print(f"{'Algorithm':<25} {'Fitness':<10} {'Time (s)':<10} {'Valid':<6}")
            print("-" * 55)
            
            for algo_name, result in instance_results.items():
                fitness = result['fitness']
                time_taken = result['time']
                valid = "YES" if result['solution'].valid else "NO"
                print(f"{algo_name:<25} {fitness:<10.4f} {time_taken:<10.2f} {valid:<6}")
            
            # Find best solution
            best_algo = min(instance_results.keys(), 
                           key=lambda k: instance_results[k]['fitness'])
            print(f"\nBest algorithm: {best_algo} (fitness: {instance_results[best_algo]['fitness']:.4f})")
    
    # Summary
    print("\n=== Summary ===")
    print(f"{'Instance':<20} {'Best Algorithm':<20} {'Best Fitness':<15} {'Total Time (s)':<15}")
    print("-" * 70)
    
    for instance_name, results in all_results.items():
        best_algo = min(results.keys(), key=lambda k: results[k]['fitness'])
        best_fitness = results[best_algo]['fitness']
        total_time = sum(r['time'] for r in results.values())
        
        print(f"{instance_name:<20} {best_algo:<20} {best_fitness:<15.4f} {total_time:<15.2f}")
    
    # Show detailed comparison for best solutions
    print("\n=== Best Solutions Details ===")
    for instance_name, results in all_results.items():
        best_algo = min(results.keys(), key=lambda k: results[k]['fitness'])
        best_solution = results[best_algo]['solution']
        
        print(f"\n--- {instance_name} - {best_algo} ---")
        print(f"Fitness: {best_solution.fitness:.6f}")
        print(f"Valid: {best_solution.valid}")
        print(f"Total Weight: {best_solution.total_weight:.2f}")
        print(f"Center of Mass: ({best_solution.center_of_mass[0]:.2f}, {best_solution.center_of_mass[1]:.2f})")
        print(f"Placement Order: {best_solution.permutation}")
        
        # Show constraint status
        com_min_x, com_max_x, com_min_y, com_max_y = best_solution.container.get_center_of_mass_bounds()
        weight_ok = best_solution.total_weight <= best_solution.container.max_weight
        com_ok = (com_min_x <= best_solution.center_of_mass[0] <= com_max_x and 
                 com_min_y <= best_solution.center_of_mass[1] <= com_max_y)
        geometric_ok = all(cylinder.placed for cylinder in best_solution.cylinders)
        
        print("Constraint Status:")
        print(f"  - Weight: {'PASS' if weight_ok else 'FAIL'}")
        print(f"  - Center of Mass: {'PASS' if com_ok else 'FAIL'}")
        print(f"  - Geometric: {'PASS' if geometric_ok else 'FAIL'}")
    
    return all_results

def test_individual_algorithm():
    """
    Test a single algorithm on a specific instance
    """
    print("=== Individual Algorithm Test ===")
    
    # Load a specific instance
    instances = load_reference_instances()
    instance_name = 'reference_2'
    instance_data = instances[instance_name]
    
    print(f"Testing {instance_name} instance...")
    
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
    
    # Run Evolutionary Algorithm
    ga = EvolutionaryAlgorithm(
        container=container,
        cylinders=cylinders,
        population_size=50,
        generations=100,
        crossover_rate=0.8,
        mutation_rate=0.2
    )
    
    print("Running Evolutionary Algorithm...")
    start_time = time.time()
    solution = ga.run()
    end_time = time.time()
    
    print(f"Algorithm completed in {end_time - start_time:.2f} seconds")
    print(f"Best fitness: {solution.fitness:.6f}")
    
    # Display solution
    viz = Visualization()
    viz.display_solution(solution, f"{instance_name} - Evolutionary Algorithm")
    
    return solution

if __name__ == "__main__":
    # Run full comparison
    results = run_algorithm_comparison()
    
    # Uncomment to test individual algorithm
    # test_individual_algorithm()
    
    print("\nTest completed!")