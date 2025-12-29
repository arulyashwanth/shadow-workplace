import requests
import time
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.status import Status
from rich.live import Live

# CONFIG
API_URL = "http://127.0.0.1:8000"
console = Console()

def get_hired():
    console.clear()
    console.print(Panel.fit("[bold cyan]🏢 WELCOME TO SHADOW WORKPLACE[/bold cyan]", border_style="cyan"))
    
    prompt_text = Prompt.ask("[bold green]?[/bold green] What job role do you want to simulate?")
    
    with console.status("[bold yellow]Manager is negotiating with DevOps...[/bold yellow]", spinner="dots"):
        try:
            response = requests.post(f"{API_URL}/agent/start_job", json={"prompt": prompt_text})
            data = response.json()
            
            # Extract Repo URL
            msgs = data.get("messages", [])
            last_msg = msgs[-1] if msgs else "No response"
            
            # Find URL
            repo_url = None
            for word in last_msg.split():
                if "github.com" in word:
                    repo_url = word
                    break
            
            console.print(Panel(last_msg, title="[bold green]Job Offer[/bold green]", border_style="green"))
            return repo_url
            
        except Exception as e:
            console.print(f"[bold red]Error connecting to server:[/bold red] {e}")
            return None

def get_roasted(repo_url):
    console.print("\n[bold white]Phase 2: The Review[/bold white]")
    console.print(f"Target Repo: [underline blue]{repo_url}[/underline blue]")
    Prompt.ask("Press [bold red]ENTER[/bold red] when you have pushed your bad code to GitHub...")
    
    with console.status("[bold red]Senior Engineer is judging you...[/bold red]", spinner="bouncingBar"):
        try:
            response = requests.post(f"{API_URL}/agent/review_code", json={"repo_url": repo_url})
            data = response.json()
            review = data.get("messages", ["Error"])[0]
            
            console.print(Panel(Markdown(review), title="[bold red]Code Review Verdict[/bold red]", border_style="red"))
            
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    while True:
        repo = get_hired()
        if repo:
            get_roasted(repo)
        
        if Prompt.ask("Run another simulation?", choices=["y", "n"]) == "n":
            break