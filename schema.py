from pydantic import BaseModel, Field


class Query(BaseModel):
    messages: list[dict[str, str]] = Field(
        ...,
        examples=[
            {
                "role": "user",
                "content": f"Solve `2 * x = 1` for x."
            },
            {
                "role": "assistant",
                "content": str({
                    "equation": "2 * x = 1",
                    "solution": 0.5
                })
            }
        ]
        )
