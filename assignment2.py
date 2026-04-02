import random

POPULATION_SIZE = 120
MAX_GENERATIONS = 300
MUTATION_RATE = 0.12
TOURNAMENT_SIZE = 4
ELITISM_COUNT = 2
RANDOM_SEED = 42

random.seed(RANDOM_SEED)

ZONE_CAPACITIES = {
    "Z1": 120, "Z2": 80, "Z3": 80, "Z4": 80,
    "Z5": 80, "Z6": 60, "Z7": 150, "Z8": 100,
}

ZONES = list(ZONE_CAPACITIES.keys())

PRODUCTS = [
    {"id": "P1", "name": "Glass Bottles", "weight": 20, "category": "Beverage", "fragile": True,  "hazardous": False, "temp_ctrl": False, "demand": "Medium"},
    {"id": "P2", "name": "Frozen Meat", "weight": 30, "category": "Food", "fragile": False, "hazardous": False, "temp_ctrl": True,  "demand": "High"},
    {"id": "P3", "name": "Cleaning Acid", "weight": 10, "category": "Chemical", "fragile": False, "hazardous": True,  "temp_ctrl": False, "demand": "Low"},
    {"id": "P4", "name": "Rice Bags", "weight": 50, "category": "Grocery", "fragile": False, "hazardous": False, "temp_ctrl": False, "demand": "High"},
    {"id": "P5", "name": "Ceramic Plates", "weight": 15, "category": "Kitchenware", "fragile": True,  "hazardous": False, "temp_ctrl": False, "demand": "Medium"},
    {"id": "P6", "name": "Ice Cream", "weight": 25, "category": "Food", "fragile": False, "hazardous": False, "temp_ctrl": True,  "demand": "High"},
    {"id": "P7", "name": "Detergent", "weight": 12, "category": "Chemical", "fragile": False, "hazardous": True,  "temp_ctrl": False, "demand": "Medium"},
    {"id": "P8", "name": "Chips Carton", "weight": 8,  "category": "Snacks", "fragile": False, "hazardous": False, "temp_ctrl": False, "demand": "High"},
    {"id": "P9", "name": "Olive Oil Bottles", "weight": 18, "category": "Grocery", "fragile": True,  "hazardous": False, "temp_ctrl": False, "demand": "Medium"},
    {"id": "P10", "name": "Industrial Bleach", "weight": 22, "category": "Chemical", "fragile": False, "hazardous": True,  "temp_ctrl": False, "demand": "Low"},
    {"id": "P11", "name": "Yogurt Cartons", "weight": 14, "category": "Food", "fragile": False, "hazardous": False, "temp_ctrl": True,  "demand": "High"},
    {"id": "P12", "name": "Flour Bags", "weight": 45, "category": "Grocery", "fragile": False, "hazardous": False, "temp_ctrl": False, "demand": "High"},
    {"id": "P13", "name": "Wine Bottles", "weight": 16, "category": "Beverage", "fragile": True,  "hazardous": False, "temp_ctrl": False, "demand": "Medium"},
    {"id": "P14", "name": "Paint Cans", "weight": 28, "category": "Chemical", "fragile": False, "hazardous": True,  "temp_ctrl": False, "demand": "Low"},
    {"id": "P15", "name": "Biscuit Boxes", "weight": 6,  "category": "Snacks", "fragile": False, "hazardous": False, "temp_ctrl": False, "demand": "High"},
    {"id": "P16", "name": "Motor Oil", "weight": 35, "category": "Chemical", "fragile": False, "hazardous": True,  "temp_ctrl": False, "demand": "Low"},
    {"id": "P17", "name": "Frozen Fish", "weight": 20, "category": "Food", "fragile": False, "hazardous": False, "temp_ctrl": True,  "demand": "High"},
    {"id": "P18", "name": "Bubble Wrap Rolls", "weight": 10, "category": "Packaging", "fragile": True,  "hazardous": False, "temp_ctrl": False, "demand": "Medium"},
    {"id": "P19", "name": "Wheat Sacks", "weight": 40, "category": "Grocery", "fragile": False, "hazardous": False, "temp_ctrl": False, "demand": "High"},
    {"id": "P20", "name": "Hand Sanitizer", "weight": 8,  "category": "Chemical", "fragile": True,  "hazardous": False, "temp_ctrl": False, "demand": "Medium"},
]

FOOD_PRODUCTS = {"Frozen Meat", "Ice Cream", "Yogurt Cartons", "Frozen Fish"}
CHEMICAL_PRODUCTS = {"Cleaning Acid", "Detergent", "Industrial Bleach", "Paint Cans", "Motor Oil", "Hand Sanitizer"}

Z8_ELIGIBLE_PRODUCTS = {
    product["name"]
    for product in PRODUCTS
    if product["temp_ctrl"] and product["demand"] == "High"
}

def create_random_chromosome():
    chromosome = []
    for product in PRODUCTS:
        if product["hazardous"]:
            preferred = ["Z5"]
        elif product["temp_ctrl"]:
            preferred = ["Z4", "Z8"]
        elif product["fragile"]:
            preferred = ["Z3"]
        elif product["weight"] > 40:
            preferred = ["Z1"]
        elif product["demand"] == "High":
            preferred = ["Z6", "Z1", "Z7", "Z2"]
        else:
            preferred = ZONES[:]

        if random.random() < 0.7:
            chromosome.append(random.choice(preferred))
        else:
            chromosome.append(random.choice(ZONES))
    return chromosome

def create_initial_population(size):
    return [create_random_chromosome() for _ in range(size)]

def evaluate_fitness(chromosome, return_details=False):
    total_penalty = 0
    details = []

    zone_weights = {z: 0 for z in ZONES}
    for i in range(len(PRODUCTS)):
        zone_weights[chromosome[i]] += PRODUCTS[i]["weight"]

    for z in ZONES:
        if zone_weights[z] > ZONE_CAPACITIES[z]:
            excess = zone_weights[z] - ZONE_CAPACITIES[z]
            total_penalty += excess * 2

    for i in range(len(PRODUCTS)):
        p = PRODUCTS[i]
        z = chromosome[i]

        if p["fragile"] and z != "Z3":
            total_penalty += 8
        if p["hazardous"] and z != "Z5":
            total_penalty += 10
        if p["temp_ctrl"] and z not in ["Z4", "Z8"]:
            total_penalty += 9
        if p["demand"] == "High" and z != "Z6":
            total_penalty += 5
        if p["weight"] > 40 and z != "Z1":
            total_penalty += 4
        if z == "Z8" and p["name"] not in Z8_ELIGIBLE_PRODUCTS:
            total_penalty += 12

    for i in range(len(PRODUCTS)):
        for j in range(i + 1, len(PRODUCTS)):
            if PRODUCTS[i]["category"] == PRODUCTS[j]["category"] and chromosome[i] != chromosome[j]:
                total_penalty += 3

    for i in range(len(PRODUCTS)):
        for j in range(len(PRODUCTS)):
            if PRODUCTS[i]["name"] in FOOD_PRODUCTS and PRODUCTS[j]["name"] in CHEMICAL_PRODUCTS:
                if chromosome[i] == chromosome[j]:
                    total_penalty += 15

    return (total_penalty, details) if return_details else total_penalty

def tournament_selection(pop, fitness):
    best = random.randint(0, len(pop)-1)
    for _ in range(TOURNAMENT_SIZE - 1):
        challenger = random.randint(0, len(pop)-1)
        if fitness[challenger] < fitness[best]:
            best = challenger
    return pop[best][:]

# 7.4 Crossover: single-point crossover
def crossover(p1, p2):
    point = random.randint(1, len(p1)-1)
    return p1[:point] + p2[point:], p2[:point] + p1[point:]

# 7.5 Mutation: randomly change zone
def mutate(chrom):
    for i in range(len(chrom)):
        if random.random() < MUTATION_RATE:
            chrom[i] = random.choice(ZONES)
    return chrom

def run_ga():
    pop = create_initial_population(POPULATION_SIZE)
    best = None
    best_fit = float("inf")

    for gen in range(MAX_GENERATIONS):
        fitness = [evaluate_fitness(c) for c in pop]

        for i in range(len(pop)):
            if fitness[i] < best_fit:
                best_fit = fitness[i]
                best = pop[i][:]

        if best_fit == 0:
            break

        new_pop = sorted(zip(pop, fitness), key=lambda x: x[1])
        new_pop = [x[0] for x in new_pop[:ELITISM_COUNT]]

        while len(new_pop) < POPULATION_SIZE:
            p1 = tournament_selection(pop, fitness)
            p2 = tournament_selection(pop, fitness)
            c1, c2 = crossover(p1, p2)
            new_pop.append(mutate(c1))
            if len(new_pop) < POPULATION_SIZE:
                new_pop.append(mutate(c2))

        pop = new_pop

    return best, best_fit, gen + 1

def print_plan(chrom):
    plan = {z: [] for z in ZONES}
    for i in range(len(PRODUCTS)):
        plan[chrom[i]].append(PRODUCTS[i]["name"])

    print("Optimal Storage Plan")
    for z in ZONES:
        print(z + ":", ", ".join(plan[z]) if plan[z] else "(empty)")

def main():
    best, fit, gens = run_ga()
    print_plan(best)
    print("\nBest Fitness:", fit)
    print("Generations:", gens)

if __name__ == "__main__":
    main()