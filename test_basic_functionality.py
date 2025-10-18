"""
Basic functionality test for the cargo container loading implementation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from container import Container
from cylinder import Cylinder
from solution import Solution

def test_basic_functionality():
    """Test basic functionality of the implementation"""
    
    print("=== Testing Basic Functionality ===")
    
    # Create a simple container
    container = Container(width=20, height=15, max_weight=1000)
    print(f"Created container: {container}")
    
    # Create some simple cylinders
    cylinders = [
        Cylinder(diameter=2, weight=100, id=0),
        Cylinder(diameter=3, weight=150, id=1),
        Cylinder(diameter=4, weight=200, id=2)
    ]
    print(f"Created {len(cylinders)} cylinders")
    
    # Create a solution with a specific order
    solution = Solution(container, cylinders, permutation=[0, 1, 2])
    print(f"Created solution with permutation: {solution.permutation}")
    
    # Decode and evaluate the solution
    solution.decode_and_evaluate()
    print(f"Solution evaluation:")
    print(f"  - Fitness: {solution.fitness}")
    print(f"  - Valid: {solution.valid}")
    print(f"  - Total weight: {solution.total_weight}")
    print(f"  - Center of mass: {solution.center_of_mass}")
    
    # Check COM bounds
    com_min_x, com_max_x, com_min_y, com_max_y = container.get_center_of_mass_bounds()
    print(f"  - COM bounds: x=[{com_min_x}, {com_max_x}], y=[{com_min_y}, {com_max_y}]")
    
    # Check constraint status
    com_x, com_y = solution.center_of_mass
    weight_ok = solution.total_weight <= container.max_weight
    com_ok = (com_min_x <= com_x <= com_max_x) and (com_min_y <= com_y <= com_max_y)
    
    print(f"  - Weight constraint: {'PASS' if weight_ok else 'FAIL'}")
    print(f"  - COM constraint: {'PASS' if com_ok else 'FAIL'}")
    
    # Show cylinder placements
    print("\nCylinder placements:")
    for cylinder in cylinders:
        if cylinder.placed:
            print(f"  - Cylinder {cylinder.id}: diameter={cylinder.diameter}, weight={cylinder.weight}, pos=({cylinder.x}, {cylinder.y})")
    
    print("\n=== Basic functionality test completed ===")

if __name__ == "__main__":
    test_basic_functionality()