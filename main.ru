import os
import json
import threading
import mimetypes
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from app.config import config
from app.logger import logger
from app.database import init_db, create_case, add_document, list_cases, list_documents, save_message
from app.document_manager import detect_type, extract_text
from app.ai_client import LLMClient

APP_DIR = Path(__file__).resolve().parent
PROMPT_FILE = APP_DIR / "resources" / "system_prompt.txt"
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

MODEL = config.get('DE_JURIST_MODEL', 'gpt-5.5')

llm = LLMClient()
init_db()


def load_prompt():
    if PROMPT_FILE.exists():
        return PROMPT_FILE.read_text(encoding="utf-8")
    return ""


def load_history_from_db(case_id):
    # For simplicity, read messages for case
    docs = list_documents(case_id)
    return docs


def save_history_entry(case_id, role, text):
    try:
        save_message(case_id, role, text)
    except Exception as e:
        logger.exception('Failed to save history entry: %s', e)


class DeJuristApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DE-JURIST AI — юридический агент Германии")
        self.geometry("1180x760")
        self.minsize(900, 600)
        self.history = load_history()
        self.attachments = []
        self._build_ui()
        self._render_history()

    def _build_ui(self):
        style = ttk.Style(self)
        try:
            style.theme_use("vista")
        except Exception:
            pass

        root = ttk.Frame(self, padding=10)
        root.pack(fill="both", expand=True)

        header = ttk.Frame(root)
        header.pack(fill="x")
        ttk.Label(header, text="DE-JURIST AI", font=("Segoe UI", 20, "bold")).pack(side="left")
        ttk.Label(header, text="Юридический AI-агент Германии", font=("Segoe UI", 10)).pack(side="left", padx=12, pady=(8,0))
        self.web_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(header, text="Проверять актуальное право", variable=self.web_var).pack(side="right")

        body = ttk.Panedwindow(root, orient="horizontal")
        body.pack(fill="both", expand=True, pady=10)

        left = ttk.Frame(body, width=220)
        body.add(left, weight=0)
        ttk.Label(left, text="Модули", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0,8))
        for text in ["💬 Чат", "📄 Анализ документа", "📑 Мои дела", "✉️ Письма", "⏰ Сроки", "📚 Шаблоны", "⚙️ Настройки"]:
            ttk.Button(left, text=text, command=lambda t=text: self._module_notice(t)).pack(fill="x", pady=3)
        ttk.Separator(left).pack(fill="x", pady=12)
        ttk.Button(left, text="＋ Новый диалог", command=self.new_chat).pack(fill="x")

        center = ttk.Frame(body)
        body.add(center, weight=1)

        self.chat = tk.Text(center, wrap="word", font=("Segoe UI", 11), state="disabled", padx=12, pady=12)
        self.chat.pack(fill="both", expand=True)
        self.chat.tag_configure("user", font=("Segoe UI", 11, "bold"))
        self.chat.tag_configure("assistant", font=("Segoe UI", 11))
        self.chat.tag_configure("system", foreground="#666666")

        attachbar = ttk.Frame(center)
        attachbar.pack(fill="x", pady=(8,4))
        ttk.Button(attachbar, text="📎 Добавить документ", command=self.add_files).pack(side="left")
        self.attach_label = ttk.Label(attachbar, text="Нет вложений")
        self.attach_label.pack(side="left", padx=10)
        ttk.Button(attachbar, text="Очистить", command=self.clear_attachments).pack(side="right")

        bottom = ttk.Frame(center)
        bottom.pack(fill="x")
        self.input = tk.Text(bottom, height=5, wrap="word", font=("Segoe UI", 11))
        self.input.pack(side="left", fill="both", expand=True)
        self.input.bind("<Control-Return>", lambda e: self.send())
        ttk.Button(bottom, text="Отправить\nCtrl+Enter", command=self.send, width=16).pack(side="right", fill="y", padx=(8,0))

        right = ttk.Frame(body, width=240)
        body.add(right, weight=0)
        ttk.Label(right, text="Быстрые действия", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0,8))
        actions = [
            "Проанализировать документ",
            "Проверить сроки",
            "Найти ошибки",
            "Проверить правовую основу",
            "Подготовить Widerspruch",
            "Составить ответ ведомству",
            "Перевести на русский",
            "Перевести на украинский",
        ]
        for action in actions:
            ttk.Button(right, text=action, command=lambda a=action: self.quick_action(a)).pack(fill="x", pady=3)

        self.status = ttk.Label(root, text="Готово")
        self.status.pack(anchor="w")

    def _module_notice(self, name):
        messagebox.showinfo("DE-JURIST AI", f"Модуль «{name}» заложен в архитектуру. В этой первой версии основной рабочий модуль — чат и анализ вложений.")

    def _render_history(self):
        self.chat.configure(state="normal")
        self.chat.delete("1.0", "end")
        for item in self.history:
            role = item.get("role")
            text = item.get("text", "")
            if role == "user":
                self.chat.insert("end", "\nВы:\n", "user")
            elif role == "assistant":
                self.chat.insert("end", "\nDE-JURIST AI:\n", "user")
            else:
                continue
            self.chat.insert("end", text + "\n", "assistant")
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def add_files(self):
        files = filedialog.askopenfilenames(title="Выберите документы", filetypes=[
            ("Документы", "*.pdf *.docx *.doc *.txt *.md *.json"),
            ("Изображения", "*.png *.jpg *.jpeg *.webp"),
            ("Все файлы", "*.*")])
        if files:
            for f in files:
                if f not in self.attachments:
                    self.attachments.append(f)
            self._update_attach_label()

    def clear_attachments(self):
        self.attachments.clear()
        self._update_attach_label()

    def _update_attach_label(self):
        if not self.attachments:
            self.attach_label.config(text="Нет вложений")
        elif len(self.attachments) == 1:
            self.attach_label.config(text=Path(self.attachments[0]).name)
        else:
            self.attach_label.config(text=f"Вложений: {len(self.attachments)}")

    def quick_action(self, action):
        self.input.delete("1.0", "end")
        self.input.insert("1.0", action + ". Проанализируй предоставленные документы и дай результат по стандартной структуре агента.")
        self.send()

    def new_chat(self):
        if messagebox.askyesno("Новый диалог", "Начать новый диалог и очистить текущую историю?", parent=self):
            self.history = []
            save_history(self.history)
            self._render_history()
            self.clear_attachments()

    def send(self):
        text = self.input.get("1.0", "end").strip()
        if not text and not self.attachments:
            return
        if OpenAI is None:
            messagebox.showerror("Ошибка", "Не установлен пакет openai. Запустите install.bat.")
            return
        if not os.getenv("OPENAI_API_KEY"):
            messagebox.showerror("API-ключ", "Не найден OPENAI_API_KEY. Сначала настройте ключ OpenAI и затем перезапустите приложение.")
            return

        self.input.delete("1.0", "end")
        self.history.append({"role":"user", "text": text or "Проанализируй вложенные документы."})
        self._render_history()
        attachments = list(self.attachments)
        self.clear_attachments()
        self.status.config(text="Анализирую…")
        threading.Thread(target=self._call_api, args=(text, attachments), daemon=True).start()

    def _call_api(self, text, attachments):
        try:
            client = OpenAI()
            content = []
            if text:
                content.append({"type": "input_text", "text": text})
            for path in attachments:
                p = Path(path)
                mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
                with p.open("rb") as fh:
                    uploaded = client.files.create(file=fh, purpose="user_data")
                if mime.startswith("image/"):
                    content.append({"type": "input_image", "file_id": uploaded.id, "detail": "high"})
                else:
                    content.append({"type": "input_file", "file_id": uploaded.id})

            messages = []
            for item in self.history[-12:]:
                if item["role"] == "user":
                    messages.append({"role":"user", "content": item["text"]})
                elif item["role"] == "assistant":
                    messages.append({"role":"assistant", "content": item["text"]})
            messages.append({"role":"user", "content": content})

            tools = [{"type":"web_search"}] if self.web_var.get() else []
            response = client.responses.create(
                model=MODEL,
                instructions=load_prompt(),
                input=messages,
                tools=tools,
            )
            answer = response.output_text
            self.after(0, lambda: self._finish(answer))
        except Exception as exc:
            self.after(0, lambda: self._finish("Ошибка при обращении к AI:\n\n" + str(exc)))

    def _finish(self, answer):
        self.history.append({"role":"assistant", "text":answer})
        save_history(self.history)
        self._render_history()
        self.status.config(text="Готово")


if __name__ == "__main__":
    app = DeJuristApp()
    app.mainloop()
