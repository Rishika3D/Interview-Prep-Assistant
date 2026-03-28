"""
Seed script to populate sample interview questions.
Run: python -m backend.seed
"""
import os
from dotenv import load_dotenv

load_dotenv()

from backend.app import create_app
from backend.models import db, User, Question

SAMPLE_QUESTIONS = [
    # System Design
    {
        "title": "Design a URL Shortener (like bit.ly)",
        "content": "Design a scalable URL shortening service. It should handle 100M URLs created per day and 10B redirects per day.",
        "expected_answer": "Cover: requirements (read-heavy), scale estimation (10B reads/100M writes daily), hashing strategy (MD5/Base62), database (key-value store like DynamoDB), caching (Redis for hot URLs), CDN for redirects, handling collisions, custom aliases, expiry.",
        "category": "System Design",
        "difficulty": "Medium"
    },
    {
        "title": "Design Twitter / X",
        "content": "Design a social media platform like Twitter. Users can post tweets, follow others, and see a home timeline feed.",
        "expected_answer": "Cover: fanout on write vs read, home timeline generation, tweet storage (SQL + Cassandra), celebrity problem (hybrid approach), media storage (S3 + CDN), search (Elasticsearch), rate limiting, notifications, 300M DAU scale.",
        "category": "System Design",
        "difficulty": "Hard"
    },
    {
        "title": "Design a Chat System (like WhatsApp)",
        "content": "Design a real-time messaging system that supports 1-1 and group chats, message delivery receipts, and online presence.",
        "expected_answer": "Cover: WebSocket for real-time, message queue (Kafka), message storage (HBase/Cassandra for write-heavy), delivery receipts (ACK), online presence (heartbeat), group messaging fanout, media attachments (S3), end-to-end encryption overview.",
        "category": "System Design",
        "difficulty": "Hard"
    },
    {
        "title": "Design a Rate Limiter",
        "content": "Design a distributed rate limiter that can handle 1M requests/second and support different rate limiting algorithms.",
        "expected_answer": "Cover: token bucket vs leaky bucket vs sliding window, Redis for distributed counter, Lua scripts for atomic operations, client vs server-side limiting, response headers (X-RateLimit), handling edge cases, where to place in architecture (API gateway).",
        "category": "System Design",
        "difficulty": "Medium"
    },
    {
        "title": "Design a Notification System",
        "content": "Design a notification service that can send push notifications, emails, and SMS to 100M users with different preferences.",
        "expected_answer": "Cover: notification types (push/email/SMS), message queue (Kafka/SQS) for decoupling, third-party integrations (APNs, FCM, Twilio, SendGrid), user preference storage, retry mechanism, rate limiting per user, analytics/tracking, template management.",
        "category": "System Design",
        "difficulty": "Medium"
    },
    # Behavioral
    {
        "title": "Tell me about a time you handled conflict",
        "content": "Describe a situation where you had a disagreement with a colleague or manager. How did you handle it?",
        "expected_answer": "Use STAR method. Show: active listening, empathy, data-driven resolution, outcome focused. Avoid: blaming, staying in conflict, not resolving.",
        "category": "Behavioral",
        "difficulty": "Medium"
    },
    {
        "title": "Describe a project you led end-to-end",
        "content": "Tell me about a project where you took full ownership from inception to delivery. What was your approach?",
        "expected_answer": "STAR: clear problem definition, stakeholder alignment, breaking down into milestones, handling blockers, team coordination, measurable outcome (shipped, % improvement, users impacted).",
        "category": "Behavioral",
        "difficulty": "Medium"
    },
    # Technical
    {
        "title": "Explain the difference between SQL and NoSQL",
        "content": "When would you choose SQL over NoSQL and vice versa? Give real-world examples.",
        "expected_answer": "SQL: ACID, structured data, complex joins, financial systems. NoSQL: scale, flexible schema, high write throughput, document/key-value/graph stores. CAP theorem. Examples: PostgreSQL vs MongoDB vs Redis vs Cassandra.",
        "category": "Technical",
        "difficulty": "Easy"
    },
    {
        "title": "How does indexing work in databases?",
        "content": "Explain database indexing. How does it improve performance? What are the trade-offs?",
        "expected_answer": "B-tree index structure, clustered vs non-clustered, composite indexes, covering indexes. Trade-offs: faster reads, slower writes, storage overhead. When NOT to index: small tables, high-cardinality updates. Explain index on WHERE/JOIN/ORDER BY columns.",
        "category": "Technical",
        "difficulty": "Medium"
    },
]

def seed():
    app = create_app()
    with app.app_context():
        # Create a demo user
        demo_email = "demo@example.com"
        user = User.query.filter_by(email=demo_email).first()

        if not user:
            user = User(email=demo_email)
            user.set_password("demo123")
            db.session.add(user)
            db.session.commit()
            print(f"Created demo user: {demo_email} / demo123")

        # Add sample questions
        added = 0
        for q_data in SAMPLE_QUESTIONS:
            exists = Question.query.filter_by(
                user_id=user.id,
                title=q_data["title"]
            ).first()

            if not exists:
                question = Question(user_id=user.id, **q_data)
                db.session.add(question)
                added += 1

        db.session.commit()
        print(f"Added {added} sample questions for demo user.")
        print(f"\nLogin with: {demo_email} / demo123")

if __name__ == '__main__':
    seed()
