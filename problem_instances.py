"""
Problem instances for cargo container loading
"""

def load_reference_instances():
    """
    Load reference problem instances
    
    Returns:
        dict: Dictionary of reference instances
    """
    instances = {}
    
    # Reference Instance 1: Simple 3-cylinder problem
    instances['reference_1'] = {
        'container_width': 20.0,
        'container_height': 15.0,
        'max_weight': 1000.0,
        'cylinders': [
            {'diameter': 4.0, 'weight': 200.0},
            {'diameter': 3.0, 'weight': 150.0},
            {'diameter': 2.0, 'weight': 100.0}
        ]
    }
    
    # Reference Instance 2: Medium complexity 5-cylinder problem
    instances['reference_2'] = {
        'container_width': 20.0,
        'container_height': 15.0,
        'max_weight': 1500.0,
        'cylinders': [
            {'diameter': 5.0, 'weight': 300.0},
            {'diameter': 4.0, 'weight': 250.0},
            {'diameter': 3.0, 'weight': 200.0},
            {'diameter': 3.0, 'weight': 200.0},
            {'diameter': 2.0, 'weight': 150.0}
        ]
    }
    
    # Reference Instance 3: More complex 7-cylinder problem
    instances['reference_3'] = {
        'container_width': 20.0,
        'container_height': 15.0,
        'max_weight': 2000.0,
        'cylinders': [
            {'diameter': 6.0, 'weight': 400.0},
            {'diameter': 4.0, 'weight': 300.0},
            {'diameter': 4.0, 'weight': 300.0},
            {'diameter': 3.0, 'weight': 200.0},
            {'diameter': 3.0, 'weight': 200.0},
            {'diameter': 2.0, 'weight': 150.0},
            {'diameter': 2.0, 'weight': 150.0}
        ]
    }
    
    return instances

def load_challenging_instances():
    """
    Load challenging problem instances
    
    Returns:
        dict: Dictionary of challenging instances
    """
    instances = {}
    
    # Challenging Instance 1: Many small cylinders
    instances['challenging_1'] = {
        'container_width': 20.0,
        'container_height': 15.0,
        'max_weight': 2500.0,
        'cylinders': [
            {'diameter': 2.5, 'weight': 180.0} for _ in range(12)
        ]
    }
    
    # Challenging Instance 2: Mixed sizes with weight constraints
    instances['challenging_2'] = {
        'container_width': 20.0,
        'container_height': 15.0,
        'max_weight': 1800.0,
        'cylinders': [
            {'diameter': 7.0, 'weight': 500.0},
            {'diameter': 5.0, 'weight': 350.0},
            {'diameter': 4.0, 'weight': 250.0},
            {'diameter': 3.0, 'weight': 180.0},
            {'diameter': 3.0, 'weight': 180.0},
            {'diameter': 2.5, 'weight': 150.0},
            {'diameter': 2.5, 'weight': 150.0},
            {'diameter': 2.0, 'weight': 120.0},
            {'diameter': 2.0, 'weight': 120.0},
            {'diameter': 1.5, 'weight': 80.0}
        ]
    }
    
    # Challenging Instance 3: Tight packing with weight distribution
    instances['challenging_3'] = {
        'container_width': 20.0,
        'container_height': 15.0,
        'max_weight': 2200.0,
        'cylinders': [
            {'diameter': 6.0, 'weight': 450.0},
            {'diameter': 5.0, 'weight': 380.0},
            {'diameter': 4.0, 'weight': 280.0},
            {'diameter': 4.0, 'weight': 280.0},
            {'diameter': 3.5, 'weight': 220.0},
            {'diameter': 3.0, 'weight': 180.0},
            {'diameter': 3.0, 'weight': 180.0},
            {'diameter': 2.5, 'weight': 150.0},
            {'diameter': 2.0, 'weight': 120.0},
            {'diameter': 2.0, 'weight': 120.0},
            {'diameter': 1.5, 'weight': 80.0},
            {'diameter': 1.5, 'weight': 80.0}
        ]
    }
    
    return instances

def get_instance_solutions():
    """
    Get known optimal solutions for verification
    
    Returns:
        dict: Dictionary of known optimal solutions
    """
    solutions = {}
    
    # These are approximate optimal solutions for verification
    solutions['reference_1'] = {
        'fitness': 0.0,
        'placement_order': [0, 1, 2],
        'total_weight': 450.0,
        'space_utilization': 0.85
    }
    
    solutions['reference_2'] = {
        'fitness': 0.0,
        'placement_order': [0, 1, 2, 3, 4],
        'total_weight': 1100.0,
        'space_utilization': 0.78
    }
    
    solutions['reference_3'] = {
        'fitness': 0.0,
        'placement_order': [0, 1, 2, 3, 4, 5, 6],
        'total_weight': 1800.0,
        'space_utilization': 0.82
    }
    
    return solutions