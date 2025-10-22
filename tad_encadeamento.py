from __future__ import annotations

class Sticker:

    next : Sticker | None
    id : int
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
    start : Sticker | None
    end : Sticker | None

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
                new = Sticker(self.sentinel.previous, code, 1, self.sentinel)
                i = self.sentinel
                if i.next.id > code:
                    i.next.previous = new
                    new.next = i.next
                    i.next = new
                    new.previous = self.sentinel
                    on_collection = True
                while i.next is not self.sentinel and not on_collection:
                    i = i.next
                    if i.id < code and (i.next.id is None or i.next.id > code):
                        i.next.previous = new
                        new.next = i.next
                        i.next = new
                        new.previous = i
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


    
    def have(self, code: int) -> bool:
        '''
        Retorna True se a figurinha de código *code* está na coleção.
        Retorna False em caso contrário.
        '''
        i = self.sentinel
        found = False
        while i.next is not self.sentinel and not found:
            i = i.next
            if i.id == code:
                found = True
        return found

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
        self_repeats = []
        other_repeats = []
        i = self.sentinel
        
        while i.next is not self.sentinel:
            i = i.next
            if not other.have(i.id) and i.units > 1:
                self_repeats.append(i)
        i = other.sentinel
        while i.next is not other.sentinel:
            i = i.next
            if not self.have(i.id) and i.units > 1:
                other_repeats.append(i)
        if len(self_repeats) > len(other_repeats):
            smaller = other_repeats
            bigger = self_repeats 
        else:
            smaller = self_repeats
            bigger = other_repeats
        while len(bigger) > len(smaller):
            bigger.pop()
        for k in self_repeats:
            other.insert(k.id)
            k.units -= 1
        for j in other_repeats:
            self.insert(j.id)
            j.units -= 1
        
    def insert_list(self, lst : list) -> None:
        '''
        Insere na coleção adesivos não repetidos com base nos id's de
        *lst*
        '''
        i = self.sentinel
        n = 0
        all_added = False
        while i.next is not self.sentinel and not all_added:
            i = i.next
            new = Sticker(self.sentinel.previous, lst[n], 1, self.sentinel)
            if i.id < lst[n] and (i.next.id > lst[n] or i.next.id == None):
                i.next.previous = new
                new.next = i.next
                i.next = new
                new.previous = i
            


    
    