from app.services.rag.retriever import Retriever
from app.services.ai.llm_service import LLMService


class RAGService:

    @staticmethod
    async def ask(query: str) -> str:
        try:
            # Retrieve relevant documents from ChromaDB
            docs = await Retriever.retrieve(query)

            if not docs:
                return (
                    f'📚 "{query}" সম্পর্কে কোনো প্রাসঙ্গিক '
                    f'ডকুমেন্ট পাওয়া যায়নি।'
                )

            # Combine retrieved documents
            context = "\n\n--- DOCUMENT ---\n\n".join(docs)

            prompt = f"""
Knowledge Base Context:
{context}

User Question:
{query}

Language Rule:
- Detect the language of the user's question.
- If the user asks in English, answer entirely in English.
- If the user asks in Bengali, answer entirely in Bengali.
- If the user asks in mixed Bengali-English, answer primarily in Bengali.
- Do not translate an English question into Bengali.
- Do not answer an English question in Bengali.
- Do not mention this language rule in your answer.

Answer Rules:
- Use the knowledge-base context above.
- You are an agricultural expert.
- Give a clear, accurate and useful answer.
- Do not invent information that is not supported by the context.
- If the context does not contain enough information, clearly say so.
"""

            answer = await LLMService.generate_response(
                prompt=prompt,
                system_prompt=(
                    "You are AgriPulse AI, a helpful agricultural assistant. "
                    "Always answer in the same language as the user's question. "
                    "Use the provided agricultural knowledge base as the primary source."
                )
            )

            return answer

        except Exception as e:
            print(f"RAG Service Error: {e}")
            return f"RAG Error: {str(e)}"

