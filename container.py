"""
Container class for the cargo container loading problem
"""

class Container:
    """
    Represents a rectangular container with weight constraints
    """
    
    def __init__(self, width, height, max_weight):
        """
        Initialize a container
        
        Args:
            width (float): Container width
            height (float): Container height  
            max_weight (float): Maximum weight capacity
        """
        self.width = width
        self.height = height
        self.max_weight = max_weight
        
        # Calculate center of mass bounds (central 60%)
        self.com_min_x = width * 0.2
        self.com_max_x = width * 0.8
        self.com_min_y = height * 0.2
        self.com_max_y = height * 0.8
        
        self.area = width * height
    
    def is_valid_position(self, x, y, radius):
        """
        Check if a circle with given center and radius fits within container
        
        Args:
            x (float): X coordinate of circle center
            y (float): Y coordinate of circle center
            radius (float): Circle radius
            
        Returns:
            bool: True if position is valid, False otherwise
        """
        # Check boundaries
        left_bound = x - radius >= 0
        right_bound = x + radius <= self.width
        top_bound = y - radius >= 0
        bottom_bound = y + radius <= self.height
        
        return left_bound and right_bound and top_bound and bottom_bound
    
    def get_center_of_mass_bounds(self):
        """
        Get the bounds for center of mass calculation
        
        Returns:
            tuple: (min_x, max_x, min_y, max_y) bounds for center of mass
        """
        return (self.com_min_x, self.com_max_x, self.com_min_y, self.com_max_y)
    
    def __str__(self):
        return f"Container(width={self.width}, height={self.height}, max_weight={self.max_weight})"