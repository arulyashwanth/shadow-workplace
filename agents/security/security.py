import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_code_from_github(repo_url):
    """Fetches the code AND the filename."""
    try:
        clean_url = repo_url.rstrip("/")
        parts = clean_url.split("/")
        owner, repo = parts[-2], parts[-1]
        
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        response = requests.get(api_url, headers=HEADERS)
        
        if response.status_code != 200: return "ERROR_ACCESS", "Unknown"

        files = response.json()
        target_file = None
        
        # Priority: Look for main.py first, then app.py, then any .py
        if isinstance(files, list):
            # Sort so we prioritize main.py
            files.sort(key=lambda x: 0 if x["name"] == "main.py" else 1)
            
            for f in files:
                if f["name"].endswith(".py"):
                    target_file = f
                    break
        
        if not target_file: return "NO_PYTHON_CODE", "None"

        return requests.get(target_file["download_url"]).text, target_file["name"]
    except Exception as e:
        return f"ERROR: {str(e)}", "Error"

def security_node(state):
    print("--- SECURITY AGENT STARTED ---")
    repo_url = state.get("repo_url", "")
    
    # 1. Fetch Code
    code, filename = get_code_from_github(repo_url)
    
    print(f"🔎 Scanning File: {filename}")
    
    if code == "NO_PYTHON_CODE" or "ERROR" in code:
        return {"messages": ["Security Passed (No Code)"], "security_status": "clean"}

    # 2. Check for Google Keys
    if "AIza" in code:
        # Find the specific line for debugging
        for line in code.splitlines():
            if "AIza" in line:
                print(f"🚨 DETECTED 'AIza' on line: {line.strip()}")
        
        return {
            "messages": [f"🚨 SECURITY BLOCK: Found Google Key in {filename}. Remove 'AIza...'."],
            "security_status": "blocked" 
        }

    # 3. Check for OpenAI Keys (Smarter Regex)
    # Looks for 'sk-' followed by 20+ chars, ignoring 'task-manager' etc.
    if re.search(r"\bsk-[a-zA-Z0-9]{20,}", code):
        print(f"🚨 DETECTED 'sk-' Key Pattern in {filename}")
        return {
            "messages": [f"🚨 SECURITY BLOCK: Found OpenAI Key in {filename}."],
            "security_status": "blocked" 
        }
    
    print("✅ Security Check Passed.")
    return {
        "messages": ["Security check passed."], 
        "security_status": "clean"
    }