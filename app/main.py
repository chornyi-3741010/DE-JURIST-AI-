import os
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from .config import config
from .logger import logger
from .database import init_db, create_case, list_cases, add_document, list_documents, save_message
from .document_manager import detect_type, extract_text
from .ai_client import LLMClient

APP_DIR = Path(__file__).resolve().parent.parent
PROMPT_PATH = APP_DIR / 'resources' / 'system_prompt.txt'

llm = LLMClient()


def load_prompt():
    if PROMPT_PATH.exists():
        return PROMPT_PATH.read_text(encoding='utf-8')
    return ''


class DeJuristApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('DE-JURIST AI')
        self.geometry('1200x800')
        self.minsize(900, 600)
        self.current_case_id = None
        self.attachments = []

        self._build_ui()
        self._refresh_cases()

    def _build_ui(self):
        menubar = tk.Menu(self)
        filem = tk.Menu(menubar, tearoff=0)
        filem.add_command(label='Neuer Fall', command=self.new_case)
        filem.add_command(label='Einstellungen', command=self.show_settings)
        filem.add_separator()
        filem.add_command(label='Beenden', command=self.quit)
        menubar.add_cascade(label='Datei', menu=filem)
        self.config(menu=menubar)

        root = ttk.Frame(self, padding=8)
        root.pack(fill='both', expand=True)

        left = ttk.Frame(root, width=260)
        left.pack(side='left', fill='y')
        ttk.Label(left, text='Fälle', font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        self.case_listbox = tk.Listbox(left)
        self.case_listbox.pack(fill='both', expand=True, pady=6)
        self.case_listbox.bind('<<ListboxSelect>>', lambda e: self.select_case())
        ttk.Button(left, text='Neuer Fall', command=self.new_case).pack(fill='x')

        center = ttk.Frame(root)
        center.pack(side='left', fill='both', expand=True)

        topc = ttk.Frame(center)
        topc.pack(fill='x')
        ttk.Label(topc, text='Dokumente', font=('Segoe UI', 11, 'bold')).pack(side='left')
        ttk.Button(topc, text='Dokument hinzufügen', command=self.add_files).pack(side='right')

        self.doc_list = tk.Listbox(center)
        self.doc_list.pack(fill='both', expand=True)

        bottom = ttk.Frame(center)
        bottom.pack(fill='x')
        ttk.Button(bottom, text='Dokument analysieren', command=self.analyze_document).pack(side='left')
        ttk.Button(bottom, text='Frist speichern', command=self.save_deadline).pack(side='left', padx=8)
        ttk.Button(bottom, text='Antwort erstellen', command=self.create_answer).pack(side='left', padx=8)

        right = ttk.Frame(root, width=360)
        right.pack(side='right', fill='y')
        ttk.Label(right, text='Chat / Analyse', font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        self.chat = tk.Text(right, wrap='word')
        self.chat.pack(fill='both', expand=True)

        status = ttk.Frame(self)
        status.pack(fill='x')
        self.status_label = ttk.Label(status, text='DE-JURIST AI bereit')
        self.status_label.pack(anchor='w')

    def _refresh_cases(self):
        self.case_listbox.delete(0, 'end')
        for c in list_cases():
            self.case_listbox.insert('end', f"{c['id']}: {c['title']}")

    def select_case(self):
        sel = self.case_listbox.curselection()
        if not sel:
            return
        item = self.case_listbox.get(sel[0])
        cid = int(item.split(':', 1)[0])
        self.current_case_id = cid
        self._refresh_docs()
        self.status_label.config(text=f'Fall {cid} ausgewählt')

    def _refresh_docs(self):
        self.doc_list.delete(0, 'end')
        if not self.current_case_id:
            return
        for d in list_documents(self.current_case_id):
            self.doc_list.insert('end', f"{d['id']}: {d['filename']} ({d['type']})")

    def new_case(self):
        title = tk.simpledialog.askstring('Neuer Fall', 'Titel des Falls:')
        if not title:
            return
        cid = create_case(title)
        self._refresh_cases()
        self.status_label.config(text=f'Fall {cid} erstellt')

    def add_files(self):
        files = filedialog.askopenfilenames(title='Wählen Sie Dateien', filetypes=[('Docs','*.pdf *.docx *.txt'),('Images','*.png *.jpg *.jpeg'),('Alle','*.*')])
        if not files:
            return
        if not self.current_case_id:
            messagebox.showwarning('Kein Fall', 'Wählen Sie zuerst einen Fall oder erstellen Sie einen neuen Fall.')
            return
        for f in files:
            dtype = detect_type(f)
            add_document(self.current_case_id, Path(f).name, dtype)
            self.attachments.append(f)
        self._refresh_docs()
        self.status_label.config(text=f'{len(files)} Dokument(e) hinzugefügt')

    def analyze_document(self):
        sel = self.doc_list.curselection()
        if not sel:
            messagebox.showinfo('Keine Auswahl', 'Bitte wählen Sie ein Dokument aus der Liste.')
            return
        item = self.doc_list.get(sel[0])
        docid = int(item.split(':',1)[0])
        # find path in attachments
        for p in self.attachments:
            if Path(p).name in item:
                text, warns, meta = extract_text(p)
                self.chat.insert('end', f"--- Analyse {Path(p).name} ---\n")
                self.chat.insert('end', text[:4000] + '\n')
                if warns:
                    self.chat.insert('end', '\nWARNINGS:\n' + '\n'.join(warns) + '\n')
                save_message(self.current_case_id, 'assistant', f'Analysed {Path(p).name}')
                self.status_label.config(text='Analyse abgeschlossen')
                return
        messagebox.showwarning('Datei nicht gefunden', 'Die Datei wurde nicht lokal gefunden. Stellen Sie sicher, dass sie nicht verschoben wurde.')

    def save_deadline(self):
        if not self.current_case_id:
            messagebox.showwarning('Kein Fall', 'Wählen Sie zuerst einen Fall.')
            return
        date = tk.simpledialog.askstring('Frist', 'Datum (YYYY-MM-DD):')
        desc = tk.simpledialog.askstring('Beschreibung', 'Beschreibung der Frist:')
        if not date:
            return
        # store in DB
        from .database import get_conn
        conn = get_conn(); cur = conn.cursor()
        cur.execute('INSERT INTO deadlines (case_id, date, description) VALUES (?,?,?)', (self.current_case_id, date, desc))
        conn.commit(); conn.close()
        self.status_label.config(text='Frist gespeichert')

    def create_answer(self):
        if not self.current_case_id:
            messagebox.showwarning('Kein Fall', 'Wählen Sie zuerst einen Fall.')
            return
        prompt = load_prompt()
        # collect recent messages
        messages = []
        # For now, send simple prompt
        try:
            if not llm.available():
                messagebox.showinfo('LLM nicht verfügbar', 'Online-Funktionen sind nicht konfiguriert. Bitte prüfen Sie OPENAI_API_KEY in den Einstellungen.')
                return
            answer = llm.analyze(prompt, [{'role':'user','content':'Bitte analysiere den Fall.'}])
            self.chat.insert('end', '\n=== Antwort des LLM ===\n')
            self.chat.insert('end', answer + '\n')
            save_message(self.current_case_id, 'assistant', answer)
            self.status_label.config(text='Antwort erstellt')
        except Exception as e:
            logger.exception('LLM call failed: %s', e)
            messagebox.showerror('Fehler', 'LLM Anfrage fehlgeschlagen: ' + str(e))


if __name__ == '__main__':
    init_db()
    app = DeJuristApp()
    app.mainloop()
