"""
Solution class for representing and evaluating packing solutions
"""

import random

class Solution:
    """
    Represents a solution to the cargo container loading problem
    """
    
    def __init__(self, container, cylinders, permutation=None):
        """
        Initialize a solution
        
        Args:
            container (Container): The container to pack into
            cylinders (list): List of cylinders to pack
            permutation (list): Order of cylinders (if None, random order)
        """
        self.container = container
        self.cylinders = cylinders
        self.permutation = permutation if permutation is not None else self._generate_random_permutation()
        self.fitness = None
        self.placements = []
        self.total_weight = 0
        self.center_of_mass = (0, 0)
        self.valid = True
        
    def _generate_random_permutation(self):
        """Generate a random permutation of cylinder indices"""
        indices = list(range(len(self.cylinders)))
        random.shuffle(indices)
        return indices
    
    def decode_and_evaluate(self):
        """
        Decode the permutation into actual cylinder placements and evaluate fitness
        """
        # Reset all cylinders
        for cylinder in self.cylinders:
            cylinder.placed = False
            cylinder.x = None
            cylinder.y = None
        
        self.placements = []
        self.total_weight = 0
        self.valid = True
        
        # Place cylinders according to permutation order
        for cylinder_idx in self.permutation:
            cylinder = self.cylinders[cylinder_idx]
            
            # Find valid position for this cylinder
            position = self._find_valid_position(cylinder)
            
            if position is None:
                # Could not place cylinder - invalid solution
                self.valid = False
                self.fitness = float('inf')
                return
            
            # Place the cylinder
            cylinder.set_position(position[0], position[1])
            self.placements.append((cylinder_idx, position))
            self.total_weight += cylinder.weight
        
        # Evaluate fitness
        self._evaluate_fitness()
    
    def _find_valid_position(self, cylinder):
        """
        Find a valid position for a cylinder using improved placement heuristic
        
        Args:
            cylinder (Cylinder): Cylinder to place
            
        Returns:
            tuple: (x, y) position or None if no valid position found
        """
        # Try multiple placement strategies
        
        # Strategy 1: Bottom-left with better spacing
        step_size = cylinder.radius / 5.0  # Coarser search for speed
        
        # Start from bottom-left corner
        y = cylinder.radius
        while y <= self.container.height - cylinder.radius:
            x = cylinder.radius
            while x <= self.container.width - cylinder.radius:
                # Check if this position is valid
                if self._is_position_valid(x, y, cylinder):
                    return (x, y)
                
                # Move right
                x += step_size
            
            # Move up
            y += step_size
        
        # Strategy 2: Try to place near existing cylinders for better packing
        contact_position = self._find_contact_position(cylinder)
        if contact_position:
            return contact_position
        
        # Strategy 3: Try grid-based placement with better distribution
        grid_size = cylinder.radius * 2
        grid_positions = []
        
        # Generate grid positions in a more distributed manner
        for grid_y in range(int(self.container.height / grid_size) + 1):
            for grid_x in range(int(self.container.width / grid_size) + 1):
                x = grid_x * grid_size + cylinder.radius
                y = grid_y * grid_size + cylinder.radius
                grid_positions.append((x, y))
        
        # Shuffle to avoid bias
        random.shuffle(grid_positions)
        
        for x, y in grid_positions:
            if self._is_position_valid(x, y, cylinder):
                return (x, y)
        
        # Strategy 4: Random placement as last resort
        for _ in range(50):
            x = random.uniform(cylinder.radius, self.container.width - cylinder.radius)
            y = random.uniform(cylinder.radius, self.container.height - cylinder.radius)
            
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
    
    def _find_contact_position(self, cylinder):
        """
        Find a position for cylinder that touches other cylinders or walls
        
        Args:
            cylinder (Cylinder): Cylinder to place
            
        Returns:
            tuple: (x, y) position or None if no valid position found
        """
        # Try positions touching already placed cylinders
        for placed_cylinder in self.cylinders:
            if not placed_cylinder.placed:
                continue
                
            # Calculate possible contact positions (8 directions around the placed cylinder)
            directions = [
                (1, 0),   # right
                (-1, 0),  # left
                (0, 1),   # down
                (0, -1),  # up
                (1, 1),   # down-right
                (1, -1),  # up-right
                (-1, 1),  # down-left
                (-1, -1)  # up-left
            ]
            
            for dx, dy in directions:
                # Position touching the placed cylinder
                new_x = placed_cylinder.x + (cylinder.radius + placed_cylinder.radius) * dx
                new_y = placed_cylinder.y + (cylinder.radius + placed_cylinder.radius) * dy
                
                if self._is_position_valid(new_x, new_y, cylinder):
                    return (new_x, new_y)
        
        # Try positions touching container walls
        wall_positions = [
            (cylinder.radius, cylinder.radius),  # bottom-left corner
            (self.container.width - cylinder.radius, cylinder.radius),  # bottom-right corner
            (cylinder.radius, self.container.height - cylinder.radius),  # top-left corner
            (self.container.width - cylinder.radius, self.container.height - cylinder.radius),  # top-right corner
        ]
        
        for x, y in wall_positions:
            if self._is_position_valid(x, y, cylinder):
                return (x, y)
        
        return None
    
    def _evaluate_fitness(self):
        """
        Evaluate the fitness of the current solution
        """
        if not self.valid:
            self.fitness = float('inf')
            return
        
        # Calculate center of mass
        com_x = sum(cylinder.weight * cylinder.x for cylinder in self.cylinders if cylinder.placed)
        com_y = sum(cylinder.weight * cylinder.y for cylinder in self.cylinders if cylinder.placed)
        
        if self.total_weight > 0:
            com_x /= self.total_weight
            com_y /= self.total_weight
        
        self.center_of_mass = (com_x, com_y)
        
        # Check constraints
        com_min_x, com_max_x, com_min_y, com_max_y = self.container.get_center_of_mass_bounds()
        
        # Weight constraint penalty
        weight_penalty = max(0, self.total_weight - self.container.max_weight) * 1000
        
        # Center of mass constraint penalty - much higher penalty
        com_penalty_x = max(0, com_min_x - com_x, com_x - com_max_x) * 1000
        com_penalty_y = max(0, com_min_y - com_y, com_y - com_max_y) * 1000
        com_penalty = com_penalty_x + com_penalty_y
        
        # Space utilization (primary objective - minimize wasted space)
        total_cylinder_area = sum(cylinder.get_area() for cylinder in self.cylinders if cylinder.placed)
        space_utilization = total_cylinder_area / self.container.area
        space_fitness = 1.0 - space_utilization  # Minimize this
        
        # Add penalty for cylinders not placed (if any)
        placement_penalty = (len(self.cylinders) - sum(1 for c in self.cylinders if c.placed)) * 1000
        
        # Composite fitness
        self.fitness = space_fitness + weight_penalty + com_penalty + placement_penalty
    
    def mutate(self, mutation_rate):
        """
        Apply mutation to the solution
        
        Args:
            mutation_rate (float): Probability of mutation
        """
        if random.random() < mutation_rate:
            # Swap mutation
            i, j = random.sample(range(len(self.permutation)), 2)
            self.permutation[i], self.permutation[j] = self.permutation[j], self.permutation[i]
    
    def crossover(self, other):
        """
        Perform crossover with another solution
        
        Args:
            other (Solution): Another solution to crossover with
            
        Returns:
            Solution: New solution from crossover
        """
        # Order crossover (OX)
        child_permutation = [None] * len(self.permutation)
        
        # Select a random segment
        start, end = sorted(random.sample(range(len(self.permutation)), 2))
        
        # Copy segment from parent 1
        child_permutation[start:end] = self.permutation[start:end]
        
        # Fill remaining positions from parent 2 in order
        ptr = 0
        for gene in other.permutation:
            if gene not in child_permutation:
                while child_permutation[ptr] is not None:
                    ptr += 1
                child_permutation[ptr] = gene
        
        # Create new solution
        child = Solution(self.container, self.cylinders, child_permutation)
        child.decode_and_evaluate()
        
        return child
    
    def __str__(self):
        return f"Solution(fitness={self.fitness}, valid={self.valid}, weight={self.total_weight})"
    
    def __repr__(self):
        return self.__str__()