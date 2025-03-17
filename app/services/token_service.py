from tiktoken import get_encoding

class TokenService:
    def __init__(self):
        # Cache for the tokenizer to avoid recreating it
        self._tokenizer = get_encoding("o200k_base")
    
    async def count_tokens(
        self,
        text: str
    ) -> int:
        """
        Count tokens in text using the appropriate tokenizer for the model.
        
        Args:
            text: String or list of strings to count tokens for
            
        Returns:
            Number of tokens in the text
        """
        try:
            return len(self._tokenizer.encode(text))
                
        except Exception as e:
            raise RuntimeError(f"Failed to count tokens: {str(e)}")
        
    async def truncate_text(
        self,
        text: str,
        max_tokens: int
    ) -> str:
        """
        Truncate text to the specified number of tokens.

        Args:
            text: String to truncate
            max_tokens: Maximum number of tokens to keep
            
        Returns:
            Truncated text
        """
        try:
            tokens = self._tokenizer.encode(text)
            return self._tokenizer.decode(tokens[:max_tokens])
        except Exception as e:
            raise ValueError(f"Failed to truncate text: {str(e)}")
    