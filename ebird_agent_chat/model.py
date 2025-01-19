from pydantic import BaseModel, Field, field_validator
from typing import Any

class Article(BaseModel):
    title: str = Field(..., pattern=r'^[A-Z][A-Za-z0-9\s]{2,49}$')
    content: str

    @field_validator('content')
    @classmethod
    def validate_content(cls, v: Any) -> str:
        required_words = ['important', 'summary']
        content_lower = v.lower()
        
        missing_words = [word for word in required_words if word not in content_lower]
        
        if missing_words:
            raise ValueError(f"Missing required words: {', '.join(missing_words)}")
        
        return v
