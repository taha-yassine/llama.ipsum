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
        text, offsets = self._tokenizer.decode_with_offsets(self._tokenizer.encode(text))
        return self._offsets_to_list(text, offsets)
    
    def _offsets_to_list(self, text: str, offsets: list[int]) -> list[str]:
        """
        Convert a string and a list of token offsets to a list of strings.
        """
        return [text[offsets[i]:offsets[i+1]] for i in range(len(offsets)-1)]
