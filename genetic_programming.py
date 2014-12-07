# Genetic Programming
# This weekend, I was introduced to genetic programming. Following the tutorial,
# I ran a simulation to evolve the string "Hello, Worlds!".

# Thanks, http://burakkanber.com/blog/machine-learning-genetic-algorithms-in-javascript-part-2/

from random import random
from math import floor

class Gene():
    def __init__(self, code):
        self.code = code
        self.cost = 9999

    def mate(self, gene):
        middle = int(floor(len(self.code)/2))
        return [Gene(self.code[:middle] + gene.code[middle:]),
                Gene(gene.code[:middle] + self.code[middle:])]

    def mutate(self, chance):
        if random() < chance:
            return

        code = ''
        index = round(random() * len(self.code))
        for i in range(len(self.code)):
            upOrDown = -1 if round(random()) else 1
            if i == index and ord(self.code[i]) + upOrDown < 256 and ord(self.code[i]) > 0:
                code += chr(ord(self.code[i]) + upOrDown)
            else:
                code += self.code[i]

        self.code = code

    def random(self, length):
        code = ''
        for i in range(length):
            code += chr(int(random()*255))
        self.code = code

    def calcCost(self, target):
        total = 0
        for i in range(len(self.code)):
            total += (ord(self.code[i]) - ord(target[i])) * (ord(self.code[i]) - ord(target[i]))

        self.cost = total


class Population():
    def __init__(self, target, size, log_costs):
        self.target = target
        self.members = []
        for i in range(size):
            gene = Gene('')
            gene.random(len(self.target))
            self.members.append(gene)
        self.generationNumber = 0
        
        self.log_costs = log_costs
        if self.log_costs:
            self.cost_log = [] # logs the cost of the highest ranking member
        
    def calcCosts(self):
        for member in self.members:
            member.calcCost(self.target)

    def mutate(self, chance):
        for member in self.members:
            member.mutate(chance)

    # Should be called after Population.calcCosts()
    def sort(self):
        self.members = sorted(self.members, key=lambda member: member.cost)

    def display(self):
        self.calcCosts()
        self.sort()
        print "Generation", self.generationNumber, self.members[0].code, self.members[0].cost

    def generation(self, display):
        while not self._generation(display):
            pass
            
        if self.log_costs:
            return self.cost_log
        else:
            return self.generationNumber
        
    def _generation(self, display):
        self.calcCosts()
        self.sort()
        if self.log_costs:
            self.cost_log.append(self.members[0].cost)
        if display:
            self.display()

        children = self.members[0].mate(self.members[1])
        self.members[-2] = children[0]
        self.members[-1] = children[1]

        for member in self.members:
            member.mutate(0.5)
            member.calcCost(self.target)
            if member.code == self.target:
                self.sort()
                if display:
                    self.display()
                return True

        self.generationNumber += 1
        return False

if __name__ == '__main__':
    gene1 = Gene("AAAAAAAAAAAAAA")
    gene2 = Gene("AAAAAAAAAAAAAA")
    children = gene1.mate(gene2)
    for child in children:
        child.calcCost("Hello, Worlds!")
        print child.code, child.cost

    population = Population("Hello, Worlds!", size=100, log_costs=True)
    population.generation(display=True)
    print population.cost_log
