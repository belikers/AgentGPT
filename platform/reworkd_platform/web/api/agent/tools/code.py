from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from lanarky.responses import StreamingResponse
from langchain import LLMChain

from reworkd_platform.web.api.agent.model_settings import ModelSettings, create_model
from reworkd_platform.web.api.agent.tools.tool import Tool


class Code(Tool):
    description = (
        "Useful for writing, reviewing, and refactoring code. Can also fix bugs, "
        "and explain programming concepts."
    )
    public_description = "Write and review code."

    def __init__(self, model_settings: ModelSettings):
        super().__init__(model_settings)

    async def call(
        self, goal: str, task: str, input_str: str
    ) -> FastAPIStreamingResponse:
        from reworkd_platform.web.api.agent.prompts import code_prompt

        llm = create_model(self.model_settings, streaming=True)
        chain = LLMChain(llm=llm, prompt=code_prompt)

        return StreamingResponse.from_chain(
            chain,
            {"goal": goal, "language": "English", "task": task},
            media_type="text/event-stream",
        )
