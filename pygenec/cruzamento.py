from numpy import array
from numpy.random import random, randint, shuffle


class NotCompatibleIndividualsSizeError(Exception):
    pass


class Cruzamento:

    def __init__(self, tamanho_populacao) -> None:
        self.tamanho_populacao = tamanho_populacao

    def cruzamento(self, progenitor1, progenitor2):
        raise NotImplementedError("Implementado nas classes filhas")

    def descendentes(self, subpopulacao, probabilidade_cruzamento=0.5):
        nova_populacao = []
        numero_populacao = len(subpopulacao)

        while len(nova_populacao) < self.tamanho_populacao:
            i = randint(0, numero_populacao - 1)
            j = randint(0, numero_populacao - 1)

            while i == j:
                j = randint(0, numero_populacao - 1)

            cruzar = random()
            if cruzar < probabilidade_cruzamento:
                descendente_1, descendente_2 = self.cruzamento(subpopulacao[i], subpopulacao[j])
                nova_populacao.append(descendente_1)

                if len(nova_populacao) < self.tamanho_populacao:
                    nova_populacao.append(descendente_2)

        return array(nova_populacao)


class UmPonto(Cruzamento):
    
    def __init__(self, tamanho_populacao):
        super(UmPonto, self).__init__(tamanho_populacao)

    def cruzamento(self, progenitor1, progenitor2):
        tamanho_progenitor1 = len(progenitor1)
        tamanho_progenitor2 = len(progenitor2)

        if tamanho_progenitor1 != tamanho_progenitor2:
            raise NotCompatibleIndividualsSizeError(f'Tamanho do progenitor 1 ({tamanho_progenitor1}) '
                                                    f'é diferente do progenitor 2 ({tamanho_progenitor2})')

        ponto = randint(1, tamanho_progenitor1 - 1)
        descendente1 = progenitor1.copy()
        descendente2 = progenitor2.copy()

        descendente1[ponto:] = progenitor2[ponto:]
        descendente2[ponto:] = progenitor1[ponto:]

        return descendente1, descendente2


class KPontos(Cruzamento):

    def __init__(self, tamanho_populacao):
        super(KPontos, self).__init__(tamanho_populacao)

    def cruzamento(self, progenitor1, progenitor2):
        tamanho_progenitor1 = len(progenitor1)
        tamanho_progenitor2 = len(progenitor2)

        if tamanho_progenitor1 != tamanho_progenitor2:
            raise NotCompatibleIndividualsSizeError(f'Tamanho do progenitor 1 ({tamanho_progenitor1}) '
                                                    f'é diferente do progenitor 2 ({tamanho_progenitor2})')

        descendente1 = progenitor1.copy()
        descendente2 = progenitor2.copy()

        k_pontos = randint(0, tamanho_progenitor1 - 2)
        k = []

        while len(k) < k_pontos:
            p = randint(1, tamanho_progenitor1 - 1)
            if p not in k:
                k.append(p)
        k.sort()

        troca = randint(0, 1)

        for i in range(k_pontos - 1):
            if troca == 0:
                troca = 1
            else:
                troca = 0
                descendente1[k[i]:k[i + 1]] = progenitor2[k[i]:k[i + 1]]
                descendente2[k[i]:k[i + 1]] = progenitor1[k[i]:k[i + 1]]

        return descendente1, descendente2


class Embaralhamento(Cruzamento):

    def __init__(self, tamanho_populacao):
        super(Embaralhamento, self).__init__(tamanho_populacao)

    def cruzamento(self, progenitor1, progenitor2):
        tamanho_progenitor1 = len(progenitor1)
        tamanho_progenitor2 = len(progenitor2)

        if tamanho_progenitor1 != tamanho_progenitor2:
            raise NotCompatibleIndividualsSizeError(f'Tamanho do progenitor 1 ({tamanho_progenitor1}) '
                                                    f'é diferente do progenitor 2 ({tamanho_progenitor2})')

        order = list(range(tamanho_progenitor1))
        shuffle(order)

        ponto = randint(1, tamanho_progenitor1 - 1)
        descendente1 = progenitor1.copy()
        descendente2 = progenitor2.copy()

        descendente1[:] = descendente1[order]
        descendente2[:] = descendente2[order]

        descendente1[ponto:], descendente2[ponto:] = descendente2[ponto:], descendente1[ponto:]

        tmp1 = descendente1.copy()
        tmp2 = descendente2.copy()

        for i, j in enumerate(order):
            descendente1[j] = tmp1[i]
            descendente2[j] = tmp2[i]

        return descendente1, descendente2






