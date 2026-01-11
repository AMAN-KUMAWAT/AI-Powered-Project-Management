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
        # Generate UI specific HTML/Tailwind code for preview
        ui_code = f"""
<div class="p-8 bg-slate-900 min-h-screen text-white font-sans">
    <div class="max-w-4xl mx-auto">
        <header class="flex justify-between items-center mb-12 border-b border-white/10 pb-6">
            <h1 class="text-3xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
                {req.epic_title}
            </h1>
            <span class="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-full text-xs font-bold uppercase">v1.0.0</span>
        </header>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
            <div class="p-6 bg-white/5 rounded-2xl border border-white/10 hover:border-blue-500/50 transition-all group">
                <div class="w-12 h-12 bg-blue-500/20 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                </div>
                <h3 class="text-xl font-bold mb-2">Fast Performance</h3>
                <p class="text-slate-400 text-sm leading-relaxed">Optimized implementation for the {req.epic_title} module ensuring sub-100ms response times.</p>
            </div>
            
            <div class="p-6 bg-white/5 rounded-2xl border border-white/10 hover:border-purple-500/50 transition-all group">
                <div class="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
                </div>
                <h3 class="text-xl font-bold mb-2">Secure by Default</h3>
                <p class="text-slate-400 text-sm leading-relaxed">Enterprise-grade security protocols integrated directly into the {req.language} architecture.</p>
            </div>
        </div>

        <button class="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl font-bold hover:opacity-90 transition-all shadow-lg shadow-blue-500/25">
            Initialize {req.epic_title}
        </button>
    </div>
</div>
<script src="https://cdn.tailwindcss.com"></script>
"""
        return {"code": ui_code}

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
