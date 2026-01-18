from pydantic import BaseModel, Field, field_validator
import re

class Structure(BaseModel):
    tldr: str = Field(description="translation of the original paper abstract in the specified language")
    motivation: str = Field(description="describe the motivation in this paper in the specified language")
    method: str = Field(description="method of this paper described in the specified language")
    result: str = Field(description="result of this paper described in the specified language")
    conclusion: str = Field(description="conclusion of this paper described in the specified language")
    tags: list[str] = Field(description="list of tags for the paper (e.g., LLM, Agent, GRT, Skills, etc.)")
    score: int = Field(description="score of the paper from 1 to 5 (1 not recommended, 5 highly recommended)")
    recommendation_reason: str = Field(description="reason for recommending or not recommending the paper in the specified language")