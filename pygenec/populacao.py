from numpy import argsort, unique
from numpy.random import randint

class Populacao:

    def __init__(self, avaliacao, genes_totais, tamanho_populacao):
        self.avaliacao = avaliacao
        self.genes_totais = genes_totais
        self.tamanho_populacao = tamanho_populacao

    def gerar_populacao(self):
        self.populacao = randint(0, 2,
                                 size=(self.tamanho_populacao,
                                       self.genes_totais),
                                 dtype='b')

    def avaliar(self):
        valores_unicos, indices = unique(self.populacao,
                                         return_inverse=True,
                                         axis=0)

        valores = self.avaliacao(valores_unicos)
        valores = valores[indices]
        ind = argsort(valores)
        self.populacao[:] = self.populacao[ind]
        return valores[ind]

