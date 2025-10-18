# Literature Review: Rectangle Packing Problem

## History and Complexity

The rectangle packing problem, also known as the rectangular strip packing problem, has a rich history dating back to the early days of computational geometry. The problem involves arranging a set of rectangular items within a larger rectangular container to minimize wasted space or maximize utilization. This problem belongs to the class of NP-hard optimization problems, meaning that no known polynomial-time algorithm can solve all instances optimally (Garey & Johnson, 1979).

The computational complexity of rectangle packing was formally established in the 1970s when it was shown to be NP-complete. This means that as the problem size increases, the time required to find optimal solutions grows exponentially. The problem's complexity stems from the combinatorial nature of possible arrangements and the geometric constraints that must be satisfied.

## Applications

Rectangle packing problems have numerous practical applications across various industries:

1. **Manufacturing and Cutting Stock Problems**: In industries like steel, glass, and textile manufacturing, the problem of cutting rectangular sheets from larger rectangular stock materials to minimize waste is a classic application (Dyckhoff, 1990).

2. **Cargo Loading and Logistics**: The assessment's cargo container loading problem is directly related to logistics and transportation optimization, where efficient packing of cylindrical containers in rectangular shipping containers reduces transportation costs.

3. **VLSI Design**: In microelectronics, placing rectangular circuit components on rectangular silicon wafers to maximize chip yield is a critical application (Lengauer, 1991).

4. **Textile and Garment Industry**: Cutting patterns from rectangular fabric rolls to minimize material waste is another important application.

## Solution Algorithms

### 1. Guillotine Cut Algorithm

The guillotine cut algorithm is a classical approach that divides the remaining space using guillotine cuts (cuts that go from one edge to the opposite edge). This method was first proposed by Gilmore and Gomory (1965) for the cutting stock problem. The algorithm works by recursively dividing the available space into smaller rectangles using guillotine cuts and placing items in these spaces.

**Advantages**: Simple to implement, guarantees feasible solutions, and provides good approximations for many instances.
**Disadvantages**: Often suboptimal as it restricts the cutting pattern to guillotine cuts only.

### 2. Bottom-Left Fill Algorithm

The bottom-left (BL) heuristic places items one by one in the lowest possible position and then as far left as possible (Huang & Ye, 2011). This greedy approach builds the packing incrementally, placing each item in the first feasible position found.

**Advantages**: Fast execution time, easy to implement, and produces reasonable solutions for many practical instances.
**Disadvantages**: Can get stuck in local optima and may not find optimal solutions for complex instances.

### 3. Genetic Algorithm (Evolutionary Approach)

Genetic algorithms have been successfully applied to rectangle packing problems since the 1990s. Hopper and Turton (2001) demonstrated the effectiveness of genetic algorithms for 2D packing problems. The approach uses a population-based search with crossover and mutation operators to explore the solution space.

**Encoding**: Solutions are typically encoded as permutations of items, with placement rules determining the actual coordinates.
**Fitness Function**: Usually based on wasted space, container utilization, or constraint violations.
**Operators**: Order crossover (OX), position-based crossover, and various mutation operators are commonly used.

**Advantages**: Can escape local optima, handles complex constraints well, and can find near-optimal solutions for large instances.
**Disadvantages**: Computationally expensive, requires careful parameter tuning, and no guarantee of optimality.

## Recent Developments

Recent research has focused on hybrid approaches that combine evolutionary algorithms with local search heuristics. Burke et al. (2006) proposed a memetic algorithm that combines genetic algorithms with local search operators, showing improved performance over pure genetic approaches. More recent work has incorporated machine learning techniques to guide the search process and improve solution quality.

The problem continues to be an active area of research, with new variants and constraints being explored. The cargo container loading problem with cylindrical items and weight distribution constraints adds additional complexity that requires specialized evolutionary approaches.

## References

- Burke, E. K., Kendall, G., & Whitwell, G. (2006). A new placement heuristic for the orthogonal stock cutting problem. Operations Research, 54(3), 490-500.

- Dyckhoff, H. (1990). A typology of cutting and packing problems. European Journal of Operational Research, 44(2), 145-159.

- Garey, M. R., & Johnson, D. S. (1979). Computers and Intractability: A Guide to the Theory of NP-Completeness. W.H. Freeman.

- Gilmore, P. C., & Gomory, R. E. (1965). Multistage cutting stock problems of two and more dimensions. Operations Research, 13(1), 94-120.

- Hopper, E., & Turton, B. H. (2001). An empirical investigation of meta-heuristic and heuristic algorithms for a 2D packing problem. European Journal of Operational Research, 128(1), 34-57.

- Huang, E., & Ye, W. (2011). A simulated annealing algorithm for the container loading problem with shipment priority. International Journal of Production Economics, 132(2), 203-211.

- Lengauer, T. (1991). Combinatorial Algorithms for Integrated Circuit Layout. John Wiley & Sons.