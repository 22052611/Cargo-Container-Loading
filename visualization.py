"""
Visualization module for cargo container loading solutions
"""

import sys
import time
from container import Container
from cylinder import Cylinder

class Visualization:
    """
    Visualization class for displaying container loading solutions
    """
    
    def __init__(self, scale=20):
        """
        Initialize the visualization
        
        Args:
            scale (float): Scale factor for display
        """
        self.scale = scale
        self.solutions = []
        self.current_solution_index = 0
        self.algorithm_names = []
        
        # Initialize Processing (this would normally use the Processing library)
        # For now, we'll create a text-based visualization
        self.width = 800
        self.height = 600
        
    def display_solution(self, solution, title="Solution"):
        """
        Display a solution
        
        Args:
            solution (Solution): Solution to display
            title (str): Title for the display
        """
        print(f"\n=== {title} ===")
        print(f"Fitness: {solution.fitness:.6f}")
        print(f"Valid: {solution.valid}")
        print(f"Total Weight: {solution.total_weight:.2f}")
        print(f"Container Max Weight: {solution.container.max_weight}")
        print(f"Center of Mass: ({solution.center_of_mass[0]:.2f}, {solution.center_of_mass[1]:.2f})")
        
        # Check constraints
        com_min_x, com_max_x, com_min_y, com_max_y = solution.container.get_center_of_mass_bounds()
        print(f"COM Bounds: ({com_min_x:.2f}, {com_max_x:.2f}) x ({com_min_y:.2f}, {com_max_y:.2f})")
        
        if solution.valid:
            print("Constraint Status:")
            print(f"  - Weight constraint: {'PASS' if solution.total_weight <= solution.container.max_weight else 'FAIL'}")
            com_ok = (com_min_x <= solution.center_of_mass[0] <= com_max_x and
                     com_min_y <= solution.center_of_mass[1] <= com_max_y)
            print(f"  - COM constraint: {'PASS' if com_ok else 'FAIL'}")
            print(f"  - Geometric constraint: {'PASS' if all(cylinder.placed for cylinder in solution.cylinders) else 'FAIL'}")
        
        # Display placement order
        print(f"\nPlacement Order: {solution.permutation}")
        
        # Display cylinder positions
        print("\nCylinder Placements:")
        for i, cylinder_idx in enumerate(solution.permutation):
            cylinder = solution.cylinders[cylinder_idx]
            print(f"  {i+1}. Cylinder {cylinder_idx}: diameter={cylinder.diameter}, weight={cylinder.weight}, "
                  f"position=({cylinder.x:.2f}, {cylinder.y:.2f})")
        
        # Display text-based visualization
        self._display_text_visualization(solution)
    
    def _display_text_visualization(self, solution):
        """
        Display a text-based visualization of the container
        
        Args:
            solution (Solution): Solution to visualize
        """
        container = solution.container
        grid_width = int(container.width / self.scale)
        grid_height = int(container.height / self.scale)
        
        # Create grid
        if grid_width <= 0 or grid_height <= 0:
            print(f"Warning: Invalid grid dimensions {grid_width}x{grid_height}")
            return
            
        grid = [[' ' for _ in range(grid_width)] for _ in range(grid_height)]
        
        # Mark container boundaries
        for i in range(grid_width):
            if 0 <= i < grid_width:
                grid[0][i] = '═'
                grid[grid_height-1][i] = '═'
        for i in range(grid_height):
            if 0 <= i < grid_height:
                grid[i][0] = '║'
                grid[i][grid_width-1] = '║'
        
        # Mark center of mass bounds
        com_min_x, com_max_x, com_min_y, com_max_y = container.get_center_of_mass_bounds()
        com_min_grid_x = int(com_min_x / self.scale)
        com_max_grid_x = int(com_max_x / self.scale)
        com_min_grid_y = int(com_min_y / self.scale)
        com_max_grid_y = int(com_max_y / self.scale)
        
        for i in range(com_min_grid_y, com_max_grid_y + 1):
            if 0 <= i < grid_height:
                grid[i][com_min_grid_x] = '│'
                grid[i][com_max_grid_x] = '│'
        for i in range(com_min_grid_x, com_max_grid_x + 1):
            if 0 <= i < grid_width:
                grid[com_min_grid_y][i] = '─'
                grid[com_max_grid_y][i] = '─'
        
        # Place cylinders
        cylinder_chars = ['●', '○', '◉', '◎', '◐', '◑', '◒', '◓', '■', '□']
        for i, cylinder_idx in enumerate(solution.permutation):
            cylinder = solution.cylinders[cylinder_idx]
            if cylinder.placed:
                grid_x = int(cylinder.x / self.scale)
                grid_y = int(cylinder.y / self.scale)
                radius_grid = int(cylinder.radius / self.scale)
                
                # Mark cylinder position
                if 0 <= grid_y < grid_height and 0 <= grid_x < grid_width:
                    char = cylinder_chars[i % len(cylinder_chars)]
                    grid[grid_y][grid_x] = char
        
        # Display grid
        print(f"\nText Visualization (scale: {self.scale})")
        print("Legend: ══║│ = container bounds, ── = COM bounds, ●○◉◎ = cylinders")
        for row in grid:
            print(''.join(row))
    
    def add_solution(self, solution, algorithm_name=""):
        """
        Add a solution to the comparison list
        
        Args:
            solution (Solution): Solution to add
            algorithm_name (str): Name of the algorithm
        """
        self.solutions.append(solution)
        self.algorithm_names.append(algorithm_name)
    
    def compare_solutions(self):
        """
        Compare all added solutions
        """
        if not self.solutions:
            print("No solutions to compare")
            return
        
        print("\n=== Solution Comparison ===")
        print(f"{'Algorithm':<15} {'Fitness':<10} {'Valid':<6} {'Weight':<10} {'COM':<15}")
        print("-" * 60)
        
        for i, (solution, name) in enumerate(zip(self.solutions, self.algorithm_names)):
            fitness_str = f"{solution.fitness:.4f}"
            valid_str = "YES" if solution.valid else "NO"
            weight_str = f"{solution.total_weight:.1f}"
            com_str = f"({solution.center_of_mass[0]:.1f},{solution.center_of_mass[1]:.1f})"
            
            print(f"{name:<15} {fitness_str:<10} {valid_str:<6} {weight_str:<10} {com_str:<15}")
    
    def show_progress(self, generation, best_fitness, avg_fitness):
        """
        Show progress during evolution
        
        Args:
            generation (int): Current generation
            best_fitness (float): Best fitness in current generation
            avg_fitness (float): Average fitness in current generation
        """
        print(f"Gen {generation:4d}: Best = {best_fitness:.6f}, Avg = {avg_fitness:.6f}")
    
    def wait_for_exit(self):
        """
        Wait for user input to exit
        """
        print("\nPress Enter to exit...")
        input()
    
    def save_solution_image(self, solution, filename):
        """
        Save solution visualization as image (placeholder for actual image saving)
        
        Args:
            solution (Solution): Solution to save
            filename (str): Filename for the image
        """
        # This would use Processing to save an actual image
        # For now, we'll just save the text representation
        with open(filename + '.txt', 'w') as f:
            f.write(f"Solution saved: {filename}\n")
            f.write(f"Fitness: {solution.fitness:.6f}\n")
            f.write(f"Valid: {solution.valid}\n")
            f.write(f"Total Weight: {solution.total_weight:.2f}\n")
            f.write(f"Center of Mass: ({solution.center_of_mass[0]:.2f}, {solution.center_of_mass[1]:.2f})\n")
            f.write(f"Placement Order: {solution.permutation}\n")
            
            # Add cylinder positions
            for i, cylinder_idx in enumerate(solution.permutation):
                cylinder = solution.cylinders[cylinder_idx]
                f.write(f"Cylinder {cylinder_idx}: pos=({cylinder.x:.2f}, {cylinder.y:.2f}), "
                       f"diameter={cylinder.diameter}, weight={cylinder.weight}\n")
        
        print(f"Solution saved to {filename}.txt")

# Alternative Processing-based visualization (commented out as it requires Processing library)
"""
class ProcessingVisualization:
    def __init__(self, scale=20):
        self.scale = scale
        self.setup()
    
    def setup(self):
        size(800, 600)
        background(240)
    
    def draw_container(self, container):
        # Draw container boundaries
        stroke(0)
        strokeWeight(2)
        noFill()
        rect(0, 0, container.width * self.scale, container.height * self.scale)
        
        # Draw center of mass bounds
        com_min_x, com_max_x, com_min_y, com_max_y = container.get_center_of_mass_bounds()
        stroke(255, 0, 0, 100)
        strokeWeight(1)
        rect(com_min_x * self.scale, com_min_y * self.scale,
             (com_max_x - com_min_x) * self.scale, (com_max_y - com_min_y) * self.scale)
    
    def draw_cylinders(self, cylinders):
        # Draw cylinders
        for i, cylinder in enumerate(cylinders):
            if cylinder.placed:
                x = cylinder.x * self.scale
                y = cylinder.y * self.scale
                r = cylinder.radius * self.scale
                
                # Color based on weight
                weight_ratio = cylinder.weight / 500.0  # Normalize to max weight of 500
                fill(100 + weight_ratio * 155, 100, 100)
                noStroke()
                ellipse(x, y, r * 2, r * 2)
                
                # Draw cylinder ID
                fill(255)
                textAlign(CENTER, CENTER)
                textSize(10)
                text(str(cylinder.id), x, y)
    
    def draw_solution(self, solution):
        background(240)
        self.draw_container(solution.container)
        self.draw_cylinders(solution.cylinders)
        
        # Draw info
        fill(0)
        textAlign(LEFT, TOP)
        textSize(12)
        text(f"Fitness: {solution.fitness:.4f}", 10, 10)
        text(f"Valid: {solution.valid}", 10, 25)
        text(f"Weight: {solution.total_weight:.1f}", 10, 40)
        text(f"COM: ({solution.center_of_mass[0]:.1f}, {solution.center_of_mass[1]:.1f})", 10, 55)
"""