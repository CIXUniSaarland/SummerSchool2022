import random    
import numpy as np
import matplotlib.pyplot as plt 
import scipy.stats as ss
from ipywidgets import Output, Button, Label, HBox, VBox
from IPython.display import display

# times in minutes
# radius in cm
# temps in *c

# min, max, relative density
meat_temps = {"salmon":(49,60,0.7) , "steak":(55, 70,1.1), "shrimp":(61, 64,0.6), "chicken":(71, 90,1.0), "pork":(71, 85,1.1), "boar":(76, 81,1.2)}
init_temps = {"room temperature":20, "chilled":4, "frozen":-27}


def optimal_temps(meat):
    mn, mx, density = meat_temps[meat]
    temps = np.linspace(30, 100, 200)
    utility = meat_utility(temps, mn, mx)
    best = temps[np.argmax(utility)]
    undercooked = mn 
    overcooked = mx 
    return undercooked, best, overcooked


def expectation_cookedness(temps, meat):
    mn, mx, density = meat_temps[meat]
    return np.mean([meat_utility(t, mn, mx) for t in temps])
    
from threading import Thread, Event, Lock 
import time 

def create_game_ui(k):    
    game = CookingGame(k=k)
    cook_30 = Button(description="Cook 30")
    cook_30.on_click(lambda x: game.cook(30))
    cook_10 = Button(description="Cook 10")
    cook_10.on_click(lambda x: game.cook(10))
    cook_5 = Button(description="Cook 5")
    cook_5.on_click(lambda x: game.cook(5))
    cook_1 = Button(description="Cook 1")
    cook_1.on_click(lambda x: game.cook(1))
    serve = Button(description="Serve food!")
    serve.on_click(lambda x:game.serve())
    title_label = Label(value="You are cooking "+game.describe_food())
    temp_label = Label(value=game.describe_temp())    
    therm_label = Label(value='')

    out = Output()
    game.out = out

    game.therm_label = therm_label

    controls = HBox([cook_30, cook_10, cook_5, cook_1,  serve])
    panel = VBox([title_label, temp_label, therm_label, controls, out])
    display(panel)



class CookingGame:
    def __init__(self, k):
        self.therm_label = None
        self.k = k # thermometer smoothing
        self.chilled = random.choice(["room temperature", "chilled", "frozen"])        
        self.init_temp = init_temps[self.chilled]
        self.radius = random.uniform(2.5, 5.5)**2
        self.density = 0.9
        self.heat_capacity = 0.1
        self.oven_temp = np.random.randint(0, 5) * 10 + 150
        self.meat = random.choice(list(meat_temps.keys()))
        self.mass = get_mass(self.radius, self.density)
        self.density = 1.0
        self.cooking_time = 0
        self.thermometer_time = 0
        self.thermometer_temp = 20
        self.total_moves = 0
        self.room_temp = 20
        self.total_thermometer_time = 0
        
        self.thermometer_insert = np.random.uniform(self.radius/4, 3*self.radius/4)
        self.stopping = False
        self.score = 0
        self.out = None
        Thread(target=self.update_loop).start()

    def score_food(self):
        """Return the total thermometer time, the total number of moves,
        and the cookedness score"""
        distances = np.linspace(0, self.radius, 100)
        temps = food_model(self.radius, distances, self.init_temp, self.oven_temp, self.cooking_time, self.density, self.heat_capacity)
        goodness = expectation_cookedness(temps, self.meat)
        mn, mx, density = meat_temps[self.meat]
        over = np.max(temps-mx)
        under = np.min(temps-mn) 
        frozen = np.any(temps<0)
        return goodness, self.total_thermometer_time,  over, under, frozen

    def describe_temp(self):
        under, best, over = optimal_temps(self.meat)
        return f"{self.meat.title()} is best at {best:.0f}C. It is unsafe if any part is below {under:.0f}C and will be overcooked above {over:.0f}C"

    def describe_food(self):
        if self.mass>1000:
            mass = f"{self.mass/1000:.1f}kg"
        else:
            mass = f"{self.mass:.0f}g"

        return f"{mass} of {self.chilled} [{self.init_temp}C] {self.meat} in an oven at {self.oven_temp}C"
        
    def cook(self, minutes):
        self.thermometer_time = 0
        self.thermometer_temp = 20
        self.thermometer_insert = np.random.normal(self.radius, self.radius/3)
        self.cooking_time += minutes
        with self.out:
            print(f"[{self.cooking_time}m] You cook the {self.meat} for {minutes} minutes...")

  

    def serve(self):
        self.stopping = True
        goodness, t_time,  over, under, frozen = self.score_food()
        if self.out:
            with self.out:
                print("You serve the food.")
                print()
                if frozen:
                    print(f"The {self.meat} is still frozen!")
                    print("Guests can't even begin to eat the rock-hard food")
        

                if self.cooking_time==0:
                    print(f"You didn't even cook the {self.meat}!")
                    print("What are you doing?!")
                elif under>0 and over>0:
                    # check for overcookendess
                    if over>0 and over<25:
                        print(f"The {self.meat} is a bit tough")
                    elif  over<10 and over>=25:
                        print(f"The {self.meat} is a very tough and chewy")                
                        print("Guest struggle to finish their food.")
                    elif over>=25 and over<50:
                        print(f"The {self.meat} is a very overcooked")                
                    elif over>=50:
                        print(f"The {self.meat} is a burned to a crisp")                
                        print("Guests are seen picking at the cremated remains.")    
                elif under<0:
                    # under done
                    if under<0 and under>=-2:
                        print("The food is rather underdone.")
                        print(f"Some guests look a little unwell.")
                    elif under>=-5 and under<-10:
                        print("The food is undercooked.")
                        print(f"There is an outbreak of serious illness.")
                    elif under<=-10:
                        print("The food is severely undercooked.")
                        n_dead = np.random.randint(1, 10)
                        print(f"{n_dead} guests die of food poisoning")
                if under>0 and over<0:
                    print("The food is nicely cooked.")
                print()
                print(f"You spent {t_time:.0f} seconds staring at the thermometer.")
                print(f"Your food scored {100.0*goodness:.1f} points for cookedness.")
                score = (t_time * -1)  + goodness*500.0
                print()
                print(f"Your overall score is {score:.0f}.") 
                self.score = score
        
        return score

    def update_loop(self):
        for i in range(20_000):
            self.thermometer()
            time.sleep(1.0)
            if self.stopping:
                break
        

    def thermometer(self):
        # compute the measured temperature
        food_temp = food_model(self.radius, self.thermometer_insert, self.init_temp, self.oven_temp, self.cooking_time, self.density, self.heat_capacity)
        noise_level, beta = noise_latency(self.k)
        self.thermometer_temp = thermometer(food_temp, self.room_temp, self.thermometer_time, noise_level, beta)

        if self.therm_label!=None:
            if self.thermometer_time == 0.0:
                temp_label = "[--.-]"
            else:
                temp_label = f"[{self.thermometer_temp:.1f}C]"

            self.therm_label.value = f"{temp_label}. Cooked for {self.cooking_time} mins"
            self.thermometer_time += 1/60.0
            self.total_thermometer_time += 1/60.0
        


def meat_utility(temps, mn, mx):
    rnge = (mx-mn)
    ctr = (mx+mn)/2
    utility = np.where(temps<mn, -1*((mn-temps)**2), np.where(temps>mx, -0.45/rnge*((temps-mx)**2), 1-0.01*(temps-ctr)**2))
    return np.exp(utility/10.0)
    
    
def plot_chicken_curve(foods):
    fig, ax = plt.subplots()
    temps = np.linspace(40, 100, 200)
    mn, mx = foods["chicken"]    
    utility = meat_utility(temps, mn, mx)
    ax.plot(temps,utility, 'k')
    ax.axvline(65, ls=':', c='k')
    ax.axvline(70, ls=':', c='k')
    ax.axvline(80, ls=':', c='k')
    ax.axvline(90, ls=':', c='k')
    ax.text(60, 0.8, 'Dangerous', ha='center')
    ax.text(68, 0.8, 'Gooey', ha='center')
    ax.text(75, 0.8, 'Well cooked', ha='center')
    ax.text(85, 0.8, 'Overdone', ha='center')
    ax.text(95, 0.8, 'Burned', ha='center')
    
    ax.set_xlabel("Temp. C")
    ax.set_ylabel("Goodness")
    ax.set_title("Chicken internal temperature")

def noise_latency(k):
    k = (k**2) /25+ np.cos(k) 
    noise = np.exp(k/1.8-1.7-np.sin(k*3.1)*0.85) 
    return noise*10, k**2+0.2

    
def plot_utility_curves(foods):
    fig, ax = plt.subplots()
    temps = np.linspace(30, 100, 200)
    for food, (mn, mx, density) in foods.items():
        utility = meat_utility(temps, mn, mx)
        ax.plot(temps, utility, label=food)
    ax.legend()
    ax.set_xlabel("Temp. C") 
    ax.set_ylabel("Goodness")

def get_mass(radius, density):
    return 0.25 * radius ** 3.0 * density

def food_model(radius, insertion_depth, init_temp, cooking_temp, cooking_time, density, heat_capacity):
        mass = get_mass(radius, density)
        alpha = 1.0/((np.sqrt(mass)  * heat_capacity) * (abs(insertion_depth)+radius/2)+1+np.random.normal(0, 0.001))            
        temp = cooking_temp + (init_temp - cooking_temp) * np.exp(-alpha * cooking_time)
        
        temp = np.tanh(temp/120) * 120
        return temp

def thermometer(real_temp, init_temp, watch_time, noise_level, beta):
    beta = beta + np.random.normal(0, 0.2)
    temp = real_temp + (init_temp - real_temp) * np.exp(-beta * watch_time)
    temp = temp + np.random.normal(0, noise_level, temp.shape)
    return temp
    
    


def thermometer_model(radius, insertion_depth, init_temp, cooking_time, cooking_temp, watch_time, density, heat_capacity, noise_level, beta=5):    
    temp = food_model(radius, init_temp, cooking_temp, cooking_time, density, heat_capacity)
    thermo = thermometer_model(temp, init_temp, watch_time, noise_level, beta)
    return thermo


def cook():
    radius = np.random.uniform(9, 25)
    room_temp = 20
    density = 0.9
    heat_capacity = 0.01
    oven_temp = np.random.randint(0, 5) * 10 + 150
    meat = random.choice(list(meat_temps.keys()))
    mass = get_mass(radius, density)
    print(f"You are cooking {mass/1000:.1f}kg of {meat} in an oven at {oven_temp}C")
    for i in range(100):
        print(f"Time = {i} minutes")
        t = thermometer_model(radius, radius, room_temp, i, oven_temp, 1000.0, density, heat_capacity, 0.0)
        print(f"True internal temperature = {t:.0f}C")
        t = thermometer_model(radius, 0, room_temp, i, oven_temp, 1000.0, density, heat_capacity, 0.0)
        print(f"True surface temperature = {t:.0f}C")
        t = thermometer_model(radius, radius/2, room_temp, i, oven_temp, 0.5, density, heat_capacity, 0.1)
        print(f"Thermometer temperature at half-way = {t:.0f}C")
        
    
if __name__=="__main__":
    
    print(get_mass(10, 0.9))
    fig, ax = plt.subplots()
    times = np.linspace(0, 100, 200)
    t = thermometer_model(10, 0.0, 20.0, times, 180.0, 1.0, 0.9, 0.02, 1)
    ax.plot(times, t)
    
    
    plot_chicken_curve(meat_temps)
    plt.savefig("imgs/chicken_curve.png", bbox_inches="tight")
    plot_utility_curves(meat_temps)
    cook()
    