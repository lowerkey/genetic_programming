# Genetic Programming
# This weekend, I was introduced to genetic programming. Following the tutorial,
# I ran a simulation to evolve the string "Hello, Worlds!".

# Thanks, http://burakkanber.com/blog/machine-learning-genetic-algorithms-in-javascript-part-2/

from random import random

class Gene():
    def __init__(self, code):
        self.code = code
        self.cost = 9999

    def mate(self, gene):
        return [Gene(self.code[:len(self.code)/2] + gene.code[len(self.code)/2:]),
                Gene(gene.code[:len(self.code)/2] + self.code[len(self.code)/2:])]

    def mutate(self, chance):
        if random() < chance:
            return

        code = ''
        index = int(random() * len(self.code))
        for i in range(len(self.code)):
            upOrDown = -1 if round(random()) else 1
            if i == index:
                code += chr(ord(self.code[i]) + upOrDown)
            else:
                code += self.code[i]

        self.code = code

    def calcCost(self, target):
        total = 0
        for i in range(len(self.code)):
            total += (ord(self.code[i]) - ord(target[i])) * (ord(self.code[i]) - ord(target[i]))

        self.cost = total


class Population():
    def __init__(self, target, size):
        self.target = target
        self.members = []
        for i in range(size):
            self.members.append(Gene("A" * len(self.target)))
        self.generationNumber = 0

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
        print "Generation", self.generationNumber, self.members[0].code, self.members[0].cost
        self.calcCosts()
        self.sort()

    def generation(self, display):
        while not self._generation(display):
            pass

        return self.generationNumber

    def _generation(self, display):
        self.calcCosts()
        self.sort()
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
    gene2 = Gene("BBBBBBBBBBBBBB")
    children = gene1.mate(gene2)
    for child in children:
        child.calcCost("Hello, Worlds!")
        print child.code, child.cost

    generationNumbers = []
    for i in range(10):
        population = Population("Hello, Worlds!", 1000)
        generationNumbers.append(population.generation(False))
        print i, population.generationNumber
    print generationNumbers
