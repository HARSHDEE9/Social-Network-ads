import tkinter as tk

from ui import ChatbotApp


def main() -> None:
    root = tk.Tk()
    ChatbotApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
