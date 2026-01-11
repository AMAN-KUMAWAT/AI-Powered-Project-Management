from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.project import Project
from pydantic import BaseModel
import random

router = APIRouter()

class CodeGenRequest(BaseModel):
    epic_title: str
    language: str
    is_ui: bool = False

@router.post("/projects/{project_id}/generate-code")
async def generate_code(project_id: int, req: CodeGenRequest, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if req.is_ui:
        # Generate UI code based on selected language
        if "React" in req.language:
            code = f"""import React from 'react';
import {{ createRoot }} from 'react-dom/client';

const {req.epic_title.replace(' ', '')}App = () => {{
  return (
    <div className="min-h-screen bg-slate-900 text-white p-8 font-sans">
      <div className="max-w-4xl mx-auto glass p-10 rounded-3xl border border-white/10 shadow-2xl">
        <header className="flex justify-between items-center mb-10">
          <h1 className="text-4xl font-black tracking-tight">{req.epic_title}</h1>
          <span className="bg-blue-500/20 text-blue-400 px-4 py-1 rounded-full text-xs font-bold uppercase">React v18</span>
        </header>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-6 bg-white/5 rounded-2xl border border-white/10 hover:bg-white/10 transition-all cursor-pointer">
            <h3 className="text-xl font-bold mb-2">Live Component</h3>
            <p className="text-slate-400 text-sm">This is a real React functional component rendered in real-time.</p>
          </div>
        </div>
      </div>
    </div>
  );
}};

export default {req.epic_title.replace(' ', '')}App;"""
            # Browser preview wrapper
            preview = f"""<!DOCTYPE html><html><head><script src="https://unpkg.com/react@18/umd/react.development.js"></script><script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script><script src="https://unpkg.com/@babel/standalone/babel.min.js"></script><script src="https://cdn.tailwindcss.com"></script></head><body><div id="root"></div><script type="text/babel">const App = () => {{ return (<div class="min-h-screen bg-slate-900 text-white p-8 font-sans"><div class="max-w-4xl mx-auto bg-white/5 p-10 rounded-3xl border border-white/10 shadow-2xl"><header class="flex justify-between items-center mb-10"><h1 class="text-4xl font-black tracking-tight">{req.epic_title}</h1><span class="bg-blue-500/20 text-blue-400 px-4 py-1 rounded-full text-xs font-bold uppercase">React</span></header><div class="p-12 border-2 border-dashed border-white/10 rounded-2xl text-center"><p class="text-slate-400">React Functional Component</p></div></div></div>); }}; ReactDOM.createRoot(document.getElementById('root')).render(<App />);</script></body></html>"""
            return {"code": code, "preview": preview}

        elif "Java" in req.language:
            code = f"""import javax.swing.*;
import java.awt.*;

public class {req.epic_title.replace(' ', '')}UI extends JFrame {{
    public {req.epic_title.replace(' ', '')}UI() {{
        setTitle("{req.epic_title} - Java Desktop App");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        JPanel panel = new JPanel();
        panel.setBackground(new Color(15, 23, 42));
        panel.setLayout(new BorderLayout());
        
        JLabel label = new JLabel("{req.epic_title}", SwingConstants.CENTER);
        label.setForeground(Color.WHITE);
        label.setFont(new Font("Inter", Font.BOLD, 32));
        
        panel.add(label, BorderLayout.CENTER);
        add(panel);
    }}

    public static void main(String[] args) {{
        SwingUtilities.invokeLater(() -> {{
            new {req.epic_title.replace(' ', '')}UI().setVisible(true);
        }});
    }}
}}"""
            # OS Window Simulation for Preview
            preview = f"""<!DOCTYPE html><html><head><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-slate-200 p-10 flex items-center justify-center min-h-screen"><div class="w-full max-w-2xl bg-[#f0f0f0] rounded-lg shadow-2xl overflow-hidden border border-gray-400"><div class="bg-gray-300 px-4 py-2 flex items-center justify-between border-b border-gray-400"><div class="flex items-center space-x-2"><div class="w-3 h-3 rounded-full bg-red-500"></div><div class="w-3 h-3 rounded-full bg-yellow-500"></div><div class="w-3 h-3 rounded-full bg-green-500"></div><span class="ml-2 text-xs font-semibold text-gray-600">{req.epic_title} - Java Swing Application</span></div></div><div class="h-[400px] bg-[#0f172a] flex flex-col items-center justify-center text-white"><div class="p-8 border border-white/10 rounded-xl bg-white/5 text-center"><img src="https://upload.wikimedia.org/wikipedia/en/3/30/Java_programming_language_logo.svg" class="w-16 h-16 mx-auto mb-4 opacity-50"><h2 class="text-3xl font-bold">{req.epic_title}</h2><p class="text-slate-400 mt-2">Java Desktop Simulation</p><button class="mt-6 px-6 py-2 bg-blue-600 rounded text-sm font-bold">Swing Action</button></div></div></div></body></html>"""
            return {"code": code, "preview": preview}

        elif "Python" in req.language:
            code = f"""import tkinter as tk
from tkinter import ttk

class {req.epic_title.replace(' ', '')}App:
    def __init__(self, root):
        self.root = root
        self.root.title("{req.epic_title}")
        self.root.geometry("800x600")
        self.root.configure(bg="#0f172a")
        
        self.label = tk.Label(root, text="{req.epic_title}", 
                             fg="white", bg="#0f172a", font=("Inter", 24, "bold"))
        self.label.pack(expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = {req.epic_title.replace(' ', '')}App(root)
    root.mainloop()"""
            preview = f"""<!DOCTYPE html><html><head><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-slate-100 p-10 flex items-center justify-center min-h-screen"><div class="w-full max-w-2xl bg-white rounded shadow-xl border border-gray-300"><div class="bg-gray-100 px-4 py-1 flex justify-between border-b border-gray-300"><span class="text-xs text-gray-600">{req.epic_title} - Tkinter</span><div class="flex space-x-2"><span class="text-xs">_</span><span class="text-xs">□</span><span class="text-xs">X</span></div></div><div class="h-[400px] bg-[#0f172a] flex items-center justify-center text-white font-mono"><div class="text-center"><div class="text-4xl font-bold mb-4">Python UI</div><div class="text-xl text-blue-400">{req.epic_title}</div></div></div></div></body></html>"""
            return {"code": code, "preview": preview}

        else:
            # Standard HTML fallback
            code = f"""<!DOCTYPE html>
<html>
<head>
    <title>{req.epic_title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-white min-h-screen p-12">
    <div class="max-w-4xl mx-auto glass p-12 rounded-3xl border border-white/10 bg-white/5">
        <h1 class="text-5xl font-black mb-6 tracking-tighter">{req.epic_title}</h1>
        <p class="text-slate-400 text-lg leading-relaxed">{req.language} implementation dashboard.</p>
    </div>
</body>
</html>"""
            return {"code": code, "preview": code}

    # Rest of the snippets for non-UI requests

    # Standard logic snippets...
    
    languages_snippets = {
        "Python": [
            f"class {req.epic_title.replace(' ', '')}Manager:\n    def __init__(self):\n        self.data = []\n\n    def process_feature(self):\n        # Logic for {req.epic_title}\n        print('Processing {req.epic_title}...')",
            f"import os\n\ndef run_{req.epic_title.lower().replace(' ', '_')}():\n    \"\"\"Implementation for {req.epic_title}\"\"\"\n    return f'Executing {req.epic_title} logic'"
        ],
        "JavaScript": [
            f"class {req.epic_title.replace(' ', '')}Service {{\n    constructor() {{\n        this.items = [];\n    }}\n\n    async handleFeature() {{\n        console.log('Handling {req.epic_title}...');\n    }}\n}}",
            f"const start{req.epic_title.replace(' ', '')} = () => {{\n    // Logic for {req.epic_title}\n    return `Success for ${{req.epic_title}}`;\n}};"
        ],
        "TypeScript": [
            f"interface I{req.epic_title.replace(' ', '')} {{\n    id: string;\n    name: string;\n}}\n\nexport class {req.epic_title.replace(' ', '')}Controller {{\n    execute(): void {{\n        console.log('Running {req.epic_title}');\n    }}\n}}",
        ],
        "Java": [
            f"public class {req.epic_title.replace(' ', '')}Feature {{\n    private String status;\n\n    public void process() {{\n        System.out.println(\"Processing {req.epic_title}...\");\n    }}\n}}",
        ],
        "C#": [
            f"namespace SmartAI.Features\n{{\n    public class {req.epic_title.replace(' ', '')}Handler\n    {{\n        public void Run() => Console.WriteLine(\"Executing {req.epic_title}\");\n    }}\n}}",
        ],
        "PHP": [
            f"<?php\n\nclass {req.epic_title.replace(' ', '')}Controller\n{{\n    public function handle()\n    {{\n        return 'Handling {req.epic_title}';\n    }}\n}}",
        ],
        "Go": [
            f"package main\n\nimport \"fmt\"\n\nfunc Handle{req.epic_title.replace(' ', '')}() {{\n    fmt.Println(\"Processing {req.epic_title}\")\n}}",
        ],
        "Rust": [
            f"pub fn handle_{req.epic_title.lower().replace(' ', '_')}() {{\n    println!(\"Processing {req.epic_title}\");\n}}",
        ],
        "Ruby": [
            f"class {req.epic_title.replace(' ', '')}Handler\n  def handle\n    puts \"Handling {req.epic_title}\"\n  end\nend",
        ]
    }
    
    snippets = languages_snippets.get(req.language, ["// No snippet found for this language"])
    generated_code = random.choice(snippets)
    
    return {"code": generated_code}
