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
    item_description: str = "" # NEW: For story-based generation
    is_ui: bool = False

@router.post("/projects/{project_id}/generate-code")
async def generate_code(project_id: int, req: CodeGenRequest, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Use description if available, otherwise fallback to title
    gen_context = req.item_description if req.item_description else req.epic_title
    display_title = req.epic_title

    if req.is_ui:
        # Generate UI code based on selected language
        if "React" in req.language:
            code = f"""import React, {{ useState }} from 'react';
import {{ createRoot }} from 'react-dom/client';

const {display_title.replace(' ', '')}App = () => {{
  // State management based on context: {display_title}
  const [data, setData] = useState([]);

  return (
    <div className="min-h-screen bg-[#0f172a] text-slate-200 p-8 font-sans">
      <div className="max-w-5xl mx-auto space-y-8">
        <header className="flex justify-between items-end border-b border-white/10 pb-6">
          <div>
            <h1 className="text-4xl font-black text-white tracking-tight">{display_title}</h1>
            <p className="text-blue-400 font-medium mt-1">Generated Component Prototype</p>
          </div>
          <div className="flex items-center space-x-2 bg-white/5 px-4 py-2 rounded-xl border border-white/10">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
            <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400">React v18 • Active</span>
          </div>
        </header>

        <section class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div class="lg:col-span-2 space-y-6">
            <div class="p-8 bg-blue-600/10 rounded-3xl border border-blue-500/20 relative overflow-hidden group">
              <div class="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <svg width="120" height="120" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>
              </div>
              <h3 class="text-blue-400 text-xs font-black uppercase mb-4 tracking-widest">Requirement Context</h3>
              <p class="text-white text-xl font-medium leading-relaxed italic">
                "{gen_context}"
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="p-6 bg-white/5 rounded-2xl border border-white/10 hover:border-blue-500/50 transition-all cursor-pointer">
                <div class="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center mb-4 text-blue-400">
                  <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                </div>
                <h4 class="font-bold text-white mb-1">Dynamic Logic</h4>
                <p class="text-slate-400 text-sm">Implementation logic for: {display_title}</p>
              </div>
              <div class="p-6 bg-white/5 rounded-2xl border border-white/10 hover:border-purple-500/50 transition-all cursor-pointer">
                <div class="w-10 h-10 rounded-lg bg-purple-500/20 flex items-center justify-center mb-4 text-purple-400">
                  <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 15V3m0 12l-4-4m4 4l4-4M2 17l.621 2.485A2 2 0 004.561 21h14.878a2 2 0 001.94-1.515L22 17"></path></svg>
                </div>
                <h4 class="font-bold text-white mb-1">Data Pipeline</h4>
                <p class="text-slate-400 text-sm">Synchronized with story requirements.</p>
              </div>
            </div>
          </div>

          <aside class="space-y-6">
            <div class="p-6 bg-slate-800/50 rounded-2xl border border-white/5 shadow-xl">
              <h4 class="text-sm font-bold text-slate-300 mb-4 uppercase tracking-wider">Component Specs</h4>
              <div class="space-y-3">
                <div class="flex justify-between text-xs py-2 border-b border-white/5">
                  <span class="text-slate-500">Framework</span>
                  <span class="text-blue-400 font-mono">React v18</span>
                </div>
                <div class="flex justify-between text-xs py-2 border-b border-white/5">
                  <span class="text-slate-500">Styling</span>
                  <span class="text-cyan-400 font-mono">Tailwind CSS</span>
                </div>
                <div class="flex justify-between text-xs py-2">
                  <span class="text-slate-500">Focus</span>
                  <span class="text-purple-400 font-mono italic">Functional UI</span>
                </div>
              </div>
            </div>
          </aside>
        </section>
      </div>
    </div>
  );
}};

export default {display_title.replace(' ', '')}App;"""
            # Browser preview wrapper
            preview = f"""<!DOCTYPE html><html><head><script src="https://unpkg.com/react@18/umd/react.development.js"></script><script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script><script src="https://unpkg.com/@babel/standalone/babel.min.js"></script><script src="https://cdn.tailwindcss.com"></script><style>.glass {{ background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.05); }}</style></head><body><div id="root"></div><script type="text/babel">const App = () => {{ return (<div class="min-h-screen bg-[#0f172a] text-slate-200 p-8 font-sans"><div class="max-w-5xl mx-auto space-y-8"><header class="flex justify-between items-end border-b border-white/10 pb-6"><div><h1 class="text-4xl font-black text-white tracking-tight">{display_title}</h1><p class="text-blue-400 font-medium mt-1">Generated Component Prototype</p></div><div class="flex items-center space-x-2 bg-white/5 px-4 py-2 rounded-xl border border-white/10"><div class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div><span class="text-[10px] font-bold uppercase tracking-widest text-slate-400">React v18 • Active</span></div></header><section class="grid grid-cols-1 lg:grid-cols-3 gap-8"><div class="lg:col-span-2 space-y-6"><div class="p-8 bg-blue-600/10 rounded-3xl border border-blue-500/20 relative overflow-hidden group"><h3 class="text-blue-400 text-xs font-black uppercase mb-4 tracking-widest">Requirement Context</h3><p class="text-white text-xl font-medium leading-relaxed italic text-balance">"{gen_context}"</p></div><div class="grid grid-cols-1 md:grid-cols-2 gap-4"><div class="p-6 bg-white/5 rounded-2xl border border-white/10 hover:border-blue-500/50 transition-all cursor-pointer"><h4 class="font-bold text-white mb-1">Dynamic Logic</h4><p class="text-slate-400 text-sm">Implementation for {display_title}</p></div><div class="p-6 bg-white/5 rounded-2xl border border-white/10 hover:border-purple-500/50 transition-all cursor-pointer"><h4 class="font-bold text-white mb-1">Data Sync</h4><p class="text-slate-400 text-sm">Live updates active.</p></div></div></div><aside class="space-y-6"><div class="p-6 bg-slate-800/50 rounded-2xl border border-white/5 shadow-xl"><h4 class="text-sm font-bold text-slate-300 mb-4 uppercase tracking-wider">Specs</h4><div class="space-y-3"><div class="flex justify-between text-xs py-2 border-b border-white/5"><span class="text-slate-500">Framework</span><span class="text-blue-400 font-mono">React</span></div><div class="flex justify-between text-xs py-2 border-b border-white/5"><span class="text-slate-500">Styling</span><span class="text-cyan-400 font-mono">Tailwind</span></div></div></div></aside></section></div></div>); }}; ReactDOM.createRoot(document.getElementById('root')).render(<App />);</script></body></html>"""
            return {"code": code, "preview": preview}

        elif "Java" in req.language:
            code = f"""import javax.swing.*;
import java.awt.*;

public class {display_title.replace(' ', '')}UI extends JFrame {{
    public {display_title.replace(' ', '')}UI() {{
        setTitle("{display_title} - Java Desktop App");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        JPanel panel = new JPanel();
        panel.setBackground(new Color(15, 23, 42));
        panel.setLayout(new BorderLayout());
        
        JLabel label = new JLabel("{display_title}", SwingConstants.CENTER);
        label.setForeground(Color.WHITE);
        label.setFont(new Font("Inter", Font.BOLD, 32));
        
        // Context label for Java simulation
        JLabel contextLabel = new JLabel("Context: " + "{gen_context[:50]}...", SwingConstants.CENTER);
        contextLabel.setForeground(new Color(148, 163, 184));
        contextLabel.setFont(new Font("Inter", Font.ITALIC, 14));
        
        panel.add(label, BorderLayout.CENTER);
        panel.add(contextLabel, BorderLayout.SOUTH);
        add(panel);
    }}

    public static void main(String[] args) {{
        SwingUtilities.invokeLater(() -> {{
            new {display_title.replace(' ', '')}UI().setVisible(true);
        }});
    }}
}}"""
            # OS Window Simulation for Preview
            preview = f"""<!DOCTYPE html><html><head><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-slate-200 p-10 flex items-center justify-center min-h-screen"><div class="w-full max-w-2xl bg-[#f0f0f0] rounded-lg shadow-2xl overflow-hidden border border-gray-400"><div class="bg-gray-300 px-4 py-2 flex items-center justify-between border-b border-gray-400"><div class="flex items-center space-x-2"><div class="w-3 h-3 rounded-full bg-red-500"></div><div class="w-3 h-3 rounded-full bg-yellow-500"></div><div class="w-3 h-3 rounded-full bg-green-500"></div><span class="ml-2 text-xs font-semibold text-gray-600">{display_title} - Java UI Context</span></div></div><div class="h-[400px] bg-[#0f172a] flex flex-col items-center justify-center text-white p-10"><div class="p-8 border border-white/10 rounded-xl bg-white/5 text-center w-full"><img src="https://upload.wikimedia.org/wikipedia/en/3/30/Java_programming_language_logo.svg" class="w-16 h-16 mx-auto mb-4 opacity-50"><h2 class="text-3xl font-bold">{display_title}</h2><p class="text-blue-400 mt-4 text-sm uppercase font-bold">Requirement Context:</p><p class="text-slate-400 mt-2 italic text-xs">"{gen_context}"</p></div></div></div></body></html>"""
            return {"code": code, "preview": preview}

        elif "Python" in req.language:
            code = f"""import tkinter as tk
from tkinter import ttk

class {display_title.replace(' ', '')}App:
    def __init__(self, root):
        self.root = root
        self.root.title("{display_title}")
        self.root.geometry("800x600")
        self.root.configure(bg="#0f172a")
        
        self.label = tk.Label(root, text="{display_title}", 
                             fg="white", bg="#0f172a", font=("Inter", 24, "bold"))
        self.label.pack(pady=20)
        
        self.desc = tk.Label(root, text="Context: " + "{gen_context[:100]}...", 
                             fg="#94a3b8", bg="#0f172a", font=("Inter", 10, "italic"))
        self.desc.pack(expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = {display_title.replace(' ', '')}App(root)
    root.mainloop()"""
            preview = f"""<!DOCTYPE html><html><head><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-slate-100 p-10 flex items-center justify-center min-h-screen"><div class="w-full max-w-2xl bg-white rounded shadow-xl border border-gray-300"><div class="bg-gray-100 px-4 py-1 flex justify-between border-b border-gray-300"><span class="text-xs text-gray-600">{display_title} - Python Context</span><div class="flex space-x-2"><span class="text-xs">_</span><span class="text-xs">□</span><span class="text-xs">X</span></div></div><div class="h-[400px] bg-[#0f172a] flex items-center justify-center text-white font-mono p-10"><div class="text-center"><div class="text-4xl font-bold mb-4">{display_title}</div><div class="bg-white/5 p-4 rounded border border-white/10 mt-4"><p class="text-[10px] text-blue-400 uppercase font-bold mb-2">Basis of Generation:</p><p class="text-xs text-slate-400 italic">"{gen_context}"</p></div></div></div></div></body></html>"""
            return {"code": code, "preview": preview}

        else:
            # Standard HTML fallback
            code = f"""<!DOCTYPE html>
<html>
<head>
    <title>UI Component Prototype</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#0f172a] text-white min-h-screen p-12 font-sans">
    <div class="max-w-4xl mx-auto space-y-10">
        <header class="border-b border-white/10 pb-8">
            <h1 class="text-5xl font-black tracking-tighter mb-2">Component Prototype</h1>
            <p class="text-blue-400 font-bold uppercase text-xs tracking-[0.2em]">Generated via Smart AI PM</p>
        </header>

        <main class="space-y-8">
            <div class="p-10 bg-blue-600/10 rounded-[2rem] border border-blue-500/20 shadow-2xl shadow-blue-500/5">
                <h3 class="text-blue-400 text-xs font-black uppercase mb-6 tracking-widest flex items-center">
                    <span class="w-8 h-px bg-blue-500/50 mr-3"></span>
                    User Story & Requirements
                </h3>
                <p class="text-slate-200 text-2xl font-medium leading-relaxed italic">
                    "{gen_context}"
                </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="p-8 bg-white/5 rounded-3xl border border-white/5 hover:bg-white/10 transition-all group">
                    <h4 class="text-lg font-bold mb-2 group-hover:text-blue-400 transition-colors">{display_title}</h4>
                    <p class="text-slate-400 text-sm">Primary implementation target based on provided description.</p>
                </div>
                <div class="p-8 bg-white/5 rounded-3xl border border-white/5 flex items-center justify-center border-dashed">
                    <p class="text-slate-500 text-xs font-mono uppercase tracking-widest">{req.language} Environment</p>
                </div>
            </div>
        </main>
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
