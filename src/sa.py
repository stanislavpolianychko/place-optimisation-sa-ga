from datetime import datetime
import pandas as pd
import random
import math

# Load the data
file_path = "a2v3.csv"  # Replace with your file path
data = pd.read_csv(file_path, header=None)
data.columns = ["name", "dimensions", "quantity", "order_time"]

# Parse dimensions and sort orders
data["dimensions"] = data["dimensions"].apply(lambda x: tuple(map(int, x.split("x"))))
data["volume"] = data["dimensions"].apply(lambda x: x[0] * x[1] * x[2])
data = data.sort_values("order_time")

# Precompute dimensions lookup
dimensions_lookup = {row["name"]: sorted(row["dimensions"][:2]) for _, row in data.iterrows()}
# Initialize constants
PLATE_SIZE = 500  # 500x500 cm plate
BUFFER = 5  # Buffer space around each component in cm
SEPARATION = 10  # Separation between components in cm
MAX_TEMP = 1000
MIN_TEMP = 1
COOLING_RATE = 0.99

# Helper function to determine time range
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


def neighbor_solution(plates):
    """Generate a neighbor solution with optimized moves."""
    new_plates = [plate[:] for plate in plates]  # Deep copy of the current arrangement

    if len(new_plates) > 1:
        plate_index = random.randint(0, len(new_plates) - 1)
        if new_plates[plate_index]:
            # Step 1: Swap two parts within the same plate
            if len(new_plates[plate_index]) > 1:
                p1, p2 = random.sample(range(len(new_plates[plate_index])), 2)
                new_plates[plate_index][p1], new_plates[plate_index][p2] = (
                    new_plates[plate_index][p2],
                    new_plates[plate_index][p1],
                )

        # Step 2: Attempt to move one part from the next plate
        if plate_index < len(new_plates) - 1 and new_plates[plate_index + 1]:
            part = random.choice(new_plates[plate_index + 1])
            if is_same_time_range(new_plates[plate_index][0][1], part[1]):
                if can_fit_in_plate(new_plates[plate_index], part):
                    new_plates[plate_index].append(part)
                    new_plates[plate_index + 1].remove(part)

        # Remove empty plates
        new_plates = [plate for plate in new_plates if plate]

    return new_plates



def can_fit_in_plate(plate, part):
    """Check if a part can be added to a plate without violating constraints."""
    part_name, _, part_x, part_y = part
    width, height = dimensions_lookup[part_name]

    # Check for overlap with existing parts on the plate
    for existing_part in plate:
        existing_name, _, existing_x, existing_y = existing_part
        existing_width, existing_height = dimensions_lookup[existing_name]

        # Check overlap
        if not (
            part_x + width + BUFFER <= existing_x or  # To the left
            part_x >= existing_x + existing_width + BUFFER or  # To the right
            part_y + height + BUFFER <= existing_y or  # Above
            part_y >= existing_y + existing_height + BUFFER  # Below
        ):
            return False  # Overlaps with an existing part

    return True  # No overlaps, can fit


def calculate_cost(plates):
    """Cost function based on the number of plates used and wasted space."""
    used_space = sum(len(plate) for plate in plates)
    total_area = len(plates) * (PLATE_SIZE ** 2)
    return total_area - used_space

def simulated_annealing(data):
    """Simulated annealing optimization."""
    current_solution = generate_initial_solution(data)
    current_cost = calculate_cost(current_solution)
    best_solution, best_cost = current_solution, current_cost
    temp = MAX_TEMP

    while temp > MIN_TEMP:
        new_solution = neighbor_solution(current_solution)
        new_cost = calculate_cost(new_solution)
        if new_cost < current_cost or random.uniform(0, 1) < math.exp((current_cost - new_cost) / temp):
            current_solution, current_cost = new_solution, new_cost
            if new_cost < best_cost:
                best_solution, best_cost = new_solution, new_cost
        temp *= COOLING_RATE * 1.01  # Faster cooling

    return best_solution, best_cost



def calculate_utilization(plates, dimensions_lookup):
    """Calculate the space utilization as a percentage."""
    total_used_area = 0
    for plate in plates:
        for part in plate:
            part_name = part[0]
            width, height = dimensions_lookup[part_name]  # Use precomputed dimensions
            total_used_area += width * height

    total_plate_area = len(plates) * (PLATE_SIZE ** 2)
    return (total_used_area / total_plate_area) * 100


def write_to_csv(solution, file_name="optimized_solution1.csv"):
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

# Run the optimized Simulated Annealing
# Generate the baseline solution (chronological placement)
baseline_solution = generate_initial_solution(data)

# Run Simulated Annealing
optimized_solution, optimized_cost = simulated_annealing(data)

# Calculate space utilization for baseline and optimized solutions
baseline_utilization = calculate_utilization(baseline_solution, dimensions_lookup)
optimized_utilization = calculate_utilization(optimized_solution, dimensions_lookup)

# Calculate efficiency improvement
efficiency_improvement = ((optimized_utilization - baseline_utilization) / baseline_utilization) * 100

# Display results
print("Simulated Annealing Results")
print("Number of plates used (Baseline):", len(baseline_solution))
print("Number of plates used (Optimized):", len(optimized_solution))
print("Baseline Utilization (%):", baseline_utilization)
print("Optimized Utilization (%):", optimized_utilization)
print("Efficiency Improvement (%):", efficiency_improvement)
write_to_csv(optimized_solution)