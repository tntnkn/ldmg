from .TableLoader    import load_tables, process_states_records, process_transitions_records
from .Graph          import Graph


def load_graph():
    states_records, transitions_records = load_tables()
    states = process_states_records(states_records)
    transitions = process_transitions_records(transitions_records)

    return Graph(states, transitions)

