"""
Greedy algorithm implementation for cargo container loading
"""

import random
from container import Container
from cylinder import Cylinder
from solution import Solution

class GreedyAlgorithm:
    """
    Greedy algorithm for solving the cargo container loading problem
    """
    
    def __init__(self, container, cylinders, strategy='largest_first'):
        """
        Initialize the greedy algorithm
        
        Args:
            container (Container): The container to pack into
            cylinders (list): List of cylinders to pack
            strategy (str): Greedy strategy ('largest_first', 'smallest_first', 'heaviest_first', 'lightest_first')
        """
        self.container = container
        self.cylinders = cylinders
        self.strategy = strategy
        self.solution = None
        
    def sort_cylinders(self):
        """
        Sort cylinders according to the chosen strategy
        
        Returns:
            list: Sorted list of cylinder indices
        """
        if self.strategy == 'largest_first':
            return sorted(range(len(self.cylinders)), 
                         key=lambda i: self.cylinders[i].diameter, reverse=True)
        elif self.strategy == 'smallest_first':
            return sorted(range(len(self.cylinders)), 
                         key=lambda i: self.cylinders[i].diameter)
        elif self.strategy == 'heaviest_first':
            return sorted(range(len(self.cylinders)), 
                         key=lambda i: self.cylinders[i].weight, reverse=True)
        elif self.strategy == 'lightest_first':
            return sorted(range(len(self.cylinders)), 
                         key=lambda i: self.cylinders[i].weight)
        else:
            # Default: random order
            indices = list(range(len(self.cylinders)))
            random.shuffle(indices)
            return indices
    
    def find_best_position(self, cylinder):
        """
        Find the best position for a cylinder using bottom-left heuristic
        
        Args:
            cylinder (Cylinder): Cylinder to place
            
        Returns:
            tuple: (x, y) position or None if no valid position found
        """
        best_position = None
        best_y = float('inf')
        
        # Try positions from bottom to top
        step_size = cylinder.radius / 5.0
        
        for y in [cylinder.radius + i * step_size for i in range(int(self.container.height / step_size) + 1)]:
            if y > self.container.height - cylinder.radius:
                break
                
            for x in [cylinder.radius + i * step_size for i in range(int(self.container.width / step_size) + 1)]:
                if x > self.container.width - cylinder.radius:
                    break
                
                # Check if position is valid
                if self._is_position_valid(x, y, cylinder):
                    # Prefer lower positions
                    if y < best_y or (y == best_y and x < (best_position[0] if best_position else float('inf'))):
                        best_position = (x, y)
                        best_y = y
        
        return best_position
    
    def _is_position_valid(self, x, y, cylinder):
        """
        Check if a position is valid for a cylinder
        
        Args:
            x (float): X coordinate
            y (float): Y coordinate
            cylinder (Cylinder): Cylinder to place
            
        Returns:
            bool: True if position is valid
        """
        # Check container boundaries
        if not self.container.is_valid_position(x, y, cylinder.radius):
            return False
        
        # Check overlap with already placed cylinders
        for placed_cylinder in self.cylinders:
            if placed_cylinder.placed and placed_cylinder.overlaps_with(cylinder):
                return False
        
        return True
    
    def run(self):
        """
        Run the greedy algorithm
        
        Returns:
            Solution: Solution found by the greedy algorithm
        """
        # Reset all cylinders
        for cylinder in self.cylinders:
            cylinder.placed = False
            cylinder.x = None
            cylinder.y = None
        
        # Sort cylinders according to strategy
        placement_order = self.sort_cylinders()
        
        # Place cylinders
        placed_count = 0
        total_weight = 0
        
        for cylinder_idx in placement_order:
            cylinder = self.cylinders[cylinder_idx]
            
            # Find best position
            position = self.find_best_position(cylinder)
            
            if position is not None:
                # Place the cylinder
                cylinder.set_position(position[0], position[1])
                placed_count += 1
                total_weight += cylinder.weight
        
        # Create solution
        self.solution = Solution(self.container, self.cylinders, placement_order)
        self.solution.decode_and_evaluate()
        
        return self.solution
    
    def get_strategy_name(self):
        """
        Get the name of the current strategy
        
        Returns:
            str: Strategy name
        """
        return self.strategy.replace('_', ' ').title()

class BottomLeftAlgorithm:
    """
    Bottom-left heuristic algorithm for cargo container loading
    """
    
    def __init__(self, container, cylinders):
        """
        Initialize the bottom-left algorithm
        
        Args:
            container (Container): The container to pack into
            cylinders (list): List of cylinders to pack
        """
        self.container = container
        self.cylinders = cylinders
        self.solution = None
    
    def run(self):
        """
        Run the bottom-left algorithm
        
        Returns:
            Solution: Solution found by the bottom-left algorithm
        """
        # Reset all cylinders
        for cylinder in self.cylinders:
            cylinder.placed = False
            cylinder.x = None
            cylinder.y = None
        
        # Sort cylinders by size (largest first)
        placement_order = sorted(range(len(self.cylinders)), 
                               key=lambda i: self.cylinders[i].diameter, reverse=True)
        
        # Place cylinders using bottom-left heuristic
        placed_count = 0
        total_weight = 0
        
        for cylinder_idx in placement_order:
            cylinder = self.cylinders[cylinder_idx]
            
            # Find bottom-left position
            position = self._find_bottom_left_position(cylinder)
            
            if position is not None:
                # Place the cylinder
                cylinder.set_position(position[0], position[1])
                placed_count += 1
                total_weight += cylinder.weight
        
        # Create solution
        self.solution = Solution(self.container, self.cylinders, placement_order)
        self.solution.decode_and_evaluate()
        
        return self.solution
    
    def _find_bottom_left_position(self, cylinder):
        """
        Find the bottom-left position for a cylinder
        
        Args:
            cylinder (Cylinder): Cylinder to place
            
        Returns:
            tuple: (x, y) position or None if no valid position found
        """
        # Try positions from bottom to top
        y_positions = [cylinder.radius + i * cylinder.radius / 10.0 
                      for i in range(int(self.container.height / (cylinder.radius / 5.0)) + 1)]
        
        for y in y_positions:
            if y > self.container.height - cylinder.radius:
                break
            
            # For each y, find the leftmost valid x
            x_positions = [cylinder.radius + i * cylinder.radius / 10.0 
                          for i in range(int(self.container.width / (cylinder.radius / 5.0)) + 1)]
            
            for x in x_positions:
                if x > self.container.width - cylinder.radius:
                    break
                
                if self._is_position_valid(x, y, cylinder):
                    return (x, y)
        
        return None
    
    def _is_position_valid(self, x, y, cylinder):
        """
        Check if a position is valid for a cylinder
        
        Args:
            x (float): X coordinate
            y (float): Y coordinate
            cylinder (Cylinder): Cylinder to place
            
        Returns:
            bool: True if position is valid
        """
        # Check container boundaries
        if not self.container.is_valid_position(x, y, cylinder.radius):
            return False
        
        # Check overlap with already placed cylinders
        for placed_cylinder in self.cylinders:
            if placed_cylinder.placed and placed_cylinder.overlaps_with(cylinder):
                return False
        
        return True