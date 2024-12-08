## Introduction

In this task, we were given the objective of applying theoretical knowledge of optimization to a practical problem. The goal was to develop an efficient solution for arranging components on 5-meter × 5-meter sheets for thermal treatment, maximizing space utilization and minimizing the number of sheets used, while adhering to specific constraints such as spacing requirements.

After analyzing the problem in detail, we decided to test two algorithms to find the most effective solution. We first implemented **Simulated Annealing (SA)**, a straightforward approach for local optimization, to evaluate its ability to handle the problem's constraints. Subsequently, we applied **Genetic Algorithm (GA)**, a more complex population-based method, to explore its potential for achieving better global optimization results.

### Problem Description

The task involves optimizing the placement of components onto **5-meter × 5-meter sheets** for thermal treatment in a furnace. The process includes adhering to strict spatial and thermal insulation requirements. Orders are processed in **two batches per day**:
1. **Midnight to noon** (first batch).
2. **Noon to midnight** (second batch).

The goal is to maximize the utilization of sheet space while minimizing the total number of sheets used, ensuring that all components in each batch are processed together. Once all orders in a batch are processed, the sheet numbering should **restart from 1** for the next batch.


### Input Dataset Description

The dataset provides detailed information about component orders and includes the following columns:

| **Column**           | **Description**                                                                   |
|----------------------|-----------------------------------------------------------------------------------|
| **Component_ID**     | A unique identifier for each component.                                           |
| **Dimensions**       | The size of the component in centimeters (length × width × height).               |
| **Quantity**         | The number of units ordered for the specified component.                          |
| **Order_Timestamp**  | The date and time of the order, used to group components into processing batches. |

#### Dataset Preview:

| Component_ID | Dimensions | Quantity | Order_Timestamp        |
|--------------|------------|----------|------------------------|
| MR-009       | 40x30x10   | 5        | 2024-09-16 00:26:41    |
| PL-014       | 40x20x10   | 5        | 2024-09-16 00:26:41    |
| BR-178       | 30x30x5    | 1        | 2024-09-16 00:26:41    |
| FE-213       | 40x20x10   | 1        | 2024-09-16 00:26:41    |
| AZ-011       | 40x25x10   | 1        | 2024-09-16 00:26:41    |


### Key Constraints

1. **Sheet Dimensions**: Each sheet measures **500 cm × 500 cm**.
2. **Thermal Insulation Gaps**:
    - **5 cm gap** must surround each component.
    - **10 cm gap** is required between adjacent components (i.e., two 5 cm blocks).
3. **Component Placement**: Components must lie flat, utilizing their largest face.
4. **Batch Separation**: Sheets for the first and second batches are numbered independently, starting at **1** for each batch.


### Objective

- **Maximize Space Utilization**: Aim to utilize as much of the sheet area as possible by efficiently arranging components.
- **Minimize Number of Sheets**: Reduce the number of sheets used for each batch by compactly packing the components.
- **Restart Sheet Numbering**: For each batch (morning and evening), restart the numbering of sheets from **1**.


### Efficiency Evaluation

To evaluate the **efficiency of the optimization**:
1. **Compare Space Utilization**: Compute the percentage of utilized space on the sheets under the optimized placement strategy.
2. **Baseline Comparison**: Compare the optimized arrangement against a baseline approach, where components are placed **chronologically**, without rearrangement or optimization.
3. **Metric**: The efficiency improvement is quantified as the percentage increase in utilized space on the sheets:

    Efficiency Improvement = $\frac{\text{Optimized Utilization} - \text{Baseline Utilization}}{\text{Baseline Utilization}} \times 100$



### Expected Output

The solution should produce a CSV file with the following columns for each component placement:
- **Sheet Number**: Indicates the sheet onto which the component is placed (starting from 1 for each batch).
- **Component_ID**: The unique identifier of the component.
- **Order Timestamp**: The time of the order, linking the placement to its batch.
- **Placement Coordinates**: The **x, y** coordinates of the top-left corner of the component on the sheet, measured in centimeters.

This format ensures clarity, traceability, and compliance with the constraints. The efficiency analysis will provide insight into the benefits of optimization compared to a naive chronological placement.

We considered three algorithms for solving the problem: Genetic Algorithm (GA), Simulated Annealing (SA), and Tabu Search (TS).

## Problem-Solving Algorithms

### Genetic Algorithm (GA)
**Genetic Algorithm (GA)** is an optimization technique inspired by the process of natural selection. It uses concepts such as populations, selection, crossover, and mutation to evolve solutions toward an optimal or near-optimal result.
### Pseudocode for Genetic Algorithm (GA)
```plaintext
1. Initialize a population of candidate solutions randomly.
2. Evaluate the fitness of each candidate based on the objective function.
3. Repeat until stopping criteria (e.g., max generations, acceptable solution) are met:
   a. Select parents from the population based on their fitness.
   b. Perform crossover on selected parents to create offspring.
   c. Apply mutation to offspring to introduce diversity.
   d. Evaluate the fitness of offspring.
   e. Select the next generation from the current population and offspring.
4. Return the best solution found.
```


### Genetic Algorithm (GA)

**Genetic Algorithm (GA)** is an optimization technique inspired by the process of natural selection. It uses concepts such as populations, selection, crossover, and mutation to evolve solutions toward an optimal or near-optimal result.

#### Strengths:
- **Global Optimization Efficiency**: GA is particularly effective for exploring large and complex search spaces, even in problems with many constraints or non-linear objectives.
- **Broad Search Capability**: The population-based approach ensures that multiple regions of the solution space are explored simultaneously, increasing the likelihood of finding a global optimum.
- **Avoiding Local Optima**: Crossover and mutation operations help the algorithm escape local optima and continue searching for better solutions.
- **Flexibility**: Can be adapted to work with discrete, continuous, and mixed optimization problems.

#### Weaknesses:
- **Computational Expense**: GAs can be computationally expensive due to the need to evaluate a large population over many generations.
- **Parameter Sensitivity**: Proper tuning of parameters like population size, mutation rates, and crossover probabilities is crucial for good performance.


### Simulated Annealing (SA)

**Simulated Annealing (SA)** is a local optimization algorithm inspired by the physical annealing process, where a material is slowly cooled to achieve a state of minimum energy.
```plaintext
1. Initialize a candidate solution randomly.
2. Set an initial temperature (T) and a cooling rate (α).
3. Evaluate the fitness of the initial solution.
4. Repeat until stopping criteria (e.g., final temperature, max iterations) are met:
   a. Generate a new candidate by modifying the current solution.
   b. Evaluate the fitness of the new candidate.
   c. Accept the new candidate with probability based on fitness and T.
   d. Reduce the temperature: T = α × T.
5. Return the best solution found.
```

#### Strengths:
- **Simple Implementation**: SA is straightforward to implement and requires fewer components than population-based algorithms like GA.
- **Avoiding Local Optima**: By accepting worse solutions with a certain probability, especially in the early stages, SA can escape local optima.
- **Flexibility**: Works well for both continuous and discrete optimization problems.

#### Weaknesses:
- **Cooling Schedule Dependency**: The effectiveness of SA heavily depends on the cooling schedule; improper settings can lead to premature convergence or slow execution.
- **Single Candidate Approach**: Unlike GA, SA operates on a single solution, which limits its ability to explore the search space comprehensively.

### Why We Chose These Algorithms for Comparison

When addressing our bin-packing optimization problem, we wanted to ensure we selected algorithms that could handle the complexity of the task while respecting its constraints. **Genetic Algorithm (GA)**, **Simulated Annealing (SA)**, and **Tabu Search (TS)** were natural choices because they are well-established methods for solving optimization problems, each bringing unique strengths to the table.

#### **Why These Three Algorithms?**
- **Genetic Algorithm (GA)** stands out as a global optimization method. It is particularly effective in exploring large, complex solution spaces like ours, where the goal is to maximize sheet utilization while minimizing the number of sheets. With its population-based nature, GA can evaluate multiple potential arrangements simultaneously, providing a diverse exploration of the space. Its adaptability to constraints—by penalizing infeasible solutions—makes it ideal for solving a problem as intricate as ours.

- **Simulated Annealing (SA)** offers a different approach. While it doesn’t evaluate a population of solutions like GA, it introduces probabilistic mechanisms that allow it to escape local optima. This makes SA a strong candidate for refining solutions, especially when dealing with the tight spatial constraints of placing components on sheets. Its simplicity is appealing, and it serves as a great benchmark for testing the efficiency of more sophisticated approaches like GA.

- **Tabu Search (TS)** was included for its structured local search capabilities. TS avoids getting stuck in cycles by remembering previously visited solutions and steering the search in new directions. It’s an appealing choice for tasks with clear neighborhood structures, and we wanted to test its potential for fine-tuning solutions in our context.

### Comparison of GA and SA

#### **Exploration vs. Exploitation**:
- **Genetic Algorithm (GA)**:  
  GA excels in **exploration** due to its population-based approach. By evaluating a diverse set of solutions in each generation, GA searches multiple regions of the solution space simultaneously. This makes it particularly effective for avoiding premature convergence and thoroughly investigating the search space for better solutions. The genetic operators (crossover and mutation) enable GA to combine features of good solutions and introduce diversity, further enhancing exploration.

- **Simulated Annealing (SA)**:  
  SA, on the other hand, focuses more on **exploitation**. It starts with a single solution and explores its neighborhood iteratively. While SA incorporates randomness through its temperature-based acceptance criteria, it lacks the population diversity of GA and is less likely to explore distant areas of the solution space. SA is more directed, making it faster at exploiting a promising region of the search space, but at the risk of getting stuck in local optima if the cooling schedule is not well-designed.



#### **Global vs. Local Optimization**:
- **Genetic Algorithm (GA)**:  
  GA is inherently designed for **global optimization**. By maintaining a diverse population and leveraging genetic operations, GA can escape local optima and search for global optima effectively. Its ability to combine features of different high-quality solutions (via crossover) allows it to discover novel and potentially better solutions that are not reachable through local search alone.

- **Simulated Annealing (SA)**:  
  SA is primarily a **local optimization** algorithm. While it has mechanisms to probabilistically escape local optima (through high-temperature acceptance of worse solutions), it lacks the ability to globally combine features from multiple solutions. This makes it more prone to converging to suboptimal solutions, especially if the temperature decreases too quickly or the neighborhood structure is limited.



#### **Scalability**:
- **Genetic Algorithm (GA)**:  
  GA is highly scalable and can handle **larger, more complex problems** effectively. Its population-based approach distributes the search across many candidates, making it more resilient to problem size and complexity. Additionally, the fitness evaluations for individual solutions can be parallelized, which significantly reduces computation time for large-scale problems.

- **Simulated Annealing (SA)**:  
  SA's performance tends to degrade as the problem size increases. Because SA explores the search space one solution at a time, the computational cost grows with the complexity of the neighborhood structure and the size of the solution space. Moreover, for larger problems, designing an effective cooling schedule becomes increasingly challenging, which can lead to either premature convergence or excessive computation time.



#### **Key Takeaways**:
- **Diversity and Exploration**: GA's population ensures broad exploration of the search space, whereas SA's single-solution approach limits its exploratory capabilities.
- **Optimization Capability**: GA is better suited for problems requiring global optimization, while SA excels in fine-tuning solutions within a specific region.
- **Complexity Handling**: GA scales well with problem complexity due to parallel evaluation and the population-based search, while SA struggles with larger or highly constrained problems.


#### Why We Chose Genetic Algorithm (GA)

Based on our experiments and analysis, **Genetic Algorithm (GA)** was chosen as the optimal approach for solving our problem because it consistently outperformed Simulated Annealing (SA) across key metrics such as space utilization, the total number of sheets used, and overall feasibility of solutions. Theoretical advantages of GA also aligned with the problem's requirements, further solidifying our choice.

#### **Results-Based Decision**:
- **Superior Metrics**: GA demonstrated higher sheet space utilization and required fewer sheets compared to SA. Its ability to effectively balance the constraints of spacing and boundaries with optimization goals resulted in better arrangements.
- **Consistency**: While SA occasionally produced good solutions, GA consistently found better ones due to its population-based approach, which allows for a broader exploration of possibilities.

#### **Theoretical Advantages**:
1. **Exploration of Solution Space**:  
   GA's population-based nature enables thorough exploration of the solution space. By evaluating multiple candidate solutions simultaneously, GA avoids getting stuck in local optima, a common issue with SA. This makes GA particularly effective for finding globally optimal arrangements.

2. **Global Optimization**:  
   GA's genetic operators, such as crossover and mutation, allow it to combine good traits from different solutions and introduce diversity, ensuring robust global search capabilities. This is crucial for problems like ours, where optimal placement of components requires significant exploration and adaptation.

3. **Scalability**:  
   GA is well-suited to handle the increasing complexity of larger orders and more diverse part arrangements. The parallel evaluation of candidates and adaptability to larger solution spaces make GA more efficient as problem size grows.

4. **Flexibility with Constraints**:  
   By incorporating constraints directly into its fitness function (e.g., penalties for overlaps or spacing violations), GA can dynamically adapt to complex rules while optimizing sheet usage. This flexibility is a key advantage over simpler approaches like SA, which may require additional post-processing to handle constraints.


#### **Summary**:
While **Simulated Annealing (SA)** is simpler and faster for smaller problems, **Genetic Algorithm (GA)** excels in tackling the complexities of our bin-packing optimization problem. Its ability to explore, adapt, and optimize on a global scale, combined with its superior performance on tested metrics, makes it the ideal choice for maximizing sheet utilization and minimizing the number of sheets used.

## Performance Comparison: Simulated Annealing (SA) vs. Genetic Algorithm (GA)

We evaluated both **Simulated Annealing (SA)** and **Genetic Algorithm (GA)** on the bin-packing optimization problem to determine their effectiveness in improving sheet space utilization. Below, we present the results and key observations for both algorithms.



### **Simulated Annealing (SA) Results**

- **Baseline Utilization (%):** 36.0542
- **Optimized Utilization (%):** 36.0542
- **Efficiency Improvement (%):** 0.0

#### **Key Observations**:
1. **Limited Improvement**:  
   Despite fine-tuning SA with parameters such as **MAX_TEMP = 10000**, **MIN_TEMP = 1**, and **COOLING_RATE = 0.99**, the algorithm failed to improve the baseline utilization. This indicates that SA struggled to explore alternative arrangements effectively.

2. **Local Search Limitation**:  
   SA's reliance on a single candidate solution and local adjustments made it difficult for the algorithm to escape the baseline configuration, resulting in zero efficiency improvement.

3. **Fast Convergence**:  
   SA converged quickly due to its straightforward cooling schedule, but the lack of exploration limited its ability to find better solutions.



### **Genetic Algorithm (GA) Results**

- **Baseline Utilization (%):** 36.0542
- **Optimized Utilization (%):** 45.6187
- **Efficiency Improvement (%):** 26.5280

#### **Key Observations**:
1. **Significant Improvement**:  
   With parameters such as **POPULATION_SIZE = 50**, **GENERATIONS = 100**, and **MUTATION_RATE = 0.1**, GA achieved a substantial increase in space utilization, improving efficiency by **26.53%** over the baseline.

2. **Robust Global Search**:  
   GA's population-based approach allowed it to explore a wide variety of arrangements, leveraging genetic operators (crossover and mutation) to combine and refine solutions. This global search capability was critical in discovering significantly better configurations.

3. **Adaptability to Constraints**:  
   GA incorporated constraints into its fitness function, effectively penalizing infeasible solutions. This ensured that all optimized results adhered to the problem's spacing and boundary requirements.


### **Comparison of Algorithms**

| **Metric**                      | **SA**                 | **GA**                 |
|---------------------------------|------------------------|------------------------|
| **Baseline Utilization (%)**    | 36.0542                | 36.0542                |
| **Optimized Utilization (%)**   | 36.0542                | 45.6187                |
| **Efficiency Improvement (%)**  | 0.0                    | 26.5280                |
| **Exploration**                 | Limited (local only)   | Broad (global search)  |
| **Adaptability to Constraints** | Moderate               | High                   |
| **Convergence Speed**           | Fast                   | Moderate               |



### **Conclusion**

- **Simulated Annealing (SA)**: SA was unable to improve the baseline solution due to its limited exploration capabilities. While it performed local optimization quickly, it lacked the tools to escape the baseline configuration effectively.
- **Genetic Algorithm (GA)**: GA delivered significantly better results, improving efficiency by 26.53%. Its ability to explore the global solution space, adapt to constraints, and evolve solutions over generations made it the superior choice for this optimization problem.
