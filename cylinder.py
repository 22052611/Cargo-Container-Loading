"""
Cylinder class for the cargo container loading problem
"""

class Cylinder:
    """
    Represents a cylindrical container (modeled as a circle)
    """
    
    def __init__(self, diameter, weight, id):
        """
        Initialize a cylinder
        
        Args:
            diameter (float): Cylinder diameter
            weight (float): Cylinder weight
            id (int): Unique identifier for the cylinder
        """
        self.diameter = diameter
        self.radius = diameter / 2.0
        self.weight = weight
        self.id = id
        self.x = None
        self.y = None
        self.placed = False
    
    def set_position(self, x, y):
        """
        Set the position of the cylinder
        
        Args:
            x (float): X coordinate of center
            y (float): Y coordinate of center
        """
        self.x = x
        self.y = y
        self.placed = True
    
    def get_position(self):
        """
        Get the position of the cylinder
        
        Returns:
            tuple: (x, y) coordinates of center
        """
        return (self.x, y)
    
    def overlaps_with(self, other):
        """
        Check if this cylinder overlaps with another cylinder
        
        Args:
            other (Cylinder): Another cylinder to check against
            
        Returns:
            bool: True if cylinders overlap, False otherwise
        """
        if not (self.placed and other.placed):
            return False
            
        distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return distance < (self.radius + other.radius)
    
    def touches(self, other):
        """
        Check if this cylinder touches another cylinder
        
        Args:
            other (Cylinder): Another cylinder to check against
            
        Returns:
            bool: True if cylinders touch, False otherwise
        """
        if not (self.placed and other.placed):
            return False
            
        distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return abs(distance - (self.radius + other.radius)) < 1e-6
    
    def get_area(self):
        """
        Get the area of the cylinder
        
        Returns:
            float: Area of the cylinder
        """
        return 3.14159 * self.radius ** 2
    
    def __str__(self):
        return f"Cylinder(id={self.id}, diameter={self.diameter}, weight={self.weight}, pos=({self.x}, {self.y}))"
    
    def __repr__(self):
        return self.__str__()