from __future__ import annotations

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
    >>> a.str_stikers()
    '[3]'
    >>> a.insert(41)
    >>> a.insert(29)
    >>> a.insert(3)
    >>> a.str_repeat()
    '[]'
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
    >>> a,insert(54)
    >>> a.insert(54)
    >>> a.insert(33)
    >>> a.insert(41)
    >>> a.insert(60)
    >>> a.insert(60)
    >>> a.insert(60)
    >>> a.str_stikers()
    '[3, 12, 29, 33, 41, 54, 60]'
    >>> a.str_repeat()
    '[3 (2), 54 (1), 60 (3)]'
    >>> b = Collection(60)
    >>> b.str_stickers()
    '[]'
    >>> # Nenhuma das trocas devem alterar as coleções
    >>> # Pois b não possui figurinhas para trocar.
    >>> a.exchange(b)
    >>> b.exchange(a)
    >>> a.str_stikers()
    '[3, 12, 29, 33, 41, 54, 60]'
    >>> a.str_repeat()
    '[3 (2), 54 (1), 60 (3)]'
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
    '[3 (2), 54 (1), 60 (3)]'
    >>> b.str_stickers()
    '[]'
    >>> b.insert(0)
    >>> b.insert(12)
    >>> b.insert(51)
    >>> b.insert(51)
    >>> b.str_stikers()
    '[0, 9, 12, 51]'
    >>> b.str_repeat()
    '[0 (1), 12 (1), 51 (2)]'
    >>> a.str_stikers()
    '[3, 12, 29, 33, 41, 54, 60]'
    >>> a.str_repeat()
    '[3 (2), 54 (1), 60 (3)]'
    >>> # Serão realizadas 2 trocas ente a e b.
    >>> # a enviará 3 e 54
    >>> # b enviará 0 e 51
    >>> # mesmo que 12 seja repetida em b, não será
    >>> # enviada, porque a já possui uma 12
    >>> a.exchange(b)
     >>> a.str_stikers()
    '[0, 3, 12, 29, 33, 41, 51, 54, 60]'
    >>> a.str_repeat()
    '[3 (1), 60 (3)]'
    >>> b.str_stikers()
    '[0, 3, 9, 12, 51, 54]'
    >>> b.str_repeat()
    '[12 (1), 51 (1)]'
    '''
    # campos: varia com a implementação
    def __init__(self, unique: int) -> None:
        '''
        Cria uma coleção em relação a um álbum com *unique* figurinhas únicas,
        ou seja, os códigos das figurinhas variam de 0 a *unique*.
        '''
        raise NotImplementedError
    
    def insert(self, code: int) -> None:
        '''
        Aumenta em 1 a quantidade da figurinha de código *code*.

        Se ela não estiver na coleção, a figurinha é adicionada.
        Se a figurinha não estiver no intervalo das possíveis figurinhas
        do álbum, nada acontece.
        '''
        raise NotImplementedError

    def remove(self, code: int) -> None:
        '''
        Reduz em 1 a quantidade da figurinha de código *code*.

        Se a quantidade da figurinha redizir para 0, ela é removida
        da coleção. Se a figurinha não estiver na coleção, nada acontece.
        '''
        raise NotImplementedError
    
    def have(self, code: int) -> bool:
        '''
        Retorna True se a figurinha de código *code* está na coleção.
        Retorna False em caso contrário.
        '''
        raise NotImplementedError
    
    def str_stickers(self) -> str:
        '''
        Gera uma representação em formato de sting das figurinhas da coleção.
        '''
        raise NotImplementedError
    
    def str_repeat(self) -> str:
        '''
        Gera uma representação em formato de string das figurinhas repetidas
        da coleção, junto com a quantidade (além da primeira) de cada figurinha
        repetida.
        '''
        raise NotImplementedError
    
    def exchange(self, other: Collection):
        '''
        Realiza o máximo de trocas válidas possíveis entre a coleção e *other*.

        Uma troca válida acontece quando uma coleção tem uma carta repetida
        que a outra não tem ao mesmo tempo que essa outra possui uma carta
        repetida que a primeira também não tenha.

        As figurinhas de menor código tem prioridade na troca.

        Requer que *other* seja uma coleção com o mesmo número de cartas únicas
        '''
        raise NotImplementedError
    