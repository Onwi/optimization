using JuMP, HiGHS, Dates

model = Model(HiGHS.Optimizer)
set_optimizer_attribute(model, "presolve", "on")
set_optimizer_attribute(model, "time_limit", 60.0)

function read_instance(filename)
    open(filename, "r") do file
        n = parse(Int, readline(file))  # Número de itens
        G = parse(Int, readline(file))  # Número de grupos
        c = parse(Int, readline(file))  # Capacidade da mochila
        group_sizes = [parse(Int, x) for x in split(readline(file))]  # Tamanhos dos grupos
        weights = zeros(Int, n)
        profits = zeros(Int, n)

        for i in 1:n
            line = split(readline(file))
            weights[i] = parse(Int, line[1])
            profits[i] = parse(Int, line[2])
        end

        groups = Vector{Int}(undef, n)
        index = 1
        for g in 1:G
            for j in 1:group_sizes[g]
                groups[index] = g
                index += 1
            end
        end

        return n, G, c, group_sizes, weights, profits, groups
    end
end


function knapsack_sharing(file)
	n, G, c, group_sizes, weights, profits, groups = read_instance(file)

	#println(n)
	#println(G)
	#println(c)
	#println(group_sizes)
	#println(weights)
	#println(profits)
	#println(groups)
	
	@variable(model, x[1:n], Bin)
    @variable(model, z)

	# Restrição da capacidade da mochila
    @constraint(model, sum(weights[i] * x[i] for i in 1:n) <= c)
	
	# Faz java parecer lindo
    group_profits = [@expression(model, sum(profits[i] * x[i] for i in 1:n if groups[i] == g)) for g in 1:G]
    
	for g in 1:G
        @constraint(model, group_profits[g] >= z)
    end

	@objective(model, Max, z)
    optimize!(model)

	return objective_value(model)
end

for arg in ARGS
	start = now()
	result = knapsack_sharing(arg)
	
	println("tempo de execução: ", now() - start)
	println("Melhor solução encontrada: ", result)
end


