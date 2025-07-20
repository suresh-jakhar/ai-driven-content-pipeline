from colorama import Fore, Style
import textwrap

def display_text_with_comparison(original, rewritten):
    """Display original vs rewritten text in columns"""
    print("\n" + "="*100)
    print(f"{Fore.BLUE}{'ORIGINAL TEXT (excerpt)':^50}{Style.RESET_ALL} | {Fore.GREEN}{'REWRITTEN TEXT (excerpt)':^50}{Style.RESET_ALL}")
    print("="*100)
    
    orig_lines = textwrap.wrap(original[:1000], width=50)
    rewrite_lines = textwrap.wrap(rewritten[:1000], width=50)
    
    for orig, rewrite in zip(orig_lines, rewrite_lines):
        print(f"{Fore.BLUE}{orig.ljust(50)}{Style.RESET_ALL} | {Fore.GREEN}{rewrite.ljust(50)}{Style.RESET_ALL}")

def get_human_feedback(original, rewritten, evaluation):
    """Enhanced CLI for human review with better formatting"""
    print(f"\n{Fore.YELLOW}{' HUMAN REVIEW STAGE ':=^100}{Style.RESET_ALL}")
    
    # Display evaluation summary
    print(f"\n{Fore.CYAN}Evaluation Summary:{Style.RESET_ALL}")
    print(f"Overall Score: {Fore.BLUE}{evaluation['total_score']}/50{Style.RESET_ALL}")
    for cat, score in evaluation["scores"].items():
        color = Fore.GREEN if score >= 7 else Fore.YELLOW if score >=5 else Fore.RED
        print(f"{cat.capitalize()+':':<12} {color}{score}/10{Style.RESET_ALL}")
    
    # Display text comparison
    display_text_with_comparison(original, rewritten)
    
    # Action menu
    print(f"\n{Fore.CYAN}Available Actions:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[A] Accept{Style.RESET_ALL} - Approve the current version")
    print(f"{Fore.YELLOW}[E] Edit{Style.RESET_ALL} - Make manual edits to the text")
    print(f"{Fore.RED}[R] Reject{Style.RESET_ALL} - Discard this version and stop processing")
    
    while True:
        try:
            choice = input(f"\n{Fore.WHITE}Enter your choice (A/E/R): {Style.RESET_ALL}").strip().upper()
            
            if choice == 'A':
                return {"status": "accepted", "edited_text": rewritten}
            elif choice == 'E':
                print(f"\n{Fore.CYAN}Enter your edited text below. Type 'END' on a new line when finished:{Style.RESET_ALL}")
                edited_lines = []
                while True:
                    line = input()
                    if line.strip() == 'END':
                        break
                    edited_lines.append(line)
                edited_text = '\n'.join(edited_lines)
                return {"status": "edited", "edited_text": edited_text}
            elif choice == 'R':
                confirm = input(f"{Fore.RED}Are you sure you want to reject this chapter? (y/n): {Style.RESET_ALL}").lower()
                if confirm == 'y':
                    return {"status": "rejected", "edited_text": ""}
            else:
                print(f"{Fore.RED}Invalid choice. Please enter A, E, or R.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Operation cancelled by user.{Style.RESET_ALL}")
            return {"status": "rejected", "edited_text": ""}