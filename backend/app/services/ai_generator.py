from typing import List, Dict

# PUBLIC_INTERFACE
def generate_test_suggestions(prompt: str) -> List[Dict]:
    """
    Return AI-generated test suggestions based on the prompt.
    This is a stub. In a real implementation, integrate with an LLM.

    Returns a list of dictionaries compatible with TestCaseCreateSchema.
    """
    prompt = (prompt or "").strip()
    title_base = prompt[:40] if prompt else "Generated Test"
    suggestions = [
        {
            "title": f"{title_base} - Scenario A",
            "description": "Auto-generated test focusing on the happy path.",
            "status": "draft",
        },
        {
            "title": f"{title_base} - Scenario B",
            "description": "Auto-generated test focusing on edge cases.",
            "status": "draft",
        },
    ]
    return suggestions
