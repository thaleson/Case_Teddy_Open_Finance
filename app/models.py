"""
Schema module for logging request information.

Defines the structure used to log requests processed by the TalentAI API,
including metadata such as request ID, user ID, timestamp, query, and result.
"""

from pydantic import BaseModel

class LogSchema(BaseModel):
    """
    Schema for logging resume analysis requests.

    Attributes:
        request_id (str): Unique identifier for the request.
        user_id (str): Identifier for the user making the request.
        timestamp (str): UTC timestamp when the request was processed.
        query (str): Optional recruitment-related query submitted by the user.
        result (str): Summary or answer returned by the LLM analysis.
    """
    request_id: str
    user_id: str
    timestamp: str
    query: str
    result: str
