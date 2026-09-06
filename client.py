import random
from typing import Dict, Any, List

class ConversationalFillerLatencyMasker:
    """
    Selects natural acoustic filler cues ('hmm', 'let me see', 'right', 'got it')
    to stream during the 200-800ms gap between user turn completion and model synthesis.
    """
    FILLERS = {
        "acknowledgement": ["Got it.", "Right.", "I understand.", "Makes sense."],
        "computation": ["Let me check that for you.", "Looking into this now.", "One second while I pull that up."],
        "deep_reasoning": ["Hmm, let's see.", "That's an interesting question, let me check.", "Good point, looking at that now."],
        "confirmation": ["Sure thing.", "Absolutely.", "Understood."]
    }

    def determine_filler_injection(
        self,
        user_utterance: str,
        estimated_inference_latency_ms: int,
        filler_cadence_threshold_ms: int = 350
    ) -> Dict[str, Any]:
        low = user_utterance.lower().strip()
        needs_filler = estimated_inference_latency_ms >= filler_cadence_threshold_ms

        if not needs_filler:
            return {
                "inject_filler": False,
                "filler_phrase": None,
                "category": "none",
                "estimated_latency_ms": estimated_inference_latency_ms,
                "latency_saved_perception_ms": 0
            }

        # Contextual categorization
        if any(w in low for w in ["why", "how", "compare", "calculate", "analyze", "explain"]):
            category = "deep_reasoning"
        elif any(w in low for w in ["check", "find", "search", "lookup", "balance", "status"]):
            category = "computation"
        elif any(w in low for w in ["can you", "please", "could you"]):
            category = "confirmation"
        else:
            category = "acknowledgement"

        chosen_filler = self.FILLERS[category][0]

        return {
            "inject_filler": True,
            "filler_phrase": chosen_filler,
            "category": category,
            "estimated_latency_ms": estimated_inference_latency_ms,
            "latency_saved_perception_ms": min(estimated_inference_latency_ms, 450)
        }
