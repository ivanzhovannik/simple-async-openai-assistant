from pydantic import BaseModel, Field


class MathSolution(BaseModel):
    equation: str = Field(..., examples=["sin(x) = 1"])
    solution: str | float = Field(..., examples=["pi/2 + 2*pi*k, where k is an integer"])

# Define your OutputSchema for parsing
OutputSchema = MathSolution

class Query(BaseModel):
    messages: list[dict[str, str]] = Field(
        ...,
        examples=[[
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
            },
            {
                "content": "Solve `cos(x) = 1` for x.",
                "role": "user"
            },
        ]]
        )
