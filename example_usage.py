import json
from client import ConversationalFillerLatencyMasker

def main():
    masker = ConversationalFillerLatencyMasker()
    query = "Can you analyze our cloud spend breakdown for last quarter?"
    result = masker.determine_filler_injection(query, estimated_inference_latency_ms=650)
    print("Conversational Filler Injection:")
    print(json.dumps(result, indent=2))
    assert result["inject_filler"] is True
    assert result["category"] == "deep_reasoning"
    print("Conversational filler masker verification: PASS")

if __name__ == "__main__":
    main()
