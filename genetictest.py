import random
import copy
import timeit

start = timeit.default_timer()

def generate_random_solution(num_nodes, num_vehicles, vehicle_capacity, demands):
    depot = 0
    remaining_capacity = [vehicle_capacity] * num_vehicles
    solution = [[] for _ in range(num_vehicles)]
    unassigned_nodes = list(range(1, num_nodes))

    for i in range(num_vehicles):
        solution[i].append(0)

    while unassigned_nodes:
        current_vehicle = random.randint(0, num_vehicles - 1)
        current_node = depot

        promising_nodes = [node for node in unassigned_nodes if demands[node] <= remaining_capacity[current_vehicle]]

        if not promising_nodes:
            continue

        selected_node = random.choice(promising_nodes)
        solution[current_vehicle].append(selected_node)

        remaining_capacity[current_vehicle] -= demands[selected_node]
        unassigned_nodes.remove(selected_node)

    for i in range(num_vehicles):
        solution[i].append(0)

    return solution

def apply_mutation(solution, mutation_rate, demands, stop_capacity):
    mutated_solution = copy.deepcopy(solution)

    for i in range(len(mutated_solution)):
        if random.uniform(0, 1) < mutation_rate and len(mutated_solution[i]) > 3:
            idx1, idx2 = random.sample(range(1, len(mutated_solution[i]) - 1), 2)
            mutated_solution[i][idx1], mutated_solution[i][idx2] = mutated_solution[i][idx2], mutated_solution[i][idx1]

    remaining_capacity = [sum(stop_capacity[stop] for stop in route) for route in mutated_solution]
    unassigned_nodes = list(range(1, len(demands)))

    for i in range(len(mutated_solution)):
        route_capacity = sum(stop_capacity[stop] for stop in mutated_solution[i])
        remaining_capacity[i] -= route_capacity
        unassigned_nodes = [node for node in unassigned_nodes if node not in mutated_solution[i]]

    while unassigned_nodes:
        for i in range(len(mutated_solution)):
            if not unassigned_nodes:
                break
            selected_node = random.choice(unassigned_nodes)
            mutated_solution[i].insert(-1, selected_node)
            route_capacity = sum(stop_capacity[stop] for stop in mutated_solution[i])
            remaining_capacity[i] -= demands[selected_node]
            unassigned_nodes.remove(selected_node)

    return mutated_solution

def calculate_route_distance(vehicle_route, data):
    distance = 0
    for i in range(1, len(vehicle_route)):
        x = vehicle_route[i - 1]
        y = vehicle_route[i]
        distance += data[x][y]
    # Include the distance from the last stop to the depot
    distance += data[vehicle_route[-1]][vehicle_route[0]]
    return distance

def calculate_route_capacity(vehicle_route, stop_capacity):
    total_capacity = sum(stop_capacity[stop] for stop in vehicle_route)
    return total_capacity

def calculate_fitness(solution, data, stop_capacity, buses, bus_capacity):
    total_distance = 0
    total_capacity_violation = 0

    for i, vehicle_route in enumerate(solution):
        route_distance = calculate_route_distance(vehicle_route, data)
        total_distance += route_distance

        route_capacity = calculate_route_capacity(vehicle_route, stop_capacity)
        print("Capacity of bus ", i + 1, ":", route_capacity)

        if route_capacity > bus_capacity:
            total_capacity_violation += (route_capacity - bus_capacity) * 99

    fitness = total_distance + total_capacity_violation
    return fitness

def display_solution(solution, fitness):
    print("Routes:", solution)
    print("Cost:", fitness)
    print()

def main():
    data = [
        [0, 5, 8, 6, 7, 3],
        [5, 0, 4, 2, 7, 1],
        [8, 4, 0, 3, 6, 2],
        [6, 2, 3, 0, 5, 2],
        [7, 7, 6, 5, 0, 4],
        [3, 1, 2, 2, 4, 0]
    ]
    buses = 3
    no_of_nodes = 6
    stop_capacity = [0, 4, 2, 4, 8, 8]
    bus_capacity = 10

    initial_sol = generate_random_solution(no_of_nodes, buses, 10, stop_capacity)
    print("\n\tGENETIC ALGORITHM\n")
    print("Initial Solution:", initial_sol)

    fitness = calculate_fitness(initial_sol, data, stop_capacity, buses, bus_capacity)
    display_solution(initial_sol, fitness)

    num_generations = 10
    solutions = [initial_sol]

    for generation in range(num_generations):
        # Selection and crossover
        print(f"Generation {generation}")
        ranked_solutions = [(calculate_fitness(sol, data, stop_capacity, buses, bus_capacity), sol) for sol in solutions]
        ranked_solutions.sort()
        best_solutions = [sol[1] for sol in ranked_solutions[:100]]

        for i, sol in enumerate(best_solutions):
            fitness = calculate_fitness(sol, data, stop_capacity, buses, bus_capacity)
            display_solution(sol, fitness)

        new_gen = []
        for _ in range(10):
            parent1, parent2 = random.choice(best_solutions), random.choice(best_solutions)
            crossover_point = random.randint(1, 2)
            child = (parent1[0], parent2[1], parent1[2])  # Example crossover, you can modify as needed

            # Mutation
            child = apply_mutation(child, mutation_rate=0.01, demands=stop_capacity, stop_capacity=stop_capacity)

            new_gen.append(child)

        # Update population
        solutions = new_gen

    stop = timeit.default_timer()
    elapsed_time = stop - start
    elapsed_time_str = "{:.8f}".format(elapsed_time)
    print("Execution Time:", elapsed_time_str, "seconds\n")

if __name__ == "__main__":
    main()
