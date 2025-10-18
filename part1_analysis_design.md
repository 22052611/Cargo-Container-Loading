# Analysis and Design: Evolutionary Approach for Cargo Container Loading

## Problem Analysis

The cargo container loading problem presents a complex optimization challenge that combines geometric constraints with physical limitations. The problem involves placing cylindrical containers (modeled as circles) within a rectangular container while satisfying three key constraints:

1. **Geometric Constraint**: All cylinders must fit within the rectangular container boundaries
2. **Weight Distribution Constraint**: The center of mass must fall within the central 60% of the container
3. **Weight Limit Constraint**: Total weight cannot exceed the container's maximum capacity
4. **Loading Order Constraint**: Cylinders are loaded from the rear and cannot be moved once placed

The complexity arises from the interaction of these constraints, particularly the geometric placement of circles (which is more complex than rectangles due to their curved boundaries) and the physical constraints of weight distribution.

## Proposed Evolutionary Approach

### 1. Problem Encoding

The encoding scheme is crucial for representing potential solutions in a way that can be manipulated by evolutionary operators. For this problem, I propose a hybrid encoding approach:

**Primary Encoding (Permutation)**: Each solution is represented as a permutation of cylinder indices. This encoding captures the loading order constraint, as cylinders are placed in the sequence specified by the permutation.

**Secondary Encoding (Placement Rules)**: For each cylinder in the permutation, a set of placement rules determines its exact (x,y) coordinates:
- **Bottom-Left Heuristic**: Place the cylinder in the lowest possible position, then as far left as possible
- **Contact-Based Placement**: Place the cylinder touching previously placed cylinders or container walls
- **Weight-Aware Placement**: Adjust placement based on weight distribution requirements

**Chromosome Structure**: 
```
[π₁, π₂, ..., πₙ] where π is a permutation of cylinder indices
```

This encoding ensures that the loading order constraint is inherently satisfied and provides a clear mapping from genotype to phenotype.

### 2. Fitness Function

The fitness function must evaluate solutions based on all constraints while providing a gradient for optimization. I propose a multi-objective fitness function with penalty terms:

**Primary Objective**: Minimize wasted space
```
space_fitness = (container_area - total_cylinder_area) / container_area
```

**Constraint Penalties**:
- **Geometric Penalty**: Penalty for cylinders extending beyond container boundaries
- **Weight Distribution Penalty**: Penalty for center of mass outside central 60% region
- **Weight Limit Penalty**: Penalty for total weight exceeding capacity

**Composite Fitness Function**:
```
fitness = w₁ × space_fitness + w₂ × geometric_penalty + w₃ × weight_distribution_penalty + w₄ × weight_limit_penalty
```

Where weights w₁, w₂, w₃, w₄ are tuned to prioritize constraint satisfaction over space optimization.

**Center of Mass Calculation**:
```
center_of_mass_x = Σ(weight_i × x_i) / total_weight
center_of_mass_y = Σ(weight_i × y_i) / total_weight
```

The fitness function is designed to be minimized, with a perfect solution achieving a fitness of 0.

### 3. Local Search Strategy

Local search is essential for fine-tuning solutions and escaping local optima. I propose a multi-level local search approach:

**Placement Optimization**: For each cylinder, explore alternative valid positions within a reasonable radius of its current position. This includes:
- Small coordinate adjustments (±5% of cylinder diameter)
- Contact-based repositioning against nearby cylinders
- Weight-aware position adjustments

**Order Optimization**: Explore local changes to the permutation:
- **Swap**: Exchange positions of two adjacent cylinders
- **Insert**: Move a cylinder to a different position in the sequence
- **Reverse**: Reverse a subsequence of the permutation

**Constraint-Specific Operators**:
- **Weight Distribution Heuristic**: Adjust cylinder positions to improve weight balance
- **Geometric Refinement**: Optimize placement to reduce wasted space while maintaining constraints

**Local Search Integration**: The local search is applied with a probability during each generation, allowing the algorithm to explore both global and local search spaces effectively.

## Evolutionary Algorithm Design

### Selection Mechanism
- **Tournament Selection**: Select parents based on fitness comparison among small subsets
- **Elitism**: Preserve the best solutions across generations

### Crossover Operators
- **Order Crossover (OX)**: Preserve relative ordering of cylinders
- **Position-Based Crossover**: Exchange positions while maintaining order constraints
- **Uniform Order Crossover**: Mix parental orders with higher probability

### Mutation Operators
- **Swap Mutation**: Exchange positions of two randomly selected cylinders
- **Insert Mutation**: Move a cylinder to a random position
- **Inversion Mutation**: Reverse a random subsequence
- **Placement Mutation**: Adjust placement coordinates of a cylinder

### Parameter Control
- **Population Size**: 50-100 individuals
- **Generations**: 100-500 depending on problem complexity
- **Crossover Rate**: 0.7-0.9
- **Mutation Rate**: 0.1-0.3
- **Local Search Probability**: 0.1-0.2

## Implementation Strategy

The algorithm will be implemented in Python using the Processing library for visualization. The implementation will follow a modular approach:

1. **Problem Representation**: Classes for Container, Cylinder, and Solution
2. **Evolutionary Engine**: Core GA operations (selection, crossover, mutation)
3. **Fitness Evaluation**: Constraint checking and fitness calculation
4. **Local Search**: Neighborhood exploration and improvement
5. **Visualization**: Real-time display of packing progress and results

This design provides a comprehensive framework for solving the cargo container loading problem while addressing all specified constraints and optimization objectives.