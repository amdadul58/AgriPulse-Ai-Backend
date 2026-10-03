import ollama


class LLMService:

    MODEL_NAME = "gemma4:31b-cloud"

    @staticmethod
    async def generate_response(
        prompt: str,
        system_prompt: str = (
            "You are AgriPulse AI, a helpful agricultural assistant. "
            "Always answer in Bengali. "
            "Use simple, clear Bengali language."
        ),
    ) -> str:

        response = await ollama.AsyncClient().chat(
            model=LLMService.MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response["message"]["content"]