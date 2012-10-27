from pipetools import foreach, sort


class Bunch:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return (self.iteritems() >
            foreach('  {0}={1!r}') | sort | '\n'.join | '<Bunch\n{0}>')

    def iteritems(self):
        return self.__dict__.iteritems()
