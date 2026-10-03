from app.services.ai.llm_service import LLMService


class ChatService:

    @staticmethod
    async def handle_text(query: str, db=None):
        """
        General AI Chat.

        AI Chat is intentionally kept separate from:
        - RAG Search
        - Vector Search
        - Disease Detection
        - Crop Recommendation
        """

        try:
            query = query.strip()

            if not query:
                return "Please type a message.", "general"

            system_prompt = """
You are AgriPulse AI, a friendly and helpful agricultural AI assistant.

You are having a normal conversational chat with the user.

Rules:
- Answer greetings naturally.
- Answer general questions naturally.
- Help users with agriculture-related questions when appropriate.
- Do NOT search or retrieve documents.
- Do NOT use RAG.
- Do NOT perform vector search.
- Do NOT pretend that you searched a knowledge base.
- Keep answers clear, useful and reasonably concise.
- If the user asks about something outside agriculture, you may still answer normally.
- Never say "no relevant document found" just because the question is a simple conversation.
"""

            reply = await LLMService.generate_response(
                prompt=query,
                system_prompt=system_prompt,
            )

            return reply, "general"

        except Exception as e:
            return f"Sorry, I couldn't process your message. Error: {str(e)}", "error"