from tiktoken import get_encoding

class TokenService:
    def __init__(self):
        # Cache for the tokenizer to avoid recreating it
        self._tokenizer = get_encoding("o200k_base")

    async def tokenize(
        self,
        text: str
    ) -> tuple[str, list[int]]:
        """
        Tokenize text using the appropriate tokenizer.

        Returns a tuple containing the original text and the list of token offsets.
        """
        return self._tokenizer.decode_with_offsets(self._tokenizer.encode(text))