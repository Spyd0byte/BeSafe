#!/usr/bin/env python3
import requests
import time
import sys
import os
import json
from concurrent.futures import ThreadPoolExecutor
import random
import base64
from typing import List, Dict, Optional

class EmailBreachChecker:
    def __init__(self):
        self.api_url = "https://haveibeenpwned.com/api/v3"
        self.api_key = ""  # You need to get your own API key from haveibeenpwned.com
        self.headers = {
            "User-Agent": "EmailBreachChecker-Terminal",
            "hibp-api-key": self.api_key
        }
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def glitchy_banner(self):
        banner = """                             
                      _-.                       .-_
                   _..-'(         \   /         )`-.._
                ./'. '||\\.       (\_/)       .//||` .`\.
             ./'.|'.'||||\\|..    )`^'(    ..|//||||`.`|.`\.
          ./'..|'.|| |||||\```````     '''''''/||||| ||.`|..`\.
        ./'.||'.|||| ||||||||||||.     .|||||||||||| ||||.`||.`\.
       /'|||'.|||||| ||||||||||||{     }|||||||||||| ||||||.`|||`\
      '.|||'.||||||| ||||||||||||{     }|||||||||||| |||||||.`|||.`
     '.||| ||||||||| |/'   ``\||/`     '\||/''   `\| ||||||||| |||.`
     |/' \./'     `\./          |/\   /\|          \./'     `\./ `\|
     V    V         V          }' `\ /' `{          V         V    V
     `    `         `               V               '         '    '

        """
        
        # Create glitch effect
        glitch_chars = ["█", "▓", "▒", "░", "╬", "╩", "╦", "╣", "╠", "╗", "╝", "╚", "╔", "═", "║"]
        
        for _ in range(5):  # Number of glitch iterations
            self.clear_screen()
            glitched_banner = ""
            for line in banner.split('\n'):
                glitched_line = ""
                for char in line:
                    if random.random() < 0.1:  # 10% chance to glitch a character
                        glitched_line += random.choice(glitch_chars)
                    else:
                        glitched_line += char
                glitched_banner += glitched_line + "\n"
            
            print(glitched_banner)
            time.sleep(0.1)
        
        # Final clean banner
        self.clear_screen()
        print(banner)
        time.sleep(0.5)
    
    def decode_animation(self, text: str):
        """Display a decoding animation for text"""
        decoded_chars = []
        for i in range(len(text) + 1):
            sys.stdout.write('\r' + ''.join(decoded_chars))
            
            # Add random characters for the decoding effect
            for j in range(len(text) - i):
                sys.stdout.write(chr(random.randint(33, 126)))
            
            sys.stdout.flush()
            
            if i < len(text):
                decoded_chars.append(text[i])
            
            time.sleep(0.05)
        
        print()
    
    def check_email_breach(self, email: str) -> Optional[List[Dict]]:
        """Check if email has been breached using HaveIBeenPwned API"""
        if not self.api_key:
            print("❌ API key not set. Please get one from https://haveibeenpwned.com/API/Key")
            return None
            
        try:
            url = f"{self.api_url}/breachedaccount/{email}"
            response = requests.get(url, headers=self.headers, params={"truncateResponse": False})
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return []
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return None
    
    def display_results(self, email: str, breaches: List[Dict]):
        """Display the breach results in a structured format"""
        if not breaches:
            print(f"✅ No breaches found for {email}")
            return
            
        print(f"❌ {len(breaches)} breaches found for {email}")
        print("└── Breach Details:")
        
        for i, breach in enumerate(breaches):
            prefix = "├──" if i < len(breaches) - 1 else "└──"
            print(f"    {prefix} {breach['Name']} ({breach['BreachDate']})")
            print(f"    {'│   ' if i < len(breaches) - 1 else '    '} └── Data compromised: {', '.join(breach['DataClasses'])}")
    
    def show_menu(self):
        """Display the Parrot OS-like menu"""
        menu_options = [
            "Check Email Breach",
            "Batch Check Emails",
            "Decode Text",
            "Exit"
        ]
        
        while True:
            self.clear_screen()
            print("""
           ██████╗ ███████╗███████╗ █████╗ ███████╗███████╗
           ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝
           ██████╔╝█████╗  ███████╗███████║█████╗  █████╗  
           ██╔══██╗██╔══╝  ╚════██║██╔══██║██╔══╝  ██╔══╝  
           ██████╔╝███████╗███████║██║  ██║██║     ███████╗
           ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ By SPYDOBYTE [CyberArtist:SHAN]
                                                
            """)
            
            print("Main Menu:")
            for i, option in enumerate(menu_options, 1):
                print(f"  {i}. {option}")
            
            try:
                choice = input("\nSelect an option (1-4): ").strip()
                
                if choice == "1":
                    email = input("Enter email to check: ").strip()
                    print(f"Checking {email}...")
                    self.decode_animation("Analyzing against known breaches...")
                    breaches = self.check_email_breach(email)
                    if breaches is not None:
                        self.display_results(email, breaches)
                    input("\nPress Enter to continue...")
                
                elif choice == "2":
                    emails = input("Enter emails separated by commas: ").split(',')
                    emails = [email.strip() for email in emails if email.strip()]
                    
                    print(f"Checking {len(emails)} emails...")
                    self.decode_animation("Batch analysis in progress...")
                    
                    with ThreadPoolExecutor(max_workers=3) as executor:
                        results = list(executor.map(self.check_email_breach, emails))
                    
                    for email, breaches in zip(emails, results):
                        if breaches is not None:
                            self.display_results(email, breaches)
                            print()
                    input("\nPress Enter to continue...")
                
                elif choice == "3":
                    text = input("Enter text to decode: ").strip()
                    self.decode_animation("Decoding text...")
                    try:
                        decoded = base64.b64decode(text).decode('utf-8')
                        print(f"Decoded text: {decoded}")
                    except:
                        print("Failed to decode text. It may not be base64 encoded.")
                    input("\nPress Enter to continue...")
                
                elif choice == "4":
                    print("Exiting...")
                    break
                
                else:
                    print("Invalid option. Please try again.")
                    time.sleep(1)
            
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                time.sleep(1)
            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(2)

def main():
    checker = EmailBreachChecker()
    checker.glitchy_banner()
    time.sleep(1)
    checker.show_menu()

if __name__ == "__main__":
    main()
