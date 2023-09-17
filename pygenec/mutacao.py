from numpy import array
from numpy.random import random, randint, shuffle


class Mutacao:

    def __init__(self, probabilidade_mutacao):
        self.probabilidade_mutacao = probabilidade_mutacao
        self._populacao = None
        self.tamanho_populacao = None
        self.numero_genes = None

    @property
    def populacao(self):
        return self._populacao

    @populacao.setter
    def populacao(self, populacao):
        self._populacao = populacao
        self.tamanho_populacao = self._populacao.shape[0]
        self.numero_genes = self._populacao.shape[1]

    def selecao(self):
        return array([i for i in range(self.tamanho_populacao)
                      if random() < self.probabilidade_mutacao])

    def mutacao(self):
        raise NotImplementedError("A ser implementado")


class Flip(Mutacao):

    def __init__(self, probabilidade_mutacao):
       super(Flip, self).__init__(probabilidade_mutacao)

    def mutacao(self):
        individuos_a_mutarem = self.selecao()
        gene_a_ser_flipado = array([randint(0, self.numero_genes - 1) for _ in individuos_a_mutarem])
        self.populacao[individuos_a_mutarem, gene_a_ser_flipado] = 1 - self.populacao[individuos_a_mutarem, gene_a_ser_flipado]


class DuplaTroca(Mutacao):

    def __int__(self, probabilidade_mutacao):
        super(DuplaTroca, self).__init__(probabilidade_mutacao)

    def mutacao(self):
        individuos_a_mutarem = self.selecao()
        gen1 = array([randint(0, self.numero_genes - 1)])
        gen2 = array([randint(0, self.numero_genes - 1)])
        self.populacao[individuos_a_mutarem, gen1], self.populacao[individuos_a_mutarem, gen2] = self.populacao[individuos_a_mutarem, gen2], self.populacao[individuos_a_mutarem, gen1]


class SequenciaReversa(Mutacao):

    def __int__(self, probabilidade_mutacao):
        super(SequenciaReversa, self).__init__(probabilidade_mutacao)

    def mutacao(self):
        individuos_a_mutarem = self.selecao()

        if individuos_a_mutarem.size != 0:
            for individuo in individuos_a_mutarem:
                gene_inicial = randint(0, self.numero_genes - 1)
                gene_final = randint(0, self.numero_genes - 1)
                while gene_inicial == gene_final:
                    gene_final = randint(0, self.numero_genes - 1)
                    if gene_inicial > gene_final:
                        gene_inicial, gene_final = gene_final, gene_inicial
                    self.populacao[individuo, gene_inicial:gene_final] = self.populacao[individuo, gene_inicial:gene_final][::-1]


