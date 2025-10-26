from __future__ import annotations
from array_ed import array
from dataclasses import dataclass

INITIAL_ARRAY_SIZE = 2

@dataclass
class StickersGroup():
    '''
    Um conjunto de figurinhas do mesmo tipo de determinado álbum, ou seja,
    que possuem o mesmo código de identificação e pertençam ao mesmo álbum.

    *code*: É o código de identificação das figurinhas. Varia de 0 a N,
            onde N é a quantidade de figurinhas únicas que o álbum possui.

    *quant*: É a quantidade de figurinhas do mesmo tipo. Se for 0,
             significa que não há figurinhas do tipo.
    '''
    code: int
    quant: int

class Collection:
    '''
    Uma coleção de figurinhas de um determinado álbum.
    Indica quais e quantas figurinhas o colecionador possui, além
    do máximo de figurinhas distintas que o álbum tem.

    Exemplos:
    >>> a = Collection(60)
    >>> a.str_stickers()
    '[]'
    >>> a.str_repeat()
    '[]'
    >>> # Testando inserir e remover figurinhas dentro do intervalo
    >>> a.insert(3)
    >>> a.str_stickers()
    '[3]'
    >>> a.insert(41)
    >>> a.insert(29)
    >>> a.insert(3)
    >>> a.str_repeat()
    '[3 (1)]'
    >>> a.insert(3)
    >>> a.insert(54)
    >>> a.insert(29)
    >>> a.str_stickers()
    '[3, 29, 41, 54]'
    >>> a.str_repeat()
    '[3 (2), 29 (1)]'
    >>> a.remove(29)
    >>> a.remove(3)
    >>> a.remove(41)
    >>> a.remove(60) # não está na coleção, então nada deve ocorrer
    >>> a.str_stickers()
    '[3, 29, 54]'
    >>> a.str_repeat()
    '[3 (1)]'
    >>> # Testando inserir e remover fora do intervalo
    >>> # Essas operações não podem alterar a coleção
    >>> a.insert(-1)
    >>> a.insert(61)
    >>> a.remove(-4)
    >>> a.remove(72)
    >>> a.str_stickers()
    '[3, 29, 54]'
    >>> a.str_repeat()
    '[3 (1)]'
    >>> # Testndo troca de figurinhas
    >>> a.insert(3)
    >>> a.insert(12)
    >>> a.insert(54)
    >>> a.insert(54)
    >>> a.insert(33)
    >>> a.insert(41)
    >>> a.insert(60)
    >>> a.insert(60)
    >>> a.insert(60)
    >>> a.str_stickers()
    '[3, 12, 29, 33, 41, 54, 60]'
    >>> a.str_repeat()
    '[3 (2), 54 (2), 60 (2)]'
    >>> b = Collection(60)
    >>> b.str_stickers()
    '[]'
    >>> # Nenhuma das trocas devem alterar as coleções
    >>> # Pois b não possui figurinhas para trocar.
    >>> a.exchange(b)
    >>> b.exchange(a)
    >>> a.str_stickers()
    '[3, 12, 29, 33, 41, 54, 60]'
    >>> a.str_repeat()
    '[3 (2), 54 (2), 60 (2)]'
    >>> b.str_stickers()
    '[]'
    >>> b.insert(12)
    >>> b.insert(51)
    >>> b.insert(9)
    >>> b.insert(0)
    >>> b.str_stickers()
    '[0, 9, 12, 51]'
    >>> b.str_repeat()
    '[]'
    >>> # b ainda não poderá trocar
    >>> a.exchange(b)
    >>> b.exchange(a)
    >>> a.str_repeat()
    '[3 (2), 54 (2), 60 (2)]'
    >>> b.str_stickers()
    '[0, 9, 12, 51]'
    >>> b.insert(0)
    >>> b.insert(12)
    >>> b.insert(51)
    >>> b.insert(51)
    >>> b.str_stickers()
    '[0, 9, 12, 51]'
    >>> b.str_repeat()
    '[0 (1), 12 (1), 51 (2)]'
    >>> a.str_stickers()
    '[3, 12, 29, 33, 41, 54, 60]'
    >>> a.str_repeat()
    '[3 (2), 54 (2), 60 (2)]'
    >>> # Serão realizadas 2 trocas ente a e b.
    >>> # a enviará 3 e 54
    >>> # b enviará 0 e 51
    >>> # mesmo que 12 seja repetida em b, não será
    >>> # enviada, porque a já possui uma 12
    >>> a.exchange(b)
    >>> a.str_stickers()
    '[0, 3, 12, 29, 33, 41, 51, 54, 60]'
    >>> a.str_repeat()
    '[3 (1), 54 (1), 60 (2)]'
    >>> b.str_stickers()
    '[0, 3, 9, 12, 51, 54]'
    >>> b.str_repeat()
    '[12 (1), 51 (1)]'
    ''' 
    # Total de figurinhas únicas
    tot_stickers: int
    # Máximo de figurinhas únicas
    max_unique: int
    # Agrupamento das figurinhas
    stickers: array[StickersGroup]

    def __init__(self, max_unique: int) -> None:
        '''
        Cria uma coleção em relação a um álbum com *max_unique* figurinhas únicas,
        ou seja, os códigos das figurinhas variam de 0 a *max_unique*.
        '''
        self.max_unique = max_unique
        self.tot_stickers = 0
        self.stickers = array(INITIAL_ARRAY_SIZE, StickersGroup(None, 0)) #type: ignore
    
    def insert(self, code: int) -> None:
        '''
        Aumenta em 1 a quantidade da figurinha de código *code*.

        Se ela não estiver na coleção, a figurinha é adicionada.
        Se a figurinha não estiver no intervalo das possíveis figurinhas
        do álbum, nada acontece.
        '''
        pos = self.position(code)
        # Está na lista na posição *pos* -> atualiza quantidade
        if pos is not None:
            self.stickers[pos].quant += 1
        # Não está na lista, mas é válido -> insere ordenado
        elif code >= 0 and code <= self.max_unique:
            self.___ordered_insert(code)
            self.tot_stickers += 1
    
    def ___ordered_insert(self, code: int) -> None:
        '''
        Insere *code* de forma ordenada em *self.stickers*
        Função auxiliar de insert().
        '''
        if self.is_full():
            self.expand()
        
        i = self.tot_stickers
        inserted = False
        while i >= 0 and not inserted:
            if i == 0 or self.stickers[i-1].code < code:
                self.stickers[i] = StickersGroup(code, 1)
                inserted = True
            else:
                self.stickers[i] = self.stickers[i-1]
            i -= 1

    def remove(self, code: int) -> None:
        '''
        Reduz em 1 a quantidade da figurinha de código *code*.

        Se a quantidade da figurinha redizir para 0, ela é removida
        da coleção. Se a figurinha não estiver na coleção, nada acontece.
        '''
        i = self.position(code)
        if i is not None:
            self.stickers[i].quant -= 1
            # Se não houver mais figurinhas do tipo, removemos do array
            if self.stickers[i].quant == 0:
                while i < self.tot_stickers:
                    self.stickers[i] = self.stickers[i+1]
                    i += 1
                self.tot_stickers -= 1
    
    def str_stickers(self) -> str:
        '''
        Gera uma representação em formato de sting das figurinhas da coleção.
        '''
        string = '['
        # adiciona o primeiro elemento (se houver)
        if not self.is_empty():
            string += str(self.stickers[0].code)
        # adiciona demais elementos
        i = 1
        while i < self.tot_stickers:
            string += f', {str(self.stickers[i].code)}'
            i += 1
        return string + ']'
    
    def str_repeat(self) -> str:
        '''
        Gera uma representação em formato de string das figurinhas repetidas
        da coleção, junto com a quantidade (além da primeira) de cada figurinha
        repetida.
        '''
        string = '['
        i = 0
        # adiciona o primeiro elemento válido
        first_in = False
        while not first_in and i < self.tot_stickers:
            if self.stickers[i].quant > 1:
                string += f'{str(self.stickers[i].code)} ({str(self.stickers[i].quant - 1)})'
                first_in = True
            i += 1
        # adiciona demais elementos válidos
        while i < self.tot_stickers:
            if self.stickers[i].quant > 1:
                string += f', {str(self.stickers[i].code)} ({str(self.stickers[i].quant - 1)})'
            i += 1
        return string + ']'
    
    def exchange(self, other: Collection) -> None:
        '''
        Realiza o máximo de trocas válidas possíveis entre a coleção e *other*.

        Uma troca válida acontece quando uma coleção tem uma carta repetida
        que a outra não tem ao mesmo tempo que essa outra possui uma carta
        repetida que a primeira também não tenha.

        As figurinhas de menor código tem prioridade na troca.

        Requer que *other* seja uma coleção com o mesmo número de cartas únicas
        '''
        if self.max_unique != other.max_unique:
            raise ValueError('Quantidade de cartas únicas diferentes')
        
        # Salvar indices das figurinhas que vão ser trocadas
        self_to_other: list[int] = []
        other_to_self: list[int] = []
        i_self = i_other = 0
        while (self.has_next(i_self) or other.has_next(i_other)) \
            and not self.is_empty() and not other.is_empty():

            stk_self = self.stickers[i_self]
            stk_other = other.stickers[i_other]
            if stk_self.code == stk_other.code:
                if self.has_next(i_self):
                    i_self += 1
                if other.has_next(i_other):
                    i_other += 1
            elif stk_self.code > stk_other.code and other.has_next(i_other):
                if stk_other.quant > 1:
                    other_to_self.append(i_other)
                i_other += 1
            elif stk_self.code < stk_other.code and self.has_next(i_self):
                if stk_self.quant > 1:
                    self_to_other.append(i_self)
                i_self += 1
            elif stk_self.code > stk_other.code and not other.has_next(i_other):
                if not last_item_is(other_to_self, i_other) and stk_other.quant > 1:
                    other_to_self.append(i_other)
                if stk_self.quant > 1:
                    self_to_other.append(i_self)
                i_self += 1
            elif stk_self.code < stk_other.code and not self.has_next(i_self):
                if not last_item_is(self_to_other, i_self) and stk_self.quant > 1:
                    self_to_other.append(i_self)
                if stk_other.quant > 1:
                    other_to_self.append(i_other)
                i_other += 1
            
            if not self.has_next(i_self) and not other.has_next(i_other) and \
                stk_self.code != stk_other.code:
                    
                if not last_item_is(self_to_other, i_self) \
                    and self.stickers[i_self].quant > 1:

                    self_to_other.append(i_self)
                if not last_item_is(other_to_self, i_other) \
                    and other.stickers[i_other].quant > 1:

                    other_to_self.append(i_other)
            
        # Realizar trocas a partir do indice (inserção no fim)
        i = 0
        while i < len(self_to_other) and i < len(other_to_self):
            self.append(other.stickers[other_to_self[i]].code)
            other.remove_index(other_to_self[i])
            other.append(self.stickers[self_to_other[i]].code)
            self.remove_index(self_to_other[i])
            i += 1
        # Ordenar tudo
        self.sort(0, self.tot_stickers - 1)
        other.sort(0, other.tot_stickers - 1)

    def position(self, code: int) -> int | None:
        '''
        Retorna a posição i da figurinha de código *code* dentro do agrupamento.
        Se ela não estiver no agrupamento, retorna None
        '''
        position = None
        # Procura se está na lista 
        found = False
        i = 0
        while not found and i < self.tot_stickers:
            # Se encontrar, atualiza position e sai do loop
            if self.stickers[i].code == code:
                position = i
                found = True
            i += 1
        return position
    
    def is_full(self) -> bool:
        '''
        Retorna True se o array *self.stickers* está cheio.
        Retorna False, caso contrário.
        '''
        # Algumas métodos (como o remove) requerem que o array sempre tenha,
        # pelo menos, um espaço livre. Portanto, o tamanho da coleção deve
        # ser um a menos do array. 
        return self.tot_stickers == len(self.stickers) - 1
    
    def is_empty(self) -> bool:
        '''
        Retorna True se o array *self.stickers* está vazio.
        Retorna False, caso contrário
        '''
        return self.tot_stickers == 0
    
    def append(self, code: int) -> None:
        '''
        Insere um novo grupo de figurinhas de código *code* no final da coleção
        '''
        if self.is_full():
            self.expand()

        self.stickers[self.tot_stickers] = StickersGroup(code, 1)
        self.tot_stickers += 1
    
    def remove_index(self, index: int) -> None:
        '''
        Reduz em 1 a quantidade da figurinha que está na posição *index* da coleção.
        '''
        self.stickers[index].quant -= 1   

    def has_next(self, index: int) -> int:
        '''
        Retorna True se o elemento na posição *index + 1* na coleção for válido,
        ou seja, o valor do código da figurinha não é None.
        '''
        return self.stickers[index + 1].code is not None
    
    def sort(self, start: int, end: int) -> None:
        '''
        Ordena os elementos das posições *start* até *end* da coleção em ordem
        crescente dos códigos das figurinhas.
        '''
        # Ordenação por Quick Sort
        if start < end:
            pivot = self.partition(start, end)
            self.sort(start, pivot - 1)
            self.sort(pivot + 1, end)
    
    def partition(self, start: int, end: int) -> int:
        '''
        Função auxiliar de sort().
        Retorna a posição do pivo na ordenação por quick sort.
        '''
        pivot = self.stickers[end]
        # Valores menores que o pivo vão para direita 
        # e maiores ou iguais vão para esquerda
        i = start - 1
        j = start
        while j <= end - 1:
            if self.stickers[j].code < pivot.code:
                i += 1
                temp = self.stickers[i]
                self.stickers[i] = self.stickers[j]
                self.stickers[j] = temp
            j += 1
        # Posiciona pivo na posição correta e retorna a posição dele
        i += 1
        temp = self.stickers[i]
        self.stickers[i] = self.stickers[end]
        self.stickers[end] = temp
        return i
    
    def expand(self) -> None:
        '''
        Aumenta em 2x a capacidade máxima da coleção
        '''
        old_size = len(self.stickers)
        new = array(old_size * 2, StickersGroup(None, 0)) #type: ignore
        for i in range(old_size):
            new[i] = self.stickers[i]
        self.stickers = new

def last_item_is(lst: list[int], item: int) -> bool:
    '''
    Verifica se o último item de *lst* é *item*
    '''
    return not len(lst) == 0 and lst[-1] == item
