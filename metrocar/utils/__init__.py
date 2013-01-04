from pipetools import foreach, sort


class Bunch:
    """
    A handy dictionary alternative that allows for direct attribute access.

    >>> duck = Bunch(name='dolan', quack=lambda: 'Qauck!')
    >>> duck.name
    'dolan'
    >>> duck.quack()
    'Qauck!'
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return (self.iteritems() >
            foreach('  {0}={1!r}') | sort | '\n'.join | '<Bunch\n{0}>')

    def iteritems(self):
        "Supports iteration over the inner dict"
        return self.__dict__.iteritems()
