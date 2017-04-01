'''A generic scheduler that can be used to schedule events. We are using
a custom scheduler because the default python sched library doesn't allow
continous running events or running incrementally without waiting (it wants
to be exclusive, not run from within an event loop)


Basic usage:
    s = Scheduler()
    e = Event(print, args=['text'])
    s.register(e)

    s.update()
    s.update()
    s.update()


This code does not import the BGE, so it does not have to be GPL
'''

from .event import Event
from .scheduler import Scheduler
