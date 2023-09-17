from numpy import exp, array, mgrid
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.animation import FuncAnimation
from pygenec.populacao import Populacao
from pygenec.selecao import Roleta, Torneio
from pygenec.cruzamento import KPontos, UmPonto, Embaralhamento
from pygenec.mutacao import Flip, DuplaTroca, SequenciaReversa
from pygenec.evolucao import Evolucao



def f(x, y):
    tmp = 3 * exp(-(y + 1) ** 2 - x ** 2) * (x - 1) ** 2 \
          - (exp(-(x + 1) ** 2 - y ** 2) / 3) \
          + exp(-x ** 2 - y ** 2) * (10 * x ** 3 - 2 * x + 10 * y ** 5)
    return tmp


def converter_para_bin(x):
    cnt = array([2 ** i for i in range(x.shape[1])])
    return array([(cnt * x[i, :]).sum() for i in range(x.shape[0])
                  ])


def xy(populacao):
    colunas = populacao.shape[1]
    meio = colunas // 2
    const = 2.0 ** meio - 1.0
    nmin = -3
    nmax = 3
    const = (nmax - nmin) / const
    x = nmin + const * converter_para_bin(populacao[:, :meio])
    y = nmin + const * converter_para_bin(populacao[:, meio:])

    return x, y


def avaliacao(populacao):
    x, y = xy(populacao)
    tmp = f(x, y)
    return tmp


cromossos_totais = 32
tamanho_populacao = 100

populacao = Populacao(avaliacao, cromossos_totais, tamanho_populacao)

populacao.gerar_populacao()
print(populacao.populacao)

# selecao = Roleta(populacao)
selecao = Torneio(populacao)

# cruzamento = UmPonto(tamanho_populacao)
# cruzamento = KPontos(tamanho_populacao)
cruzamento = Embaralhamento(tamanho_populacao)

# mutacao = Flip(probabilidade_mutacao=0.9)
# mutacao = DuplaTroca(probabilidade_mutacao=0.9)
mutacao = SequenciaReversa(probabilidade_mutacao=0.9)

evolucao = Evolucao(populacao, selecao, cruzamento, mutacao)

evolucao.numero_de_individuos_na_selecao = 10
evolucao.probabilidade_cruzamento = 0.5
evolucao.epidemia = 3


def update(frame):
    evolucao.evoluir()
    x, y = xy(populacao.populacao)
    z = f(x, y)
    graph._offsets3d = (x, y, z)


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    X, Y = mgrid[-3:3:30j, -3:3:30j]
    Z = f(X, Y)
    ax.plot_wireframe(X, Y, Z)

    x, y = xy(populacao.populacao)
    z = f(x, y)
    graph = ax.scatter(x, y, z, s=50, c='red', marker='D')

    ani = FuncAnimation(fig, update, frames=range(10000), repeat=False)
    plt.show()
