"""Example usage for GenPark Paxos Consensus Coordinator.
100% Python Standard Library.
"""

from client import PaxosConsensusCoordinator

def main():
    coordinator = PaxosConsensusCoordinator(["node_east_1", "node_east_2", "node_west_1", "node_eu_1", "node_eu_2"])
    
    # Propose global cluster leader
    result = coordinator.propose("agent_cluster_leader_alpha")
    print("Paxos Consensus Outcome:", result)
    print("Decided Value:", coordinator.chosen_value)

if __name__ == "__main__":
    main()
