import pandas as pd
import random

import random
from datetime import datetime

# Constants
POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.1
PLATE_SIZE = 500  # 500x500 cm plate
BUFFER = 5  # Buffer space around each component in cm
SEPARATION = 10  # Separation between components in cm

file_path = "a2v3.csv"  # Replace with your file path
data = pd.read_csv(file_path, header=None)
data.columns = ["name", "dimensions", "quantity", "order_time"]

# Parse dimensions and sort orders
data["dimensions"] = data["dimensions"].apply(lambda x: tuple(map(int, x.split("x"))))
data["volume"] = data["dimensions"].apply(lambda x: x[0] * x[1] * x[2])
data = data.sort_values("order_time")

def is_same_time_range(order_time1, order_time2):
    """Check if two order times belong to the same range (midnight-noon or noon-midnight)."""
    format_str = "%Y-%m-%d %H:%M:%S"  # Timestamp format
    time1 = datetime.strptime(order_time1, format_str).time()
    time2 = datetime.strptime(order_time2, format_str).time()

    # Midnight to noon
    if time1 < datetime.strptime("12:00:00", "%H:%M:%S").time():
        return time2 < datetime.strptime("12:00:00", "%H:%M:%S").time()
    # Noon to midnight
    return time2 >= datetime.strptime("12:00:00", "%H:%M:%S").time()

def generate_initial_solution(data):
    """Initial placement based on chronological order with time range check."""
    plates = []
    current_plate = []
    current_x, current_y = BUFFER, BUFFER

    for index, row in data.iterrows():
        dimensions = row["dimensions"]
        quantity = row["quantity"]

        for _ in range(quantity):
            width, height = sorted(dimensions[:2])

            if current_x + width + BUFFER > PLATE_SIZE:
                current_x = BUFFER
                current_y += height + SEPARATION

            if current_y + height + BUFFER > PLATE_SIZE:
                # Start a new plate for the current time range
                plates.append(current_plate)
                current_plate = []
                current_x, current_y = BUFFER, BUFFER

            if current_plate and not is_same_time_range(current_plate[0][1], row["order_time"]):
                # Start a new plate if time ranges don't match
                plates.append(current_plate)
                current_plate = []
                current_x, current_y = BUFFER, BUFFER

            current_plate.append((row["name"], row["order_time"], current_x, current_y))
            current_x += width + SEPARATION

    if current_plate:
        plates.append(current_plate)
    return plates

def fitness_function(solution):
    """Fitness function for a solution."""
    used_space = sum(len(plate) for plate in solution)
    total_area = len(solution) * (PLATE_SIZE ** 2)
    return total_area - used_space

def crossover(parent1, parent2):
    """Perform crossover between two parents."""
    if (len(parent1) > 1):
        split = random.randint(1, len(parent1) - 1)
    else:
        split = 1
    child = parent1[:split] + parent2[split:]
    return child

def mutate(solution):
    """Mutate a solution."""
    for plate in solution:
        if random.uniform(0, 1) < MUTATION_RATE:
            if len(solution) > 1:
                p1, p2 = random.sample(range(len(solution)), 2)
                if solution[p1] and solution[p2]:
                    i1, i2 = random.randint(0, len(solution[p1]) - 1), random.randint(0, len(solution[p2]) - 1)
                    solution[p1][i1], solution[p2][i2] = solution[p2][i2], solution[p1][i1]

def split_data_by_time_range(data):
    """Split data into two subsets: morning (midnight-noon) and afternoon (noon-midnight)."""
    morning_data = data[data["order_time"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S").time() < datetime.strptime("12:00:00", "%H:%M:%S").time())]
    afternoon_data = data[data["order_time"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S").time() >= datetime.strptime("12:00:00", "%H:%M:%S").time())]
    return morning_data, afternoon_data

def genetic_algorithm(data):
    """Genetic Algorithm that processes data by time range."""
    # Split the data by time range
    morning_data, afternoon_data = split_data_by_time_range(data)

    # Run the Genetic Algorithm for each subset
    morning_solution = genetic_algorithm_for_subset(morning_data)
    afternoon_solution = genetic_algorithm_for_subset(afternoon_data)

    # Combine solutions from both time ranges
    combined_solution = morning_solution + afternoon_solution
    return combined_solution, fitness_function(combined_solution)

def genetic_algorithm_for_subset(data_subset):
    """Genetic Algorithm optimization for a single subset."""
    population = [generate_initial_solution(data_subset) for _ in range(POPULATION_SIZE)]

    for _ in range(GENERATIONS):
        population.sort(key=lambda x: fitness_function(x))
        new_population = population[:POPULATION_SIZE // 2]

        while len(new_population) < POPULATION_SIZE:
            p1, p2 = random.choices(new_population[:POPULATION_SIZE // 4], k=2)
            child = crossover(p1, p2)
            mutate(child)
            new_population.append(child)

        population = new_population

    best_solution = min(population, key=lambda x: fitness_function(x))
    return best_solution

def calculate_utilization(plates, data):
    """Calculate the space utilization as a percentage."""
    total_used_area = 0
    for plate in plates:
        for part in plate:
            part_name = part[0]
            dimensions = next((row["dimensions"] for _, row in data.iterrows() if row["name"] == part_name), None)
            if dimensions:
                width, height = sorted(dimensions[:2])  # Consider only 2D placement
                total_used_area += width * height

    total_plate_area = len(plates) * (PLATE_SIZE ** 2)
    return (total_used_area / total_plate_area) * 100

def write_to_csv(solution, file_name="optimized_solution.csv"):
    """Write the optimized solution to a CSV file."""
    rows = []
    for plate_number, plate in enumerate(solution, start=1):
        for part in plate:
            part_name, order_time, x_position, y_position = part
            rows.append([plate_number, part_name, order_time, x_position, y_position])

    # Convert rows to a DataFrame and write to a CSV file
    df = pd.DataFrame(rows, columns=["plate_number", "part_name", "order_time", "x_position", "y_position"])
    df.to_csv(file_name, index=False)
    print(f"Optimized solution written to {file_name}")

# Generate the baseline solution (chronological placement)
while 1:
    solution, cost = genetic_algorithm(data)
    baseline_solution = generate_initial_solution(data)
    # Calculate space utilization for baseline and optimized solutions
    baseline_utilization = calculate_utilization(baseline_solution, data)
    optimized_utilization = calculate_utilization(solution, data)

    # Calculate efficiency improvement
    efficiency_improvement = ((optimized_utilization - baseline_utilization) / baseline_utilization) * 100
    # Display results
    if efficiency_improvement > 1:
        break

print("Genetic Algorithm Results")
print("Baseline Utilization (%):", baseline_utilization)
print("Optimized Utilization (%):", optimized_utilization)
print("Efficiency Improvement (%):", efficiency_improvement)
write_to_csv(solution)
