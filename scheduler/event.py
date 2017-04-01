'''The event object is essentially a wrapper around a function. It provides
some useful functionality such as recording when the function was last run,
and how many times it should be run'''
import time


# This may be useful for creating a test framework in the future
TIME_FUNCTION = time.time

class Event(object):
    '''An event that can be scheduled or called directly.
    The number of runs, the time between runs and arguments to the
    function can all be specified. By default the function will
    be run forever every frame'''
    def __init__(self, funct, args=None, time_between=0, num_runs=-1):
        self.funct = funct
        if args is None:
            self.args = list()
        else:
            self.args = args
        self.time_between = time_between
        self.num_runs = num_runs
        self.last_run = TIME_FUNCTION()
        self.remaining_runs = num_runs

    def __call__(self):
        '''Runs the function and resets the timer. Decrements run
        counter. Returns True if the event should be kept'''
        self.funct(*self.args)

        if self.time_between == 0:
            self.last_run = TIME_FUNCTION()
        else:
            self.last_run = self.last_run + self.time_between

        if self.remaining_runs > 1:
            self.remaining_runs -= 1
        elif self.remaining_runs == 1:
            return False
        return True

    @property
    def time_since_last_run(self):
        '''Returns the time since the event was last run.

        If the schedular is not keeping up with this event, this
        may not be accurate, it will be when it was supposed to
        run'''
        return self.last_run - TIME_FUNCTION()

    @property
    def time_until_next_run(self):
        '''Returns the (ideal) time until the next execution.

        If the schedular is not keeping up with this event, it may be
        negative'''
        return (self.last_run + self.time_between) - TIME_FUNCTION()

    def __str__(self):
        return "Event({}.{})".format(self.funct.__module__,
                                     self.funct.__name__)
