from __future__ import annotations

class Collection:
    '''
    Uma coleção de figurinhas de um determinado álbum.
    Indica quais e quantas figurinhas o colecionador possui, além
    do máximo de figurinhas distintas que o álbum tem.

    Exemplos:

    '''
    # campos: varia com a implementação
    def __init__(self) -> None:
        raise NotImplementedError
    
    def insert(self, code: int) -> None:
        '''
        Aumenta em 1 a quantidade da figurinha de código *code*.

        Se ela não estiver na coleção, a figurinha é adicionada.
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
    
    def str_stikers(self) -> str:
        '''
        Gera uma representação em formato de sting das figurinhas da coleção
        '''
        raise NotImplementedError
    
    def str_repeat(self) -> str:
        '''
        Gera uma representação em formato de string das figurinhas repetidas
        da coleção, junto com a quantidade excedente de cada carta.
        '''
        raise NotImplementedError
    
    def exchange(self, other: Collection):
        '''
        Realiza o máximo de trocas válidas possíveis entre a coleção e *other*.

        Uma troca válida acontece quando uma coleção tem uma carta repetida
        que a outra não tem ao mesmo tempo que essa outra possui uma carta
        repetida que a primeira também não tenha.
        '''
        raise NotImplementedError
    