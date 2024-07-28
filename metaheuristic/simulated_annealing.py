import sys
import random
import time

def parse_input_file(file_path):
    with open(file_path, 'r') as f:
        c = int(f.readline().strip())
        n = int(f.readline().strip())
        
        items = []
        for _ in range(n):
            l, p, g = map(int, f.readline().strip().split())
            items.append((l, p, g))
    
    return c, n, items

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
    
    while T > T_min and max_iterations > 0:
        i = 1
        while i <= 100:
            neighbor = get_neighbor(current_solution)
            current_value = evaluate_solution(current_solution, items, capacity)
            neighbor_value = evaluate_solution(neighbor, items, capacity)
            
            if neighbor_value > current_value or random.uniform(0, 1) < pow(2.71828, (neighbor_value - current_value) / T):
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
    
    return best_solution, best_value

def main():
    if len(sys.argv) < 4:
        print("Uso: python script.py <input_file> <seed> <max_iterations>")
        return
    
    input_file = sys.argv[1]
    seed = int(sys.argv[2])
    max_iterations = int(sys.argv[3])
    
    capacity, n, items = parse_input_file(input_file)
    
    best_solution, best_value = simulated_annealing(capacity, n, items, seed, max_iterations)
    
    print(f"Best Solution: {best_solution}")
    print(f"Best Value: {best_value}")

if __name__ == "__main__":
    main()
