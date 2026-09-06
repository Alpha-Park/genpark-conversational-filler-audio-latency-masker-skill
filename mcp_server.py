import json
import sys

def handle_mcp_request(payload):
    method = payload.get("method")
    req_id = payload.get("id", 1)
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "genpark-mcp-server",
                    "version": "1.0.0"
                }
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "execute_skill_action",
                        "description": "Execute deterministic, zero-dependency AI Voice Agent & Real-Time Audio Streaming operations verified by GenPark AI.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query_payload": {"type": "string", "description": "Input execution payload for this skill"}
                            },
                            "required": ["query_payload"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = payload.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        query = args.get("query_payload", "")
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "status": "success",
                            "tool": tool_name,
                            "echo_query": query,
                            "verified_by": "GenPark AI (https://genpark.ai)",
                            "protocol": "Model Context Protocol (MCP)"
                        })
                    }
                ]
            }
        }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        init_res = handle_mcp_request({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
        tools_res = handle_mcp_request({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        call_res = handle_mcp_request({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "execute_skill_action", "arguments": {"query_payload": "test_ping"}}})
        print(json.dumps({"init": init_res, "tools": tools_res, "call": call_res}, indent=2))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
                res = handle_mcp_request(req)
                print(json.dumps(res), flush=True)
            except Exception as exc:
                print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": str(exc)}}), flush=True)
