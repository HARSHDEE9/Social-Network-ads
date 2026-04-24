from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from chatbot import RuleBasedChatbot


class ChatbotApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.bot = RuleBasedChatbot()
        self.root.title("Basic AI Chatbot")
        self.root.geometry("980x700")
        self.root.minsize(760, 560)
        self.root.configure(bg="#eef3f7")

        self._configure_styles()
        self._build_layout()
        self._show_welcome_message()

    def _configure_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("App.TFrame", background="#eef3f7")
        style.configure("Card.TFrame", background="#f8fbfd")
        style.configure(
            "Title.TLabel",
            background="#eef3f7",
            foreground="#183153",
            font=("Segoe UI Semibold", 24),
        )
        style.configure(
            "Subtitle.TLabel",
            background="#eef3f7",
            foreground="#58708a",
            font=("Segoe UI", 11),
        )
        style.configure(
            "Accent.TButton",
            background="#183153",
            foreground="white",
            borderwidth=0,
            focusthickness=3,
            focuscolor="#183153",
            font=("Segoe UI Semibold", 11),
            padding=(14, 10),
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#21446f")],
            foreground=[("disabled", "#d8e4ef")],
        )
        style.configure(
            "Quick.TButton",
            background="#dbe9f4",
            foreground="#183153",
            borderwidth=0,
            font=("Segoe UI", 10),
            padding=(10, 8),
        )
        style.map("Quick.TButton", background=[("active", "#c7ddee")])

    def _build_layout(self) -> None:
        container = ttk.Frame(self.root, style="App.TFrame", padding=24)
        container.pack(fill="both", expand=True)

        header = ttk.Frame(container, style="App.TFrame")
        header.pack(fill="x", pady=(0, 16))

        ttk.Label(header, text="Basic AI Chatbot", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="A clean Python chatbot with rule-based replies and a friendly interface.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        body = ttk.Frame(container, style="App.TFrame")
        body.pack(fill="both", expand=True)

        sidebar = ttk.Frame(body, style="Card.TFrame", padding=18)
        sidebar.pack(side="left", fill="y", padx=(0, 18))

        ttk.Label(
            sidebar,
            text="Quick Actions",
            background="#f8fbfd",
            foreground="#183153",
            font=("Segoe UI Semibold", 14),
        ).pack(anchor="w", pady=(0, 12))

        quick_messages = [
            "Hello",
            "What can you do?",
            "Tell me a joke",
            "What is the time?",
            "Describe the project",
            "Help",
        ]
        for message in quick_messages:
            ttk.Button(
                sidebar,
                text=message,
                style="Quick.TButton",
                command=lambda text=message: self._send_quick_message(text),
            ).pack(fill="x", pady=6)

        info_text = (
            "This chatbot uses simple keyword matching to generate responses.\n\n"
            "You can customize the rules in chatbot.py and expand it with new intents."
        )
        ttk.Label(
            sidebar,
            text=info_text,
            wraplength=220,
            justify="left",
            background="#f8fbfd",
            foreground="#58708a",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(18, 0))

        chat_card = ttk.Frame(body, style="Card.TFrame", padding=0)
        chat_card.pack(side="left", fill="both", expand=True)

        self.chat_canvas = tk.Canvas(
            chat_card,
            bg="#f8fbfd",
            highlightthickness=0,
            bd=0,
        )
        self.scrollbar = ttk.Scrollbar(chat_card, orient="vertical", command=self.chat_canvas.yview)
        self.chat_frame = ttk.Frame(self.chat_canvas, style="Card.TFrame")

        self.chat_frame.bind(
            "<Configure>",
            lambda event: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")),
        )

        self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        composer = ttk.Frame(container, style="App.TFrame")
        composer.pack(fill="x", pady=(18, 0))

        input_shell = tk.Frame(
            composer,
            bg="#ffffff",
            highlightbackground="#c8d8e6",
            highlightthickness=1,
            bd=0,
        )
        input_shell.pack(side="left", fill="x", expand=True, padx=(0, 12))

        self.user_input = tk.Entry(
            input_shell,
            font=("Segoe UI", 12),
            bd=0,
            relief="flat",
            bg="#ffffff",
            fg="#183153",
            insertbackground="#183153",
        )
        self.user_input.pack(fill="x", padx=14, pady=14)
        self.user_input.bind("<Return>", self._handle_enter)

        ttk.Button(composer, text="Send", style="Accent.TButton", command=self.send_message).pack(side="right")

    def _show_welcome_message(self) -> None:
        self._add_message(
            "Bot",
            "Welcome! I'm your basic AI chatbot. Ask me something or use the quick actions to start.",
            is_user=False,
        )

    def _send_quick_message(self, message: str) -> None:
        self.user_input.delete(0, tk.END)
        self.user_input.insert(0, message)
        self.send_message()

    def _handle_enter(self, _event: tk.Event) -> str | None:
        self.send_message()
        return "break"

    def send_message(self) -> None:
        message = self.user_input.get().strip()
        if not message:
            return

        self._add_message("You", message, is_user=True)
        self.user_input.delete(0, tk.END)

        response = self.bot.get_response(message)
        bot_text = response.message if not response.suggestion else f"{response.message}\n\nTip: {response.suggestion}"
        self.root.after(250, lambda: self._add_message("Bot", bot_text, is_user=False))

    def _add_message(self, sender: str, message: str, *, is_user: bool) -> None:
        wrapper = tk.Frame(self.chat_frame, bg="#f8fbfd", padx=18, pady=10)
        wrapper.pack(fill="x", anchor="e" if is_user else "w")

        header = tk.Label(
            wrapper,
            text=sender,
            bg="#f8fbfd",
            fg="#58708a",
            font=("Segoe UI Semibold", 9),
            anchor="e" if is_user else "w",
        )
        header.pack(anchor="e" if is_user else "w", padx=4, pady=(0, 4))

        bubble_bg = "#183153" if is_user else "#dfeaf2"
        text_fg = "#ffffff" if is_user else "#183153"
        bubble_anchor = "e" if is_user else "w"

        bubble = tk.Label(
            wrapper,
            text=message,
            justify="left",
            wraplength=520,
            bg=bubble_bg,
            fg=text_fg,
            font=("Segoe UI", 11),
            padx=16,
            pady=12,
        )
        bubble.pack(anchor=bubble_anchor)

        self.root.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)
