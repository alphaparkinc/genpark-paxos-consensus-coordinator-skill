"""Paxos Single Decree Consensus Engine.
100% Python Standard Library.
"""

from typing import Dict, List, Any

class PaxosAcceptor:
    def __init__(self, acceptor_id: str):
        self.acceptor_id = acceptor_id
        self.promised_prop_num: int = 0
        self.accepted_prop_num: int = 0
        self.accepted_val: Any = None

    def receive_prepare(self, prop_num: int) -> Dict[str, Any]:
        if prop_num > self.promised_prop_num:
            self.promised_prop_num = prop_num
            return {
                "ok": True,
                "acceptor_id": self.acceptor_id,
                "accepted_prop_num": self.accepted_prop_num,
                "accepted_val": self.accepted_val
            }
        return {"ok": False, "acceptor_id": self.acceptor_id, "promised_num": self.promised_prop_num}

    def receive_accept(self, prop_num: int, val: Any) -> Dict[str, Any]:
        if prop_num >= self.promised_prop_num:
            self.promised_prop_num = prop_num
            self.accepted_prop_num = prop_num
            self.accepted_val = val
            return {"ok": True, "acceptor_id": self.acceptor_id}
        return {"ok": False, "acceptor_id": self.acceptor_id}

class PaxosConsensusCoordinator:
    """Coordinator executing Paxos consensus across a cluster of acceptors."""

    def __init__(self, acceptor_ids: List[str]):
        self.acceptors = {aid: PaxosAcceptor(aid) for aid in acceptor_ids}
        self.quorum_size = len(acceptor_ids) // 2 + 1
        self.prop_counter = 0
        self.chosen_value: Any = None

    def propose(self, value: Any) -> Dict[str, Any]:
        self.prop_counter += 1
        prop_num = self.prop_counter

        # Phase 1: Prepare
        promises = []
        highest_accepted_num = 0
        val_to_propose = value

        for aid, acceptor in self.acceptors.items():
            res = acceptor.receive_prepare(prop_num)
            if res["ok"]:
                promises.append(res)
                if res["accepted_prop_num"] > highest_accepted_num and res["accepted_val"] is not None:
                    highest_accepted_num = res["accepted_prop_num"]
                    val_to_propose = res["accepted_val"]

        if len(promises) < self.quorum_size:
            return {"consensus": False, "reason": "Failed to achieve prepare quorum"}

        # Phase 2: Accept
        accepts = []
        for aid, acceptor in self.acceptors.items():
            res = acceptor.receive_accept(prop_num, val_to_propose)
            if res["ok"]:
                accepts.append(res)

        if len(accepts) >= self.quorum_size:
            self.chosen_value = val_to_propose
            return {"consensus": True, "chosen_value": val_to_propose, "proposal_num": prop_num}
        return {"consensus": False, "reason": "Failed to achieve accept quorum"}
