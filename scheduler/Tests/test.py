'''Unit Tests for the scheduler'''
import unittest
import sys
import time
import os


def setup_path():
    '''Because this is run from a subdirectory of the project, we need to
    add the actual path'''
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    upstream_path = os.path.join(dir_path, '../../')
    sys.path.append(upstream_path)


def increment_list(inp):
    '''Does something that can easily be checked and counted from outside'''
    inp[0] += 1


class TestScheduler(unittest.TestCase):
    '''Tests a scheduler'''
    def test_basic(self):
        '''Test that events can be scheduled and run'''
        import scheduler
        sched = scheduler.Scheduler()
        input_list = [0]  # The number in here will be incremented
        eve = scheduler.Event(increment_list, args=[input_list])
        sched.register(eve)
        sched.update()
        self.assertEqual(input_list, [1])

    def test_run_multiple(self):
        '''Tests that the event will run multiple times'''
        import scheduler
        count = 3
        sched = scheduler.Scheduler()
        input_list = [0]  # The number in here will be incremented
        eve = scheduler.Event(increment_list, args=[input_list])
        sched.register(eve)
        for _ in range(count):
            sched.update()
        self.assertEqual(input_list, [count])

    def test_run_only_once(self):
        '''Tests the run counter'''
        import scheduler
        sched = scheduler.Scheduler()
        input_list = [0]  # The number in here will be incremented
        eve = scheduler.Event(increment_list, args=[input_list], num_runs=1)
        sched.register(eve)
        for _ in range(5):  # Run scheduler lots of times
            sched.update()
        self.assertEqual(input_list, [1])

    def test_run_delay(self):
        '''Tests running after a certain delay'''
        import scheduler
        delay_time = 0.01

        sched = scheduler.Scheduler()
        input_list = [0]  # The number in here will be incremented
        eve = scheduler.Event(
            increment_list,
            args=[input_list],
            time_between=delay_time * 2
        )
        sched.register(eve)

        # First two times should not do anything:
        sched.update()
        self.assertEqual(input_list, [0])
        time.sleep(delay_time)
        sched.update()
        self.assertEqual(input_list, [0])
        time.sleep(delay_time)

        # This update should increment it
        sched.update()
        self.assertEqual(input_list, [1])
        time.sleep(delay_time)

        # This update should not increment it
        sched.update()
        self.assertEqual(input_list, [1])


if __name__ == '__main__':
    setup_path()

    unittest.main()
