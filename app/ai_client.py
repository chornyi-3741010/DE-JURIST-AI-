"""AI client wrapper (OpenAI)"""
from typing import List, Dict, Any, Optional
from .config import config
from .logger import logger

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

class LLMClient:
    def __init__(self):
        self.key = config.get('OPENAI_API_KEY')
        self.model = config.get('DE_JURIST_MODEL')
        if not self.key:
            logger.warning('OPENAI_API_KEY not set; online features disabled')
            self.client = None
        else:
            try:
                self.client = OpenAI()
            except Exception as e:
                logger.exception('Failed to init OpenAI client: %s', e)
                self.client = None

    def available(self) -> bool:
        return self.client is not None

    def analyze(self, instructions: str, messages: List[Dict[str,Any]], tools: Optional[List[Dict[str,Any]]] = None) -> str:
        if not self.client:
            raise RuntimeError('LLM client not configured')
        try:
            resp = self.client.responses.create(
                model=self.model,
                instructions=instructions,
                input=messages,
                tools=tools or []
            )
            return getattr(resp, 'output_text', '')
        except Exception as e:
            logger.exception('LLM analyze failed: %s', e)
            raise
