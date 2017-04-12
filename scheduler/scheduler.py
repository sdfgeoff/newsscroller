'''Nearly every project needs a scheduler of some sort. This one is designedf
for the frame-based nature of the BGE'''
import cProfile
import sys

class Scheduler(object):
    '''A scheduler for running functions. By default one is initilized
    in bge.logic.scheduler, though others can easily be created.
    Note that the scheduler has to be updated manually each frame.
    '''
    def __init__(self):
        self.events = list()
        self.update = self.update_noprofile
        self._profile = False
        self.profile = False
        self._profiler = cProfile.Profile()
        self.error_handler = None

    def update_profiled(self):
        '''Runs update_noprofile inside a cProfile profiler'''
        self._profiler.runcall(self.update_noprofile)

    def print_stats(self):
        '''Displays the statistics if profiled'''
        self._profiler.print_stats(1)

    def update_noprofile(self):
        '''Runs an iteration of the scheduler, checking and running
        all events. A single function failing will not cause other
        events to not run. Errors are raised at the end of all
        tasks'''
        errors = list()
        for event in self.events:
            if event.time_until_next_run <= 0:
                try:
                    keep = event()
                except Exception as err:  # pylint: disable=W0703
                    # Catch all errors, so we finish the other events scheduled
                    exception_info = sys.exc_info()                    
                    errors.append((err, exception_info))
                    keep = False  # Remove a failing function
                if not keep:
                    self.events.remove(event)
        for err in errors:
            if self.error_handler is None:
                print("ARRGH!")
                raise err[0]
            else:
                self.error_handler(err[1])

    def register(self, event):
        '''Adds an event to the scheduler'''
        self.events.append(event)

    def remove(self, event):
        '''Removes an event from the scheduler'''
        self.events.remove(event)

    @property
    def profile(self):
        '''Sets if the events should be profiled so you can analyze the
        performance of items in this scheduler'''
        return self._profile

    @profile.setter
    def profile(self, val):
        self._profile = val
        if val:
            self.update = self.update_profiled
        else:
            self.update = self.update_noprofile
