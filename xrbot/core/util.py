class Util:
    @staticmethod
    def formatDate(date):
        return date.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def format_lyrics(unformatted_lyrics: str) -> str:
        """Formats the unformatted lyrics to enhance readability.

        Args:
            unformatted_lyrics (str): Unformatted lyrics as a string.

        Returns:
            str: Formatted lyrics.
        """
        formatted_lyrics = ""
        length = len(unformatted_lyrics)

        # Iterate through each character in the lyrics
        for i in range(length - 2):
            char = unformatted_lyrics[i]
            formatted_lyrics += char

            # Conditions for adding a line break
            if (
                (char.islower() and unformatted_lyrics[i + 1].isupper())
                or (char in "?!)" and unformatted_lyrics[i + 1] not in "[')")
                or (
                    char.isupper()
                    and unformatted_lyrics[i + 1].isupper()
                    and unformatted_lyrics[i + 2].islower()
                )
                or (char == "'" and unformatted_lyrics[i + 1] == "'")
                or (char == ")" and unformatted_lyrics[i + 1] == "'")
                or (char in ".;")
            ):
                formatted_lyrics += "\n"

        # Add the last two characters to the formatted lyrics
        formatted_lyrics += unformatted_lyrics[-2:]
        formatted_lyrics += unformatted_lyrics[-1]

        # Add a line break after each square bracket for readability
        formatted_lyrics = formatted_lyrics.replace("[", "\n\n[").replace("]", "]\n")

        return formatted_lyrics

    @staticmethod
    def split_lyrics(lyrics: str) -> tuple:
        """Splits lyrics into parts based on the Discord embed field character limit.

        Args:
            lyrics (str): Formatted lyrics as a string.

        Returns:
            tuple: A tuple containing up to three parts of lyrics.
        """
        parts = []
        limit = 1024
        current_index = 0
        lyrics_length = len(lyrics)

        while current_index < lyrics_length:
            # Find the last line break before the character limit
            end_index = min(current_index + limit, lyrics_length)
            while end_index > current_index and lyrics[end_index] != "\n":
                end_index -= 1

            # If no line break is found, use the character limit directly
            if end_index == current_index:
                end_index = min(current_index + limit, lyrics_length)

            # Add the lyrics part to the list
            parts.append(lyrics[current_index:end_index])

            # Update the current index
            current_index = end_index

        return tuple(parts)
