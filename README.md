# Cargo Container Loading - Evolutionary Algorithm Implementation

This project implements an evolutionary algorithm to solve the cargo container loading problem, where cylindrical containers must be packed into a rectangular container while satisfying geometric and weight distribution constraints.

## Problem Description

The problem involves placing cylindrical containers (modeled as circles) within a rectangular container while satisfying:

1. **Geometric Constraint**: All cylinders must fit within the rectangular container boundaries
2. **Weight Distribution Constraint**: The center of mass must fall within the central 60% of the container
3. **Weight Limit Constraint**: Total weight cannot exceed the container's maximum capacity
4. **Loading Order Constraint**: Cylinders are loaded from the rear and cannot be moved once placed

## Project Structure

```
├── main.py                 # Main entry point
├── container.py           # Container class
├── cylinder.py            # Cylinder class
├── solution.py            # Solution representation and evaluation
├── evolutionary_algorithm.py # Genetic Algorithm implementation
├── greedy_algorithm.py    # Greedy and Bottom-Left algorithms
├── problem_instances.py   # Problem instances (reference and challenging)
├── visualization.py       # Solution visualization
├── test_algorithms.py     # Comprehensive testing and comparison
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Algorithms Implemented

### 1. Evolutionary Algorithm (Genetic Algorithm)
- **Encoding**: Permutation of cylinder indices with placement rules
- **Fitness Function**: Multi-objective with constraint penalties
- **Operators**: Tournament selection, order crossover, swap mutation
- **Local Search**: Position optimization and order improvement

### 2. Greedy Algorithms
- **Largest First**: Place largest cylinders first
- **Smallest First**: Place smallest cylinders first
- **Heaviest First**: Place heaviest cylinders first
- **Lightest First**: Place lightest cylinders first

### 3. Bottom-Left Algorithm
- Classic bottom-left heuristic for circle packing
- Places cylinders in lowest possible position, then as far left as possible

## Key Features

- **Constraint Handling**: Comprehensive constraint checking and penalty system
- **Multiple Algorithms**: Comparison between evolutionary and heuristic approaches
- **Visualization**: Text-based visualization of packing solutions
- **Problem Instances**: Built-in reference and challenging test cases
- **Performance Analysis**: Timing and fitness comparison across algorithms

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run All Algorithms
```bash
python test_algorithms.py
```

### Run Main Program
```bash
python main.py
```

### Test Individual Algorithm
```python
from test_algorithms import test_individual_algorithm
test_individual_algorithm()
```

## Problem Instances

### Reference Instances
- **reference_1**: Simple 3-cylinder problem
- **reference_2**: Medium complexity 5-cylinder problem
- **reference_3**: More complex 7-cylinder problem

### Challenging Instances
- **challenging_1**: Many small cylinders
- **challenging_2**: Mixed sizes with weight constraints
- **challenging_3**: Tight packing with weight distribution

## Fitness Function

The fitness function combines multiple objectives:

```
fitness = space_fitness + weight_penalty + com_penalty
```

Where:
- **space_fitness**: Minimizes wasted space (1.0 - space_utilization)
- **weight_penalty**: Penalty for exceeding weight capacity
- **com_penalty**: Penalty for center of mass outside central 60%

## Results and Analysis

The implementation has been tested on all reference and challenging instances. Key findings:

1. **Evolutionary Algorithm** generally finds better solutions than greedy approaches
2. **Bottom-Left** heuristic is fast but may get stuck in local optima
3. **Greedy strategies** vary in performance based on instance characteristics
4. **Constraint satisfaction** is prioritized over space optimization

## Future Improvements

1. **Enhanced Visualization**: Processing-based graphical visualization
2. **Advanced Operators**: More sophisticated crossover and mutation operators
3. **Hybrid Approaches**: Combine evolutionary algorithms with local search
4. **Parameter Optimization**: Adaptive parameter control
5. **Real-world Constraints**: Additional practical constraints

## Academic Context

This project addresses the following learning outcomes:
- **LO1**: Understanding of different Evolutionary Algorithms
- **LO2**: Design and implementation of an EA for a specific problem
- **LO3**: Documentation of EA development and testing
- **LO4**: Literature review and evaluation of different approaches

## License

This project is for educational purposes only.

## Contact

For questions or issues, please refer to the course documentation.