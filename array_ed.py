# Este código foi disponibilizado pelo proofessor da matéria para
# termos um tipo array para usar na implementação do trabalho

from typing import TypeVar, Iterator, Generic, overload, Tuple

T = TypeVar('T')


class array(Generic[T]):
    '''
    Um arranjo de tamanho fixo implementado com uma lista.

    Exemplos
    >>> a = array(5, 0)
    >>> a
    array([0, 0, 0, 0, 0])
    >>> len(a)
    5
    >>> a[0] = 10
    >>> a[3] = 20
    >>> a
    array([10, 0, 0, 20, 0])
    >>> a[0]
    10
    >>> a[5]
    Traceback (most recent call last):
    ...
    IndexError: list index out of range

    Exemplo com string
    >>> a = array(3, 'oi')
    >>> a
    array(['oi', 'oi', 'oi'])
    >>> a[1] = ' de novo '
    >>> s = ''
    >>> for v in a:
    ...    s = s + v
    >>> s
    'oi de novo oi'
    '''

    valores: list[T]

    @overload
    def __init__(self, n_values: list[T]) -> None: ...

    @overload
    def __init__(self, n_values: int, val: T) -> None: ...

    def __init__(self, n_values: int | list[T], val: T | None = None) -> None:
        '''
        Cria um novo arranjo com *n* cópias de *val*.

        Note que todas as cópias de *val* referenciam o mesmo objeto, o pode
        não ser o comportamento desejado.

        Para criar cópias distintas de *val*, use copy.deepcopy após a criação
        do arranjo.

        Exemplo
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class Ponto:
        ...     x: int
        ...     y: int
        >>> p = Ponto(3, 4)
        >>> pontos = array(2, p)
        >>> pontos
        array([Ponto(x=3, y=4), Ponto(x=3, y=4)])
        >>> # pontos[0] e pontos[1] referenciam o mesmo objeto
        >>> pontos[0].x = 10
        >>> pontos
        array([Ponto(x=10, y=4), Ponto(x=10, y=4)])

        >>> # Para criar cópias distintas de p
        >>> # podemos usar copy.deepcopy após criar
        >>> from copy import deepcopy
        >>> p = Ponto(3, 4)
        >>> pontos = array(2, Ponto(0, 0))
        >>> for i in range(len(pontos)):
        ...     pontos[i] = deepcopy(p)
        >>> pontos
        array([Ponto(x=3, y=4), Ponto(x=3, y=4)])
        >>> pontos[0].x = 10
        >>> pontos
        array([Ponto(x=10, y=4), Ponto(x=3, y=4)])
        '''
        if isinstance(n_values, int):
            assert val is not None
            self.valores = [val] * n_values
        else:
            assert val is None
            self.valores = n_values[:]

    def __len__(self) -> int:
        return len(self.valores)

    def __getitem__(self, i: int) -> T:
        return self.valores[i]

    def __setitem__(self, i: int, value: T):
        self.valores[i] = value

    def __iter__(self) -> Iterator[T]:
        return iter(self.valores)

    def __repr__(self) -> str:
        return 'array(' + repr(self.valores) + ')'

    def __str__(self) -> str:
        return 'array(' + str(self.valores) + ')'


class array2d(Generic[T]):
    lins: int
    cols: int
    valores: list[T]

    @overload
    def __init__(self, lins_values: list[list[T]]): ...

    @overload
    def __init__(self, lins_values: int, cols: int, val: T): ...

    def __init__(self, lins_values: int | list[list[T]], cols: int | None = None, val: T | None = None):
        if isinstance(lins_values, int):
            assert cols is not None
            assert val is not None
            self.lins = lins_values
            self.cols = cols
            self.valores = [val] * (self.lins * self.cols)
        else:
            assert cols is None
            assert val is None
            self.lins = len(lins_values)
            self.cols = len(lins_values[0])
            self.valores = []
            for lin in lins_values:
                assert len(lin) == self.cols
                for val in lin:
                    self.valores.append(val)

    def __getitem__(self, index: Tuple[int, int]) -> T:
        lin, col = index
        assert lin < self.lins
        assert col < self.cols
        return self.valores[lin * self.cols + col]

    def __setitem__(self, index: Tuple[int, int], value: T):
        lin, col = index
        assert lin < self.lins
        assert col < self.cols
        self.valores[lin * self.cols + col] = value

    def __repr__(self) -> str:
        s = 'array2d(['
        sep = ''
        for lin in range(self.lins):
            i = lin * self.cols
            s += sep + repr(self.valores[i:(i + self.cols)])
            sep = '\n' + ' ' * 9
        return s + '])'

    def __str__(self) -> str:
        return repr(self)
