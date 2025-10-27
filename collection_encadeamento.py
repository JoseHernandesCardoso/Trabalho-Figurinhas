from __future__ import annotations
from dataclasses import dataclass

@dataclass
class No:
    '''Um nó em um encadeamento'''
    item: Sticker
    prox: No | None


class Fila:
    '''
    Uma coleção de Stickers que segue a política FIFO: o primeiro a ser inserido
    é o primeiro a ser removido.
    '''

    # Invariantes:
    #   - Se inicio é None, então fim é None
    #   - Se inicio é um No, então fim é o nó no fim do encadeamento que começa
    #     em inicio
    inicio: No | None
    fim: No | None

    def __init__(self) -> None:
        '''Cria uma nova fila vazia'''
        self.inicio = None
        self.fim = None

    def enfileira(self, item: Sticker):
        '''
        Adiciona *item* no final da fila.
        '''
        if self.fim is None:
            assert self.inicio is None
            self.inicio = No(item, None)
            self.fim = self.inicio
        else:
            self.fim.prox = No(item, None)
            self.fim = self.fim.prox

    def desenfileira(self) -> Sticker:
        '''
        Remove e devolve o primeiro elemento da fila.

        Requer que a fila não esteja vazia.
        '''
        if self.inicio is None:
            return None #type: ignore
        item = self.inicio.item
        self.inicio = self.inicio.prox
        if self.inicio is None:
            self.fim = None
        return item

    def vazia(self) -> bool:
        '''
        Devolve True se a fila está vazia, False caso contrário.
        '''
        return self.inicio is None
    
class Sticker:

    next : Sticker
    id :  int
    units : int
    previous : Sticker

    def __init__(self, previous, id, units, next) -> None:
        self.id = id
        self.next = next
        self.previous = previous
        self.units = units

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
    # campos: varia com a implementação

    max_sticker : int
    sentinel : Sticker

    def __init__(self, unique: int) -> None:
        '''
        Cria uma coleção em relação a um álbum com *unique* figurinhas únicas,
        ou seja, os códigos das figurinhas variam de 0 a *unique*.
        '''
        self.max_sticker = unique
        self.sentinel = Sticker(None, None, None, None)
        self.sentinel.next = self.sentinel
        self.sentinel.previous = self.sentinel
        self.start = None
        self.end = None
    
    def insert(self, code: int) -> None:
        '''
        Aumenta em 1 a quantidade da figurinha de código *code*.

        Se ela não estiver na coleção, a figurinha é adicionada.
        Se a figurinha não estiver no intervalo das possíveis figurinhas
        do álbum, nada acontece.
        '''
        on_collection = False
        if code > self.max_sticker or code < 0:
            return None
        if self.sentinel.next is self.sentinel:
            new = Sticker(self.sentinel, code, 1, self.sentinel)
            self.sentinel.next = new
            self.sentinel.previous = new
        else:
            i = self.sentinel
            while i.next is not self.sentinel and not on_collection:
                i = i.next
                if i.id == code:
                    i.units += 1
                    on_collection = True
            if not on_collection:
                i = self.sentinel
                new = Sticker(i, code, 1, i.next)
                if i.next.id > code:
                    i.next.previous = new
                    i.next = new
                    on_collection = True
                while i.next is not self.sentinel and not on_collection:
                    i = i.next
                    new = Sticker(i, code, 1, i.next)
                    if i.id < code and (i.next.id is None or i.next.id > code):
                        i.next.previous = new
                        i.next = new
                        on_collection = True
                if not on_collection:
                    self.sentinel.previous.next = new
                    self.sentinel.previous = new
    def remove(self, code: int) -> None:
        '''
        Reduz em 1 a quantidade da figurinha de código *code*.

        Se a quantidade da figurinha reduzir para 0, ela é removida
        da coleção. Se a figurinha não estiver na coleção, nada acontece.
        '''
        removed = False
        i = self.sentinel
        while i.next is not self.sentinel and not removed:
            i = i.next
            if i.id == code and i.units == 1:
                i.previous.next = i.next
                i.next.previous = i.previous
                removed = True
            elif i.id == code and i.units >1:
                i.units -= 1
                removed = True

    def str_stickers(self) -> str:
        '''
        Gera uma representação em formato de sting das figurinhas da coleção.
        '''
        
        string = '['
        i = self.sentinel.next
        if i is not self.sentinel:
            string = string + str(i.id)
            while i.next is not self.sentinel:
                i = i.next
                string = string + ', ' + str(i.id)
        string = string + ']'
        return string
    
    def str_repeat(self) -> str:
        '''
        Gera uma representação em formato de string das figurinhas repetidas
        da coleção, junto com a quantidade (além da primeira) de cada figurinha
        repetida.
        '''
        string = '['
        i = self.sentinel
        first = True
        while i.next is not self.sentinel:
            i = i.next
            if i.units > 1 and not first:
                string = string + ', ' + str(i.id) + ' (' + str(i.units - 1) + ')'
            elif i.units > 1 and first:
                string = string + str(i.id) + ' (' + str(i.units - 1) + ')'
                first =False
        string = string + ']'
        return string
    
    def exchange(self, other: Collection):
        '''
        Realiza o máximo de trocas válidas possíveis entre a coleção e *other*.

        Uma troca válida acontece quando uma coleção tem uma carta repetida
        que a outra não tem ao mesmo tempo que essa outra possui uma carta
        repetida que a primeira também não tenha.

        As figurinhas de menor código tem prioridade na troca.

        Requer que *other* seja uma coleção com o mesmo número de cartas únicas
        '''
        self_repeats = Fila()
        other_repeats = Fila()

        i = self.sentinel.next
        j = other.sentinel.next
        other_number = 0
        self_number = 0

        while i is not self.sentinel or j is not other.sentinel:
            if i.id == j.id:
                i = i.next
                j = j.next
            elif i.id is None and j.id is not None:
                
                if j.units > 1:
                    other_repeats.enfileira(j)
                    other_number += 1 
                j = j.next
            elif j.id is None and i.id is not None:
                if i.units > 1:
                    self_repeats.enfileira(i)
                    self_number += 1
                i = i.next
            elif i.id < j.id:
                if i.units > 1:
                    self_repeats.enfileira(i)
                    self_number += 1
                if i is not self.sentinel:
                    i = i.next
                else:
                    j = j.next
            elif i.id > j.id:
                if j.units > 1:
                    other_repeats.enfileira(j)
                    other_number += 1 
                if j is not other.sentinel:
                    j = j.next
                else:
                    i = i.next

        if self_number > other_number:
            trades = other_number
        else:
            trades = self_number
        self.insert_queue(other_repeats,trades)
        other.insert_queue(self_repeats, trades)
        
    def insert_queue(self, fila : Fila, n : int) -> None:
        '''
        Insere na coleção adesivos não repetidos com base na Fila de adesivos,
        *n* vezes
        '''
        if n == 0:
            return None
        i = self.sentinel
        item = fila.desenfileira()
        if i.next.id > item.id:
            new = Sticker(i, item.id, 1, i.next)
            i.next.previous = new
            i.next = new
            item.units -= 1
            n -= 1
            item = fila.desenfileira()
        while i.next is not self.sentinel and n > 0:
            i = i.next
            new = Sticker(i, item.id, 1, i.next)
            if i.id < item.id and (i.next is self.sentinel or i.next.id > item.id):
                i.next.previous = new
                i.next = new
                item.units -= 1
                n -= 1
                item = fila.desenfileira()
            
            

            


    
    
