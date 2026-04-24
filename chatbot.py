import random
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ChatResponse:
    message: str
    suggestion: str | None = None


class RuleBasedChatbot:
    def __init__(self) -> None:
        self.greetings = [
            "Hello! How can I help you today?",
            "Hi there! Ask me anything about this demo chatbot.",
            "Hey! I'm ready to chat with you.",
        ]
        self.fallbacks = [
            "I'm still learning. Try asking about the weather, time, date, jokes, or project details.",
            "I don't have a perfect answer for that yet, but I can help with basic questions and small talk.",
            "That one's outside my current rules. Try a simpler question and I'll do my best.",
        ]
        self.jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why did the computer go to therapy? It had too many bytes from the past.",
            "Why was the keyboard so productive? It always had the right type.",
        ]

    def get_response(self, user_input: str) -> ChatResponse:
        cleaned = self._normalize(user_input)
        if not cleaned:
            return ChatResponse(
                "Please type a message so I can respond.",
                "Try saying hello or ask what I can do.",
            )

        if self._matches(cleaned, "bye", "goodbye", "exit", "quit", "see you"):
            return ChatResponse(
                "Goodbye! It was nice chatting with you.",
                "You can close the window whenever you're ready.",
            )

        if self._matches(cleaned, "hello", "hi", "hey", "good morning", "good evening"):
            return ChatResponse(random.choice(self.greetings), "Ask me about this project.")

        if "your name" in cleaned or self._matches(cleaned, "who are you"):
            return ChatResponse(
                "I'm a basic AI chatbot built with Python and rule-based logic.",
                "You can ask what features I have.",
            )

        if self._matches(cleaned, "how are you", "how are you doing"):
            return ChatResponse(
                "I'm doing great and ready to help.",
                "Try asking for a joke or the current date.",
            )

        if "feature" in cleaned or "what can you do" in cleaned:
            return ChatResponse(
                "I can reply to greetings, tell simple jokes, share the current date or time, and explain this project.",
                "Ask me to describe the chatbot project.",
            )

        if "project" in cleaned or "chatbot" in cleaned:
            return ChatResponse(
                "This project is a basic AI chatbot with a stylish Python interface and predefined response rules.",
                "Ask me about the technology used.",
            )

        if "technology" in cleaned or "built with" in cleaned or "python" in cleaned:
            return ChatResponse(
                "This chatbot is built in Python using Tkinter for the graphical user interface.",
                "Ask me how the logic works.",
            )

        if "logic" in cleaned or "how it works" in cleaned or "condition" in cleaned:
            return ChatResponse(
                "I compare your message against predefined keywords and return a matching response based on simple conditions.",
                "You can ask for the source code structure too.",
            )

        if "date" in cleaned:
            from datetime import datetime

            return ChatResponse(
                f"Today's date is {datetime.now().strftime('%d %B %Y')}.",
                "You can also ask for the current time.",
            )

        if "time" in cleaned:
            from datetime import datetime

            return ChatResponse(
                f"The current time is {datetime.now().strftime('%I:%M %p')}.",
                "Ask me for today's date if you want.",
            )

        if "joke" in cleaned or "funny" in cleaned:
            return ChatResponse(random.choice(self.jokes), "Ask for another joke if you want more.")

        if "thank" in cleaned:
            return ChatResponse("You're welcome!", "I'm here if you want to ask another question.")

        if "help" in cleaned:
            return ChatResponse(
                "Try one of these: hello, what can you do, tell me a joke, what is the time, or describe the project.",
                "Use the quick action buttons in the window for shortcuts.",
            )

        return ChatResponse(random.choice(self.fallbacks), "Type help to see supported topics.")

    def _normalize(self, text: str) -> str:
        return re.sub(r"\s+", " ", text.strip().lower())

    def _matches(self, cleaned: str, *phrases: str) -> bool:
        return any(phrase in cleaned for phrase in phrases)
