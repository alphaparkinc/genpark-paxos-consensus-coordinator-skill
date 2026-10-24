"""MCP Server for GenPark Paxos Consensus Coordinator.
100% Python Standard Library.
"""

import json
import sys
from client import PaxosConsensusCoordinator

paxos = PaxosConsensusCoordinator(["node1", "node2", "node3", "node4", "node5"])

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "propose_value",
                        "description": "Propose a state value through Paxos Phase 1 & Phase 2",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"value": {"type": "string"}},
                            "required": ["value"]
                        }
                    },
                    {
                        "name": "get_chosen_value",
                        "description": "Get currently decided consensus value",
                        "inputSchema": {"type": "object"}
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "propose_value":
            val = args.get("value", "")
            res = paxos.propose(val)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }
        elif name == "get_chosen_value":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps({"chosen_value": paxos.chosen_value})}]}
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
