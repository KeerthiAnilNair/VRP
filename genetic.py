import random
import timeit
start = timeit.default_timer()

def generate_random_solution(num_nodes, num_vehicles, vehicle_capacity, demands):
    # Initialize variables
    depot = 0  # Assuming the depot is at index 0
    remaining_capacity = [vehicle_capacity] * num_vehicles
    solution = [[] for _ in range(num_vehicles)]
    unassigned_nodes = list(range(1, num_nodes))  # Nodes excluding depot

    # Main loop to generate the solution
    for i in range(num_vehicles):
        solution[i].append(0)
    while unassigned_nodes:
        current_vehicle = random.randint(0, num_vehicles - 1)
        current_node = depot  # Start from the depot

        promising_nodes = [node for node in unassigned_nodes if demands[node] <= remaining_capacity[current_vehicle]]
       
        if not promising_nodes:
            # If no promising nodes, return to the depot and start a new route
            continue

        selected_node = random.choice(promising_nodes)
        solution[current_vehicle].append(selected_node)

        # Update remaining capacity and remove the selected node from unassigned nodes
        remaining_capacity[current_vehicle] -= demands[selected_node]
        unassigned_nodes.remove(selected_node)

    for i in range(num_vehicles):
        solution[i].append(0)
    return solution



def calculate_route_distance(vehicle_route,data):
    distance=0
    for i in range(1,len(vehicle_route)):
        x=vehicle_route[i-1]
        y=vehicle_route[i]
        distance+=data[x][y]
    return distance

def calculate_route_capacity(vehicle_route,stop_capacity):
    total_capacity=0
    for stop in vehicle_route:
        total_capacity+=stop_capacity[stop]
    return total_capacity

def calculate_fitness(solution,data,stop_capacity,buses,bus_capacity):
    total_distance = 0
    total_capacity_violation = 0
    i=0
    for vehicle_route in solution:
        route_distance = calculate_route_distance(vehicle_route,data)
        i+=1
        total_distance += route_distance
        route_capacity = calculate_route_capacity(vehicle_route,stop_capacity)
        print("Capacity of bus ",i," : ",route_capacity)
        if route_capacity > bus_capacity:
           
            total_capacity_violation += (route_capacity - bus_capacity) * 99
    
    #print(total_capacity_violation,total_distance)
    fitness = total_distance + total_capacity_violation
    return fitness


def main():
    data=[[0, 5, 8, 6, 7, 3],  
    [5, 0, 4, 2, 7, 1],
    [8, 4, 0, 3, 6, 2], 
    [6, 2, 3, 0, 5, 2], 
    [7, 7, 6, 5, 0, 4],  
    [3, 1, 2, 2, 4, 0]]
    buses=3
    no_of_nodes=6
    stop_capacity=[0, 4, 2, 4, 8, 8]
                # 0, 1, 2, 3, 4, 5
    bus_capacity=10
    initial_sol=generate_random_solution(no_of_nodes,buses,10,stop_capacity)
    print("\n\tGENETIC ALGORITHM\n")
    print("Initial Solution : ",initial_sol)
    fitness=calculate_fitness(initial_sol,data,stop_capacity,buses,bus_capacity)
    print("Cost : ",fitness)
    stop = timeit.default_timer()
    elapsed_time = stop - start
    elapsed_time_str = "{:.8f}".format(elapsed_time)
    print("Execution Time:", elapsed_time_str, "seconds\n")


if __name__ == "__main__":
    main()
    