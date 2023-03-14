# RECEBE DADOS DO ARQUIVO "input.txt"
dados = open('input.txt', 'r').readline().split(',')

# DESCOBRE PREF E SUF E FAZ CONTAGEM DE OCORRÊNCIAS
k = len(dados[0])
def descobrePrefSuf(dados):
    # dicionário de prefixos e sufixos
    dic = {}
    # percorre cada elemento dentro de dados
    for dado in dados:
        if dado == '':
            continue
        # descobre sufixo e prefixo de cada elemento
        suf = dado[1:]
        pref = dado[:-1]
        if pref not in dic:
            dic[pref] = [[suf], [1, 0]]
        else:
            dic[pref][0].append(suf)
            dic[pref][1][0]+=1
            
        if suf not in dic:
            dic[suf] = [[], [0, 1]]
        else:
            dic[suf][1][1]+=1
    return dic

dic = descobrePrefSuf(dados)

# DESCOBRE NO INICIAL E FINAL
def descobreNoInicialFinal(dic):    
    inicial = ''
    final = ''
    menor = 0
    maior = 0

    # percorre cada item do dicionário e verifica o menor e maior valor resultante da subtração da contagem de prefixos e sufixos
    for d in dic.items():
        contPref, contSuf = d[1][1][0],  d[1][1][1]
        valor = contPref - contSuf
        # o maior valor deve ser o inicial
        if(valor > maior):
            maior = valor
            inicial = d[0]
        # o menor valor deve ser o final
        if(valor < menor):
            menor = valor
            final = d[0]
    return inicial, final

inicial, final = descobreNoInicialFinal(dic)

# DESCOBRE CAMINHO EULERIANO
def caminhoEuleriano(dic, inicial, final):
    atual = inicial
    caminho = []
    # executa enquanto o dicionário tiver elementos
    while(len(dic)!=0):
        # se o elemento atual ainda está no dicionário, é adicionado
        if(atual in dic):
            caminho.append(atual)
        # se o elemento não estiver no dicionário mas o dicionário ainda não estiver vazio
        if(atual not in dic and len(dic)!=0):
            # continua o caminho procurando onde adicionar os que ainda faltam
            caminho = continuaCaminho(caminho, dic)
            break
        # se o elemento estiver no dicionário e a posição atual dele ainda tiver sufixos
        elif(len(dic[atual][0])!=0):
            # subtrai quant. prefixos
            dic[atual][1][0]-=1
            # "prox" será o primeiro valor da lista de sufixos
            prox = dic[atual][0].pop(0)
            # se o prox estiver no dicionário e for diferente de None, subtrai qaunt. sufixos
            if(prox in dic and prox != None):
                dic[prox][1][1]-=1
            # se não houver mais sufixos na posição atual e quant. pref e suf estiverem zeradas
            if(len(dic[atual][0])==0 and dic[atual][1][0] == 0 and dic[atual][1][1]==0):
                # deleta vertice atual
                del dic[atual] 
            # aponta para prox vertice
            atual = prox     
        # se não houver mais sufixos na posição atual e quant. pref e suf estiverem zeradas
        elif(len(dic[atual][0])==0 and dic[atual][1][0] == 0 and dic[atual][1][1]==0):
            del dic[atual]

    return caminho

def continuaCaminho(caminho, dic):
    while(len(dic)!=0):
        novoCaminho = []
        atual = None
        # procura no dicionario um valor que corresponda a algum no caminho
        for i in caminho:
            if(i in dic):
                atual = i
                break
        if(atual==None):
            break
        # separa a lista em inicio e fim a partir do valor encontrado
        listaComeco = caminho[:caminho.index(atual)]
        listaFim = caminho[caminho.index(atual)+1:]

        # um novo caminho será formado a partir da primeira parte da lista
        novoCaminho = listaComeco.copy()

        # cria um novo caminho a partir do valor encontrado (atual)
        while(len(dic)!=0):
            if(atual in dic):
                novoCaminho.append(atual)
            # se o valor atual não estiver no dicionário mas o dicionário ainda contiver elementos, então busca dá break e busca novo elemento
            if(atual not in dic and len(dic)!=0): 
                caminho = novoCaminho + listaFim
                break
            # caso contrário, se o valor ainda tiver sufixos
            elif(len(dic[atual][0])!=0):
                # decrementa a quantidade de prefixos (setas saindo) do valor atual
                dic[atual][1][0]-=1
                prox = dic[atual][0].pop(0)
                if(prox in dic and prox != None):
                    # decrementa a quantidade de sufixos (setas entrando) do prox (que está na lista de atual)
                    dic[prox][1][1]-=1
                # se o tamanho do dicionário for 0 (sem sufixos) e já tiver quantidade de suf e pref zeradas, então deleta o vertice
                if(len(dic[atual][0])==0 and dic[atual][1][0] == 0 and dic[atual][1][1] == 0):
                    del dic[atual] 
                    # se esse vertice atual e prestes a ser deletado for igual ao próximo (aponta para si mesmo), então adiciona na lista de novo caminho
                    # e concatena listas de caminhos
                    if(atual == prox):
                        novoCaminho.append(prox)
                        caminho = novoCaminho + listaFim
                atual = prox    
            # se o tamanho do dicionário for 0 (sem sufixos) e já tiver quantidade de suf e pref zeradas, então deleta o vertice
            elif(len(dic[atual][0])==0 and dic[atual][1][0] == 0 and dic[atual][1][1]==0):
                del dic[atual]
    print(dic)
    return caminho

# transforma caminho em String com a sequencia
caminho = caminhoEuleriano(dic, inicial, final)
def montaFita(caminho):
    sequencia = caminho[0]
    for i in range(1, len(caminho)):
        sequencia += caminho[i][-1]
    return sequencia
sequencia = montaFita(caminho)

# escrevendo saída no arquivo
def escreveArquivo(sequencia):
    f = open("output.txt", "w")
    f.write(sequencia)
    f.close()

escreveArquivo(sequencia)