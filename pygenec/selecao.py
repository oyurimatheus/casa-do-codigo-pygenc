from numpy import array, where
from numpy.random import random, choice


class Selecao:

    def __init__(self, populacao):
        self.populacao = populacao

    def selecionar(self, fitness):
        raise NotImplementedError('Metodo nao implementado')

    def selecao(self, tamanho_da_populacao, fitness=None):
        progenitores = array([self.selecionar(fitness)
                              for _ in range(tamanho_da_populacao)])
        return self.populacao.populacao[progenitores]


class Roleta(Selecao):

    def __init__(self, populacao):
        super(Roleta, self).__init__(populacao)

    def selecionar(self, fitness):
        if fitness is None:
            fitness = self.populacao.avaliar()

        fmin = fitness.min()
        fitness = fitness - fmin
        total = fitness.sum()

        parada = total * (1.0 - random())
        parcial = 0
        i = 0

        while True:
            if i > fitness.size - 1:
                break
            parcial += fitness[i]
            if parcial >= parada:
                break
            i += 1

        return i - 1


class Torneio(Selecao):

    def __init__(self, populacao, tamanho=10):
        super(Torneio, self).__init__(populacao)
        self.tamanho = tamanho

    def selecionar(self, fitness):
        if fitness is None:
            fitness = self.populacao.avaliar()

        grupo = choice(fitness, size=self.tamanho)

        campeao = grupo.max()

        i = where(fitness == campeao)[0][0]
        return i

