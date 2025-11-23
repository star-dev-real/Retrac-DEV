from colorama import Fore, Style, init
import os
from pathlib import Path
import json

init(autoreset=True)
HERE = Path(__file__).parent  
RETRAC = HERE / "Profiles/retrac.json"
COMMON_CORE = HERE / "Profiles/common_core.json"
CONFIG = HERE / "config.json"

class Menu:
    def __init__(self):
        self.author = "Star"
        self.discord = "http://dsc.gg/pynite"

        self.menu_options = [
            "Edit Level",
            "Edit V-Bucks",
            "Edit Username",
            "Start",
            "Exit"
        ]

        self.level: int = 1
        self.vbucks: int = 0
        self.username: str = "Player"

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def title(self):
        self.clear()
        print(Fore.GREEN + Style.BRIGHT + """░██████████                                  ░██                                   
░██                                          ░██                                   
░██        ░██░████  ░███████   ░███████  ░████████ ░██░████  ░██████    ░███████  
░█████████ ░███     ░██    ░██ ░██    ░██    ░██    ░███           ░██  ░██    ░██ 
░██        ░██      ░█████████ ░█████████    ░██    ░██       ░███████  ░██        
░██        ░██      ░██        ░██           ░██    ░██      ░██   ░██  ░██    ░██ 
░██        ░██       ░███████   ░███████      ░████ ░██       ░█████░██  ░███████  
                                                                                   
                                                                                   
                                                                                   """)
        
        print(Fore.CYAN + Style.BRIGHT + f"               Author: {self.author} | Discord: {self.discord}\n")

    def options(self):
        for i, option in enumerate(self.menu_options, start=1):
            print(Fore.YELLOW + Style.BRIGHT + f"               [{i}] {option}")
        print()
    
    def get_choice(self) -> int:
        while True:
            try:
                choice = int(input(Fore.GREEN + Style.BRIGHT + "               Select an option: "))
                if 1 <= choice <= len(self.menu_options):
                    return choice
                else:
                    print(Fore.RED + Style.BRIGHT + "               Invalid option. Please try again.")
            except ValueError:
                print(Fore.RED + Style.BRIGHT + "               Invalid input. Please enter a number.")

    def load_config(self):
        try:
            if CONFIG.exists():
                with open(CONFIG, "r", encoding="utf-8") as f:
                    config = json.load(f)
                
                self.level = config.get("level", 1)
                self.vbucks = config.get("vbucks", 0)
                self.username = config.get("username", "Player")
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"               Error loading config: {e}")

    def save_config(self):
        try:
            config = {
                "level": self.level,
                "vbucks": self.vbucks,
                "username": self.username,
                "display_name_suffix": "(Freetrac)"
            }
            with open(CONFIG, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"               Error saving config: {e}")
            return False

    def display_stats(self):
        self.load_config()
        print(Fore.CYAN + Style.BRIGHT + "               Current Stats:")
        print(Fore.CYAN + Style.BRIGHT + f"               Level: {self.level}")
        print(Fore.CYAN + Style.BRIGHT + f"               V-Bucks: {self.vbucks}")
        print(Fore.CYAN + Style.BRIGHT + f"               Username: {self.username}")
        print()


    def get_level(self) -> int:
        while True:
            try:
                level = int(input(Fore.GREEN + Style.BRIGHT + "               Enter level: "))
                if level >= 1:
                    return level
                else:
                    print(Fore.RED + Style.BRIGHT + "               Level must be at least 1. Please try again.")
            except ValueError:
                print(Fore.RED + Style.BRIGHT + "               Invalid input. Please enter a valid number.")

    def get_vbucks(self) -> int:
        while True:
            try:
                vbucks = int(input(Fore.GREEN + Style.BRIGHT + "               Enter V-Bucks amount: "))
                if vbucks >= 0:
                    return vbucks
                else:
                    print(Fore.RED + Style.BRIGHT + "               V-Bucks cannot be negative. Please try again.")
            except ValueError:
                print(Fore.RED + Style.BRIGHT + "               Invalid input. Please enter a valid number.")

    def get_username(self) -> str:
        while True:
            username = input(Fore.GREEN + Style.BRIGHT + "               Enter username: ").strip()
            if username:
                return username
            else:
                print(Fore.RED + Style.BRIGHT + "               Username cannot be empty. Please try again.")

    def exit_message(self):
        print(Fore.CYAN + Style.BRIGHT + "\n               Thank you for using Freetrac! Goodbye!\n")

    def run(self):
        self.load_config()
        while True:
            self.title()
            self.display_stats()
            self.options()
            choice = self.get_choice()

            if choice == 1:
                self.level = self.get_level()
                if self.save_config():
                    print(Fore.GREEN + Style.BRIGHT + f"\n               Level set to {self.level}!\n")
                input(Fore.YELLOW + Style.BRIGHT + "               Press Enter to continue...")
            elif choice == 2:
                self.vbucks = self.get_vbucks()
                if self.save_config():
                    print(Fore.GREEN + Style.BRIGHT + f"\n               V-Bucks set to {self.vbucks}!\n")
                input(Fore.YELLOW + Style.BRIGHT + "               Press Enter to continue...")
            elif choice == 3:
                self.username = self.get_username()
                if self.save_config():
                    print(Fore.GREEN + Style.BRIGHT + f"\n               Username set to {self.username}!\n")
                input(Fore.YELLOW + Style.BRIGHT + "               Press Enter to continue...")
            elif choice == 4:
                print(Fore.GREEN + Style.BRIGHT + "\n               Starting...\n")
                break
            elif choice == 5:
                self.exit_message()
                exit()