import sys
import random
import time
import math

def parse_input_file(file_path):
    instances = []
    with open(file_path, 'r') as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            n = int(line)  # Número de itens
            G = int(f.readline().strip())  # Número de grupos
            capacity = int(f.readline().strip())  # Capacidade da mochila
            group_sizes = list(map(int, f.readline().strip().split()))  # Tamanhos dos grupos

            items = []
            for _ in range(n):
                line = f.readline().strip()
                if not line:
                    continue  # Pular linhas em branco
                l, p, g = map(int, line.split())
                items.append((l, p, g))

            instances.append((capacity, n, items))
    
    return instances

def evaluate_solution(solution, items, capacity):
    total_weight = sum(items[i][1] for i in range(len(solution)) if solution[i])
    
    if total_weight > capacity:
        return 0  # Solução inválida
    
    group_profits = {}
    for i, included in enumerate(solution):
        if included:
            l, _, g = items[i]
            if g not in group_profits:
                group_profits[g] = 0
            group_profits[g] += l
    
    if not group_profits:
        return 0
    
    min_profit = min(group_profits.values())
    return min_profit

def get_neighbor(solution):
    neighbor = solution[:]
    index = random.randint(0, len(solution) - 1)
    neighbor[index] = 1 - neighbor[index]
    return neighbor

def simulated_annealing(capacity, n, items, seed, max_iterations):
    random.seed(seed)
    current_solution = [random.randint(0, 1) for _ in range(n)]
    best_solution = current_solution[:]
    best_value = evaluate_solution(best_solution, items, capacity)
    
    T = 1.0
    T_min = 0.00001
    alpha = 0.9
    
    start_time = time.time()
    init_time = time.time()

    while T > T_min and max_iterations > 0:
        i = 1
        while i <= 100:
            neighbor = get_neighbor(current_solution)
            current_value = evaluate_solution(current_solution, items, capacity)
            neighbor_value = evaluate_solution(neighbor, items, capacity)
            
            if neighbor_value > current_value or random.uniform(0, 1) < math.exp((neighbor_value - current_value) / T):
                current_solution = neighbor[:]
                current_value = neighbor_value
                
                if current_value > best_value:
                    best_solution = current_solution[:]
                    best_value = current_value
                    elapsed_time = time.time() - start_time
                    print(f"{elapsed_time:.2f}s: Value={best_value}, Solution={best_solution}")
            
            i += 1
        
        T *= alpha
        max_iterations -= 1
        
    end_time = time.time() - init_time
    print(f"{end_time:.2f}s")

    return best_solution, best_value

def main():
    if len(sys.argv) < 4:
        print("Uso: python simulated_annealing.py <input_file> <seed> <max_iterations>")
        return
    
    input_file = sys.argv[1]
    seed = int(sys.argv[2])
    max_iterations = int(sys.argv[3])
    
    instances = parse_input_file(input_file)
    
    for idx, (capacity, n, items) in enumerate(instances):
        print(f"Instance {idx+1}:")
        best_solution, best_value = simulated_annealing(capacity, n, items, seed, max_iterations)
        print(f"Best Solution: {best_solution}")
        print(f"Best Value: {best_value}")
        print("")

if __name__ == "__main__":
    main()
