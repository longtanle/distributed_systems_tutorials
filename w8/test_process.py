from process import Process
import unittest

# This function simulates the execution of the broadcast part of the consensus algorithm
# where each process sends its value to all other processes.
def execute(ps: list[Process], f: int):
    # It runs the broadcast for each process and collects the results.
    return [x.broadcast([y for y in ps if y != x], f) for x in ps]

# Unit tests for the Node or Process class which should be part of the consensus algorithm.
class NodeTest(unittest.TestCase):
    # This test checks the behavior of a single node with no faults.
    # It ensures that a node can reach consensus on its own value.
    def test_solo(self):
        p = Process(1)  # Create a process with value 1
        y = p.broadcast([], 0)  # Broadcast to no other nodes with 0 faults
        self.assertEqual(y, 1)  # Check if the result is the same as the initial value

    # This test checks the behavior with two nodes and no faults.
    # It ensures that both nodes agree on the minimum value (which is 1 in this case).
    def test_two(self):
        ps = [Process(i + 1) for i in range(2)]  # Create two processes with values 1 and 2
        ys = execute(ps, 0)  # Execute the broadcast with 0 faults
        self.assertEqual([1] * len(ps), ys)  # Check if both agreed on value 1

    # This test simulates a scenario with one faulty process.
    # It checks if the non-faulty processes can still reach a consensus.
    def test_fault(self):
        class FaultyProcess():
            request_count = 0
            def values(self):
                self.request_count += 1
                # Returns a value only on the first request, simulating a crash.
                return set([1]) if self.request_count == 1 else None
            def broadcast(self, *args):
                # Always broadcasts value 1.
                return 1
        ps = [Process(3 - i) for i in range(2)]  # Create two non-faulty processes with values 2 and 1
        ps.append(FaultyProcess())  # Add the faulty process to the list
        ys = execute(ps, 1)  # Execute the broadcast allowing for 1 fault
        self.assertEqual([1] * len(ys), ys)  # Check if consensus is reached on value 1

    # This test checks for a situation where the list of other processes includes itself,
    # which should not happen and thus should raise an exception.
    def test_invalid_list(self):
        p = Process(1)  # Create a process with value 1
        # Attempt to broadcast to itself, which should raise an Exception.
        with self.assertRaises(Exception):
            p.broadcast([p], 0)

    # This test checks for an invalid 'f' parameter where the number of allowed faults is more than the number of nodes.
    # This scenario is invalid because it would be impossible to reach a consensus and should raise an exception.
    def test_invalid_f(self):
        p = Process(1)  # Create a process with value 1
        # Attempt to broadcast with an 'f' value larger than the number of processes, which should raise an Exception.
        with self.assertRaises(Exception):
            p.broadcast([], 1)
