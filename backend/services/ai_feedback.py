import anthropic
import json
import os

class AIFeedbackService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    def evaluate_answer(self, question: str, expected_answer: str, user_answer: str) -> dict:
        """
        Evaluate user's interview answer using Claude AI.
        Returns: {score, feedback, strengths, improvements}
        """
        prompt = f"""You are an expert interview coach evaluating a candidate's answer.

Question: {question}
Expected/Ideal Answer Points: {expected_answer}
Candidate's Answer: {user_answer}

Evaluate the answer and respond with ONLY valid JSON (no markdown, no extra text):
{{
    "score": <0-100 integer>,
    "feedback": "<2-3 sentence overall assessment>",
    "strengths": ["<strength 1>", "<strength 2>"],
    "improvements": ["<improvement 1>", "<improvement 2>"]
}}

Be constructive but honest. Score 80+ for good answers, 50-80 for adequate answers."""

        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Parse JSON response
        try:
            result = json.loads(response.content[0].text)
            return result
        except (json.JSONDecodeError, IndexError, KeyError):
            # Fallback if parsing fails
            return {
                "score": 50,
                "feedback": "Unable to evaluate at this time. Please try again.",
                "strengths": [],
                "improvements": ["Review the expected answer and try again"]
            }
