import random

wielkosc_populacji = 500
dlugosc_chromosomu = 14
ilosc_osobnikow_w_turnieju = 10
prawdopodobienstwo_mutacji = 0.001
prawdopodobienstwo_krzyzowania = 0.9
liczba_generacji = 50
zakres_x = (-50, 50)
srednie_przystosowania = []
najlepsze_przystosowania = []
pi = 3.141592

def randint(low, high, size):
    return [[random.randint(low, high) for _ in range(size[1])] for _ in range(size[0])]

def random_float():
    return random.random()

def create_array(data):
    if isinstance(data, list):
        return [create_array(element) for element in data]
    else:
        return data

def infinite():
    return float('inf')

def mean(data):
    if isinstance(data[0], list):
        flattened_data = [item for sublist in data for item in sublist]
        return sum(flattened_data) / len(flattened_data)
    else:
        return sum(data) / len(data)

def minimum(values):
    return min(values)

def argmin(values):
    return values.index(min(values))

def silnia(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * silnia(n - 1)

def sin(x, n_terms=10):
    sin_x = 0
    for n in range(n_terms):
        term = (-1)**n * x**(2 * n + 1) / silnia(2 * n + 1)
        sin_x += term
    return sin_x

def cos(x, n=20):
    x = x % (2 * pi)  
    suma = 0
    for i in range(n):
        term = (-1) ** i * x ** (2 * i) / silnia(2 * i)
        suma += term
    return suma



population = randint(0, 1, (wielkosc_populacji, dlugosc_chromosomu))

def dekoduj(chromosom, zakres_x, dlugosc_chromosomu):
    mid = dlugosc_chromosomu // 2

    max_bin_value = 2**mid - 1 

    x1_value = sum(bit * (2 ** i) for i, bit in enumerate(reversed(chromosom[:mid])))
    x2_value = sum(bit * (2 ** i) for i, bit in enumerate(reversed(chromosom[mid:])))

    x1 = x1_value / max_bin_value * (zakres_x[1] - zakres_x[0]) + zakres_x[0]
    x2 = x2_value / max_bin_value * (zakres_x[1] - zakres_x[0]) + zakres_x[0]

    return x1, x2

for i in population:
    print(dekoduj(i,(-50,50), 14))

def funkcja_przystosowania(chromosom):

    x1, x2 = dekoduj(chromosom, zakres_x, dlugosc_chromosomu)
    return (x1**2) + (2*x2**2) - (0.3 * np.cos(3 * np.pi * x1)) - (0.4 * np.cos(4 * np.pi * x2)) + 0.7


def selekcja_turniejowa(population, funkcja_przystosowania, tournament_size):
    wyniki_losowania = []
    for i in range(tournament_size):
        wylosowany = random.randint(0, (len(population)-1))
        wyniki_losowania.append(population[wylosowany])

    najlepszy_osobnik = None
    naj_przystosowanie = []
    for j in range(tournament_size):
        naj_przystosowanie.append(funkcja_przystosowania(wyniki_losowania[j]))

    najlepszy_osobnik = min(naj_przystosowanie)
    index = naj_przystosowanie.index(najlepszy_osobnik)
    wybrany_osobnik = wyniki_losowania[index]
    
    return wybrany_osobnik

def krzyzowanie_jednorodne(parent1, parent2):
    offspring = []
    for i in range(dlugosc_chromosomu):
        if random_float() < 0.5:
            offspring.append(parent1[i])
        else:
            offspring.append(parent2[i])
    return create_array(offspring)

def mutacja_losowa(chromosome, mutation_rate):
    for i in range(len(chromosome)):
        random_number = random_float()
        if random_number < mutation_rate:
            if chromosome[i] == 0:
                chromosome[i] = 1
            else:
                chromosome[i] = 0
    return chromosome


for generation in range(liczba_generacji):
    new_population = []
    while len(new_population) < wielkosc_populacji:

        parent1 = selekcja_turniejowa(population, funkcja_przystosowania, ilosc_osobnikow_w_turnieju)
        parent2 = selekcja_turniejowa(population, funkcja_przystosowania, ilosc_osobnikow_w_turnieju)
        if random_float() < prawdopodobienstwo_krzyzowania:
            nowe_pokolenie_1 = krzyzowanie_jednorodne(parent1, parent2)
            nowe_pokolenie_2 = krzyzowanie_jednorodne(parent1, parent2)
        else:
            nowe_pokolenie_1, nowe_pokolenie_2 = parent1, parent2
        

        nowe_pokolenie_1 = mutacja_losowa(nowe_pokolenie_1, prawdopodobienstwo_mutacji)
        nowe_pokolenie_2 = mutacja_losowa(nowe_pokolenie_2, prawdopodobienstwo_mutacji)
        
        new_population.append(nowe_pokolenie_1)
        new_population.append(nowe_pokolenie_2)
    
    population = create_array(new_population[:wielkosc_populacji])
    
    fitness_scores = create_array([funkcja_przystosowania(individual) for individual in population])
    
    srednie_przystosowanie = mean(fitness_scores)
    najlepsze_przystosowanie = min(fitness_scores)
    srednie_przystosowania.append(srednie_przystosowanie)
    najlepsze_przystosowania.append(najlepsze_przystosowanie)
    
    print(f"Generacja {generation}: Średnie Przystosowanie {srednie_przystosowanie}, Najlepsze Przystosowanie {najlepsze_przystosowanie}")

najlepszy_osobnik = population[argmin(fitness_scores)]
najlepsza_wartosc = funkcja_przystosowania(najlepszy_osobnik)

#print(populacje)
import matplotlib.pyplot as plt

print("\nNajlepsze znalezione rozwiązanie:")
print("Argument (chromosom):", najlepszy_osobnik)
dekodowane_wartosci = dekoduj(najlepszy_osobnik, (-50, 50), 14)
#print("Dekodowane wartości (zaokrąglone):", (round(dekodowane_wartosci[0], 2), round(dekodowane_wartosci[1], 2)))
print("Dekodowane wartości (zaokrąglone):", dekoduj(najlepszy_osobnik, (-50, 50), 14))
print("Wartość funkcji przystosowania:", najlepsza_wartosc)

fig, ax1 = plt.subplots(figsize=(10, 5))

color = 'tab:blue'
ax1.set_xlabel('Generacja')
ax1.set_ylabel('Średnie przystosowanie', color=color)
ax1.plot(srednie_przystosowania, label='Średnie przystosowanie', color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx() 
color = 'tab:red'
ax2.set_ylabel('Najlepsze przystosowanie', color=color) 
ax2.plot(najlepsze_przystosowania, label='Najlepsze przystosowanie', color=color, linestyle='--')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Średnie i najlepsze przystosowanie w kolejnych generacjach')
fig.tight_layout() 
fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
plt.show()



