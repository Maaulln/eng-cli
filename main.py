import os
import google.generativeai as genai
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

API_KEY = "AIzaSyCGNst5DFkpOR7X7ydPQbKmwRJIkJBXykU"


console = Console()

def setup_gemini():
    try:
        genai.configure(api_key=API_KEY)
        
        instruction = """
        You are a friendly and helpful English Tutor. 
        Your goal is to help the user practice English conversation via a CLI interface.
        
        Rules:
        1. Keep the conversation natural and engaging.
        2. Keep your responses concise (ideal for CLI).
        3. IMPORTANT: If the user makes a grammar or vocabulary mistake, 
           please correct them gently at the end of your response inside a [Correction] block.
        4. If the user's English is perfect, just continue the conversation naturally.
        5. Speak primarily in English, but you can explain complex grammar in Indonesian if asked.
        """
        
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=instruction
        )
        return model
    except Exception as e:
        console.print(f"[bold red]Error configuring Gemini:[/bold red] {e}")
        return None

def main():
    os.system('cls' if os.name == 'nt' else 'clear') # Bersihkan layar
    
    console.print(Panel.fit(
        "[bold cyan]Welcome to Gemini CLI English Tutor![/bold cyan]\n"
        "Model: [green]Waan AI[/green]\n"
        "Type 'exit' or 'quit' to stop.",
        title="English Dojo"
    ))

    model = setup_gemini()
    if not model:
        return

    # Memulai sesi chat (History otomatis disimpan oleh object chat)
    chat = model.start_chat(history=[])

    while True:
        try:
            # Input user
            user_input = Prompt.ask("\n[bold yellow]You[/bold yellow]")
            
            if user_input.lower() in ['exit', 'quit', 'keluar']:
                console.print("[bold cyan]Goodbye! Keep practicing![/bold cyan]")
                break
            
            if not user_input.strip():
                continue

            # Tampilkan indikator loading sederhana
            with console.status("[bold green]Thinking...[/bold green]", spinner="dots"):
                response = chat.send_message(user_input)
            
            # Tampilkan respons AI dengan format Markdown
            console.print("\n[bold magenta]Tutor Waan:[/bold magenta]")
            console.print(Markdown(response.text))

        except KeyboardInterrupt:
            console.print("\n[bold red]Exiting...[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]An error occurred:[/bold red] {e}")

if __name__ == "__main__":
    main();