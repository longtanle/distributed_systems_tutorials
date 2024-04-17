class Process():
    # Initialize the process with a value 'x' which is added to a set of values.
    def __init__(self, x):
        self.v = set([x])

    # Returns the current set of values the process is aware of.
    def values(self):
        return self.v

    # Simulates broadcasting its values to a list of other processes, taking into account faults.
    def broadcast(self, ps: list['Process'], f: int):
        assert(self not in ps)  # Ensure the process is not broadcasting to itself.
        assert(len(ps) >= f)  # Ensure there are enough processes compared to the number of possible faults.
        
        # Initialize a count of how many times each process has responded.
        responses_count = [0] * len(ps)
        
        # Perform the broadcast for f+1 rounds as per the consensus algorithm.
        for _ in range(f + 1):
            for idx, p in enumerate(ps):  # Go through each process.
                v_p = p.values()  # Get the values from the process.
                if v_p:  # If there are values (the process is not faulty).
                    self.v.update(v_p)  # Update the set of known values.
                    responses_count[idx] += 1  # Increment the response count for this process.
        
        # Determine if a decision can be made based on the count of responses.
        can_decide = responses_count.count(f + 1) >= len(ps) - f
        # Decide on the minimum value if possible, otherwise return None if a decision can't be made.
        return min(self.v) if can_decide else None
