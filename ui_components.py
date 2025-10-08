"""
Beautiful CLI UI Components using Rich library
This module provides reusable UI components for the Intelligent Query Router
"""

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.layout import Layout
from rich.text import Text
from rich import box
from typing import List, Dict, Any, Optional
import time

# Initialize console
console = Console()


class UIComponents:
    """Collection of beautiful UI components for the CLI"""
    
    @staticmethod
    def print_banner():
        """Display a beautiful welcome banner"""
        banner_text = """
[bold cyan]╔══════════════════════════════════════════════════════════════════════════════╗[/bold cyan]
[bold cyan]║[/bold cyan]                                                                              [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                    [bold magenta]🤖 Intelligent Query Router 🤖[/bold magenta]                           [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                              [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]  [white]A Python AI Project that automatically routes your questions to the[/white]        [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]  [white]best tool: Google Search for facts or AI Language Model for analysis[/white]       [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                              [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]  [bold yellow]🎯 Features:[/bold yellow]                                                                [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]     [green]•[/green] [white]Smart query classification[/white]                                             [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]     [green]•[/green] [white]Google Search integration[/white]                                              [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]     [green]•[/green] [white]OpenAI LLM integration[/white]                                                 [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]     [green]•[/green] [white]Automatic tool selection[/white]                                               [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]     [green]•[/green] [white]Real-time web scraping[/white]                                                [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                              [bold cyan]║[/bold cyan]
[bold cyan]╚══════════════════════════════════════════════════════════════════════════════╝[/bold cyan]
        """
        console.print(banner_text)
    
    @staticmethod
    def print_welcome():
        """Display welcome message with examples"""
        welcome_panel = Panel(
            "[bold white]Ask me anything - I'll automatically choose the best tool to answer your question.[/bold white]\n\n"
            "[bold yellow]📝 Examples:[/bold yellow]\n"
            "  [cyan]•[/cyan] [white]'What is the capital of India?'[/white] → [green]Google Search[/green]\n"
            "  [cyan]•[/cyan] [white]'Solve 2x + 5 = 15'[/white] → [blue]AI Language Model[/blue]\n"
            "  [cyan]•[/cyan] [white]'What is machine learning?'[/white] → [blue]AI Language Model[/blue]\n\n"
            "[dim]Type [bold]'quit'[/bold], [bold]'exit'[/bold], or [bold]'q'[/bold] to stop the program.[/dim]",
            title="[bold green]✨ Welcome[/bold green]",
            border_style="green",
            box=box.ROUNDED
        )
        console.print(welcome_panel)
        console.print()
    
    @staticmethod
    def get_user_input(prompt_text: str = "Your question") -> str:
        """Get user input with a beautiful prompt"""
        return Prompt.ask(f"[bold cyan]💭 {prompt_text}[/bold cyan]")
    
    @staticmethod
    def show_processing(message: str = "Processing your query"):
        """Show a processing message"""
        console.print(f"\n[bold yellow]⚡ {message}...[/bold yellow]")
    
    @staticmethod
    def display_result(result: Dict[str, Any]):
        """Display query result in a beautiful format"""
        console.print()
        
        # Handle errors
        if "error" in result:
            error_panel = Panel(
                f"[bold red]{result['error']}[/bold red]",
                title="[bold red]❌ Error[/bold red]",
                border_style="red",
                box=box.ROUNDED
            )
            console.print(error_panel)
            console.print()
            return
        
        # Create info table
        info_table = Table(show_header=False, box=None, padding=(0, 1))
        info_table.add_column("Label", style="bold cyan")
        info_table.add_column("Value", style="white")
        
        if "query" in result:
            info_table.add_row("📝 Query:", result['query'])
        
        if "source" in result:
            source_icon = "🔍" if "Google" in result['source'] else "🤖"
            info_table.add_row(f"{source_icon} Tool Used:", result['source'])
        
        if "query_type" in result:
            type_color = "green" if result['query_type'] == "search" else "blue"
            info_table.add_row("🏷️  Query Type:", f"[{type_color}]{result['query_type']}[/{type_color}]")
        
        # Display info panel
        info_panel = Panel(
            info_table,
            title="[bold yellow]📊 Query Information[/bold yellow]",
            border_style="yellow",
            box=box.ROUNDED
        )
        console.print(info_panel)
        console.print()
        
        # Display answer
        if "answer" in result:
            # Try to render as markdown if it looks like markdown
            answer_text = result['answer']
            if any(marker in answer_text for marker in ['#', '**', '*', '`', '-', '1.']):
                try:
                    answer_content = Markdown(answer_text)
                except:
                    answer_content = answer_text
            else:
                answer_content = answer_text
            
            answer_panel = Panel(
                answer_content,
                title="[bold green]💡 Answer[/bold green]",
                border_style="green",
                box=box.ROUNDED
            )
            console.print(answer_panel)
            console.print()
        
        # Display sources/URLs
        if "urls" in result and result["urls"]:
            sources_text = Text()
            for i, url in enumerate(result["urls"][:5], 1):
                sources_text.append(f"{i}. ", style="bold cyan")
                sources_text.append(f"{url}\n", style="blue underline")
            
            sources_panel = Panel(
                sources_text,
                title="[bold magenta]🔗 Sources[/bold magenta]",
                border_style="magenta",
                box=box.ROUNDED
            )
            console.print(sources_panel)
            console.print()
    
    @staticmethod
    def print_success(message: str):
        """Print a success message"""
        console.print(f"[bold green]✅ {message}[/bold green]")
    
    @staticmethod
    def print_error(message: str):
        """Print an error message"""
        console.print(f"[bold red]❌ {message}[/bold red]")
    
    @staticmethod
    def print_warning(message: str):
        """Print a warning message"""
        console.print(f"[bold yellow]⚠️  {message}[/bold yellow]")
    
    @staticmethod
    def print_info(message: str):
        """Print an info message"""
        console.print(f"[bold cyan]ℹ️  {message}[/bold cyan]")
    
    @staticmethod
    def print_goodbye():
        """Display goodbye message"""
        goodbye_panel = Panel(
            "[bold white]Thank you for using the Intelligent Query Router![/bold white]\n"
            "[dim]Have a great day! 🌟[/dim]",
            title="[bold cyan]👋 Goodbye[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED
        )
        console.print()
        console.print(goodbye_panel)
        console.print()
    
    @staticmethod
    def print_separator():
        """Print a visual separator"""
        console.print("[dim]" + "─" * console.width + "[/dim]")
    
    @staticmethod
    def confirm_action(question: str) -> bool:
        """Ask for user confirmation"""
        return Confirm.ask(f"[bold yellow]❓ {question}[/bold yellow]")
    
    @staticmethod
    def display_conversation_history(history: List[Dict[str, str]]):
        """Display conversation history in a beautiful format"""
        if not history:
            console.print("[dim]No conversation history yet.[/dim]")
            return
        
        console.print("\n[bold cyan]📜 Conversation History[/bold cyan]\n")
        
        for i, message in enumerate(history, 1):
            role = message.get("role", "unknown")
            content = message.get("content", "")
            
            if role == "user":
                icon = "👤"
                color = "cyan"
                title = "You"
            elif role == "assistant":
                icon = "🤖"
                color = "green"
                title = "AI"
            else:
                icon = "❓"
                color = "yellow"
                title = role.capitalize()
            
            panel = Panel(
                content,
                title=f"[bold {color}]{icon} {title}[/bold {color}]",
                border_style=color,
                box=box.ROUNDED
            )
            console.print(panel)
            console.print()
