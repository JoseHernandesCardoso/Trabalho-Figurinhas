from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Stikers():
    '''
    Um grupo de figurinhas do mesmo tipo de um determinado álbum
    que contém N figurinhas distintas.

    *code*: é o código que determina o tipo das figurinhas.
            Varia de 0 a N.
    *over*: é a quantidade de figurinhas repetidas além da primeira.
            É sempre maior igual a 0.
    '''
    code: int
    over: int

class Collection:
    '''
    Uma coleção de figurinhas de um determinado álbum.
    Indica quais e quantas figurinhas o colecionador possui,
    além do máximo de figurinhas distintas que o álbum tem.

    Exemplos:

    '''
    # campos: varia com a implementação
    def __init__(self) -> None:
        raise NotImplementedError
    
    def insert(self, stiker: Stikers) -> None:
        '''
        Adiciona a figurinha *stiker* ao álbum.
        Se ela já estiver no álbum, aumenta a quantia repetida em 1.
        Se ela não estiver na coleção, a figurinha é adicionada.
        '''
        raise NotImplementedError

    def remove(self, stiker: Stikers) -> None:
        '''
        Reduz em 1 a quantidade das figurinhas repetidas do tipo *stiker*.
        Se a quantidade de repetidas for 0, a figurinha é removida da coleção.
        Se a figurinha não estiver na coleção, nada acontece.
        '''
        raise NotImplementedError
    
    def have(self, stiker: Stikers) -> bool:
        '''
        Retorna True se alguma figurinha do tipo *stiker* está na coleção.
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
    