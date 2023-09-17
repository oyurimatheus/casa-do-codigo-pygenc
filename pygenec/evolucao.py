from random import random


class Evolucao:

    def __init__(self, populacao, selecao, cruzamento, mutacao):
        self.populacao = populacao
        self.selecao = selecao
        self.cruzamento = cruzamento
        self.mutacao = mutacao
        self._geracao = 0
        self._melhor_solucao = None
        self._numero_de_individuos_na_selecao = None
        self._probabilidade_cruzamento = None
        self._manter_melhor = True
        self._fitness = None
        self._first = True
        self._epidemia = None

    def evoluir(self):
        if self._first is True:
            self._fitness = self.populacao.avaliar()
            self._first = False

        self._melhor_solucao = self.populacao.populacao[-1].copy()
        subpopulacao = self.selecao.selecao(self._numero_de_individuos_na_selecao, fitness=self._fitness)
        populacao = self.cruzamento.descendentes(subpopulacao, probabilidade_cruzamento=self._probabilidade_cruzamento)

        self.mutacao.populacao = populacao
        self.mutacao.mutacao()

        self.populacao.populacao[:] = populacao[:]
        self._geracao += 1

        if self._epidemia is not None:
            if self._geracao % self._epidemia == 0 and random() < 0.5:
                print("Epidemia")
                self.populacao.gerar_populacao()

        if self._manter_melhor is True:
            self.populacao.populacao[0] = self._melhor_solucao

        self._fitness = self.populacao.avaliar()
        return self._fitness.min(), self._fitness.max()

    @property
    def geracao(self):
        return self._geracao

    @property
    def melhor_solucao(self):
        return self._melhor_solucao

    @property
    def manter_melhor(self):
        return self._manter_melhor

    @manter_melhor.setter
    def manter_melhor(self, manter_melhor):
        self._manter_melhor = manter_melhor

    @property
    def numero_de_individuos_na_selecao(self):
        return self._numero_de_individuos_na_selecao

    @numero_de_individuos_na_selecao.setter
    def numero_de_individuos_na_selecao(self, numero_de_individuos_na_selecao):
        self._numero_de_individuos_na_selecao = numero_de_individuos_na_selecao

    @property
    def probabilidade_cruzamento(self):
        return self._probabilidade_cruzamento

    @probabilidade_cruzamento.setter
    def probabilidade_cruzamento(self, probabilidade_cruzamento):
        self._probabilidade_cruzamento = probabilidade_cruzamento

    @property
    def epidemia(self):
        return self._epidemia

    @epidemia.setter
    def epidemia(self, epidemia):
        self._epidemia = epidemia
