from groq import Groq
import json
import logging
import os

logger = logging.getLogger(__name__)

SYSTEM_DESIGN_CRITERIA = """
Evaluate across these dimensions:
- Requirements clarification (functional & non-functional)
- Scale estimation (users, QPS, storage)
- High-level architecture (components, services)
- Database choices and data modeling
- Scalability (horizontal scaling, sharding, replication)
- Caching strategy (Redis, CDN, local cache)
- API design (REST/GraphQL endpoints)
- Trade-offs acknowledged (CAP theorem, consistency vs availability)
"""

class AIFeedbackService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = 'llama-3.3-70b-versatile'

    def evaluate_answer(self, question: str, expected_answer: str, user_answer: str, category: str = 'General') -> dict:
        """
        Evaluate user's interview answer using Groq (Llama 3.3 70B).
        Uses category-specific prompts for richer, more relevant feedback.
        Returns: {score, feedback, strengths, improvements}
        """
        if category == 'System Design':
            prompt = f"""You are a senior software engineer conducting a system design interview.

Question: {question}
Key Points to Cover: {expected_answer}
Candidate's Answer: {user_answer}

Evaluate using these system design criteria:
{SYSTEM_DESIGN_CRITERIA}

Respond with ONLY valid JSON (no markdown, no extra text):
{{
    "score": <0-100 integer>,
    "feedback": "<2-3 sentence assessment focusing on architecture quality and completeness>",
    "strengths": ["<specific system design strength>", "<specific system design strength>"],
    "improvements": ["<specific missing component or weak area>", "<specific missing component or weak area>"]
}}

Score guide: 85+ covers all dimensions well, 65-84 covers most, below 65 misses key areas."""

        elif category == 'Behavioral':
            prompt = f"""You are an expert interviewer evaluating a behavioral interview answer using the STAR method.

Question: {question}
Key Points Expected: {expected_answer}
Candidate's Answer: {user_answer}

Evaluate: Situation, Task, Action, Result clarity. Did they quantify impact? Was it specific?

Respond with ONLY valid JSON (no markdown, no extra text):
{{
    "score": <0-100 integer>,
    "feedback": "<2-3 sentence assessment of STAR structure and impact>",
    "strengths": ["<STAR strength>", "<communication strength>"],
    "improvements": ["<missing STAR element or vagueness>", "<improvement area>"]
}}"""

        else:
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

        logger.info(f"Requesting AI evaluation — category={category} model={self.model}")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3,
            )
        except Exception as e:
            logger.error(f"Groq API call failed: {e}", exc_info=True)
            return {
                "score": 50,
                "feedback": "AI service is temporarily unavailable. Please try again.",
                "strengths": [],
                "improvements": ["Try again in a moment"]
            }

        text = response.choices[0].message.content.strip()

        # Strip markdown code fences if present
        if text.startswith('```'):
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:]
            text = text.strip()

        try:
            result = json.loads(text)
            logger.info(f"AI evaluation complete — score={result.get('score')}")
            return result
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            logger.error(f"Failed to parse AI response as JSON: {e}. Raw response: {text[:200]}")
            return {
                "score": 50,
                "feedback": "Unable to evaluate at this time. Please try again.",
                "strengths": [],
                "improvements": ["Review the expected answer and try again"]
            }
