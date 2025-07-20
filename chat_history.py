class ChatManager:
    def __init__(self):
        self.history = []
        self.summary = ""

    def add_to_history(self, role: str, content: str):
        """Add a message to history."""
        if role not in ["user", "assistant"]:
            raise ValueError("Invalid role. Must be 'user' or 'assistant'.")
        self.history.append({"role": role, "content": content})

    def get_history(self):
        """Return the current chat history."""
        return self.history

    def reset(self):
        """Clear chat history and summary."""
        self.history = []
        self.summary = ""

    def set_summary(self, summary: str):
        """Set the current summary."""
        self.summary = summary

    def get_summary(self):
        """Get the current summary."""
        return self.summary
