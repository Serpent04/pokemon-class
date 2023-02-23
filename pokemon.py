class Pokemon:

    def __init__(self, name, type, lvl=1):
        # Each pokemon has its name, level, type and health. New pokemon, by default, starts with level 1.
        # The type of a pokemon influences on its behavior, in this version specifically on damage.
        # Pokemon's health depends on its level, each level adds 25 hit points to the pokemon's health.
        # A pokemon with 0 health points is considered knocked out. Such pokemon can't function until its revived.
        self.name = name
        self.lvl = lvl
        self.type = type
        self.health = lvl * 25
        self.max_health = lvl * 25
        self.is_knocked_out = False

    def __repr__(self):
        return f'Name: {self.name}, Type: {self.type}, Current Health: {self.health}, Lvl: {self.lvl}'

    def lose_health(self, value):
        # As long as the pokemon is not knocked out it can lose health in various ways. This version supports
        # only losing health from getting attacked by another pokemon. Note, that as soon as the health is zero
        # pokemon's knocked-out status turns True.
        if self.is_knocked_out is True:
            print(f'{self.name} is knocked out!')
        else:
            self.health -= value
            if self.health <= 0:
                print(f'{self.name} now has 0 health')
                self.knock_out()
            else:
                print(f'{self.name} now has {self.health} health')

    def gain_health(self, value):
        # As long as the pokemon is not knocked out it can gain health in various ways. This version supports only
        # healing by the trainer with potions.
        self.health += value
        if self.health >= self.max_health:
            self.health = self.max_health
        if self.is_knocked_out is True:
            print(f'{self.name} is knocked out and must be revived')
        print (f'{self.name} now has {self.health} health')

    def knock_out(self):
        self.health = 0
        self.is_knocked_out = True
        print (f'{self.name} has been knocked out')

    def revive(self):
        # A knocked out pokemon can be revived with 1 hit point.
        if self.is_knocked_out is True:
            self.health = 1
            self.is_knocked_out = False
            print (f'{self.name} has been revived')

    def attack(self, other):
        # Forces other pokemon to lose health. Damage depends on the type of both attacking and attacked pokemons.
        # Pokemon can attack only if it's not knocked out.
        if other.is_knocked_out is False:
            if isinstance(other, Pokemon):
                # A pokemon's damage depends on its level, each level adds 2 damage points
                # to the pokemon's attack ability.
                damage = self.lvl * 2
                # If a pokemon has adventage over the pokemon it attacks in terms of types,
                # than the damage will be doubled.
                if (other.type == 'Grass' and self.type == 'Fire') \
                        or (other.type == 'Fire' and self.type == 'Water') \
                        or (other.type == 'Water' and self.type == 'Grass'):
                    print (f'{self.name} dealt {2 * damage} to {other.name}')
                    other.lose_health(2 * damage)
                # In opposite, the attacked pokemon has adventage in types, or both pokemons are of the same type,
                # than the damage will be halved.
                elif (other.type == 'Fire' and self.type == 'Grass') \
                        or (other.type == 'Water' and self.type == 'Fire') \
                        or (other.type == 'Grass' and self.type == 'Water') \
                        or (self.type == other.type):
                    print (f'{self.name} dealt {0.5 * damage} to {other.name}')
                    other.lose_health(0.5 * damage)
                # If no type adventage occurs, and the pokemons are of different types,
                # than the damage will be standard.
                else:
                    print (f'{self.name} dealt {damage} to {other.name}')
                    other.lose_health(damage)
        # A knocked out pokemon can't be attacked.
        else:
            print(f'{other.name} is already knocked out!')

class Trainer:

    def __init__(self, name: str, potions: int, pokemons: list, active_pokemon: int = 0):
        self.name = name
        self.potions = potions
        self.pokemons = pokemons
        self.active_pokemon = pokemons[active_pokemon]

    def __repr__(self):
        return f'Name: {self.name}, Active Pokemon: {self.active_pokemon.name}'

    def switch_active_pokemon(self, new_active):
        if new_active < len(self.pokemons) and new_active >= 0:
            # You can't switch to a pokemon that is knocked out
            if self.pokemons[new_active].is_knocked_out:
                print(f'{self.pokemons[new_active].name} is knocked out')
            # You can't switch to your current pokemon
            elif new_active == self.active_pokemon:
                print(f'{self.pokemons[new_active].name} is already your active pokemon')
            # Switches the pokemon
            else:
                self.active_pokemon = self.pokemons[new_active]
                print(f'{self.name}: {self.active_pokemon.name}, I choose you!')

    def use_potion(self):
        if self.potions >= 0:
            self.active_pokemon.gain_health(25)
            print(f'{self.active_pokemon.name}\'s health increased by 25 points')
            self.potions -= 1
        else:
            print('You are out of potions')

    def attack(self, other):
        if other.active_pokemon.is_knocked_out is False:
            if isinstance(other, Trainer):
                print(f'{self.name} attacks {other.name}!')
                self.active_pokemon.attack(other.active_pokemon)
        else:
            print(f'{other.name}\'s active pokemon is knocked out!')

class Charmander(Pokemon):
    def __init__(self, lvl = 1):
        super().__init__("Charmander", "Fire", lvl)

class Squirtle(Pokemon):
    def __init__(self, lvl = 1):
        super().__init__("Squirtle", "Water", lvl)

class Bulbasaur(Pokemon):
    def __init__(self, lvl = 1):
        super().__init__("Bulbasaur", "Grass", lvl)

# Six pokemon are made with different levels. (If no level is given, it is level 5)
a = Charmander(7)
b = Squirtle()
c = Squirtle(1)
d = Bulbasaur(10)
e = Charmander()
f = Squirtle(2)


#Two trainers are created. The first three pokemon are given to trainer 1, the second three are given to trainer 2.
trainer_one = Trainer("Alex", 3, [a,b,c])
trainer_two = Trainer("Sara", 5, [d,e,f])

print(trainer_one)
print(trainer_two)

# Testing attacking, giving potions, and switching pokemon.
trainer_one.attack(trainer_two)
trainer_two.attack(trainer_one)
trainer_two.use_potion()
trainer_one.attack(trainer_two)
trainer_two.switch_active_pokemon(0)
trainer_two.switch_active_pokemon(1)
trainer_two.switch_active_pokemon(0)
trainer_one.attack(trainer_two)
trainer_one.attack(trainer_two)
trainer_one.attack(trainer_two)
print(trainer_two.active_pokemon.health)
trainer_one.attack(trainer_two)
trainer_one.attack(trainer_two)
trainer_one.attack(trainer_two)
trainer_one.attack(trainer_two)
trainer_one.attack(trainer_two)
trainer_one.attack(trainer_two)
trainer_one.attack(trainer_two)
print(trainer_two.active_pokemon.is_knocked_out)
#trainer_two.use_potion()
#print(trainer_two.active_pokemon.health)