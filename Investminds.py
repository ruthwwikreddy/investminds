import os
import json
import hashlib
from datetime import datetime
import logging


logging.basicConfig(filename='investments.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATA_DIR = "/Users/RuthwikReddy/Library/CloudStorage/OneDrive-Personal/Ruthwik Reddy/Projects/InvestMinds/DataUsers"

class User:
    def __init__(self, username, age, password, contact_info=None, investment_goals=None, risk_tolerance=None, investment_experience=None):
        self.username = username
        self.age = age
        self.password = self._hash_password(password)
        self.balance = 10000.0  # Starting funds
        self.investments = []
        self.investment_options = []
        self.contact_info = contact_info
        self.investment_goals = investment_goals
        self.risk_tolerance = risk_tolerance
        self.investment_experience = investment_experience

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def to_dict(self):
        return {
            "username": self.username,
            "age": self.age,
            "password": self.password,
            "balance": self.balance,
            "investments": self.investments,
            "investment_options": self.investment_options,
            "contact_info": self.contact_info,
            "investment_goals": self.investment_goals,
            "risk_tolerance": self.risk_tolerance,
            "investment_experience": self.investment_experience
        }

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_investments(user):
    if not user.investments:
        print("No investments yet.")
    else:
        print("Your Investments:")
        for index, investment in enumerate(user.investments, start=1):
            print(f"{index}. {investment['investment_option']['name']}: ${investment['amount']}, Return: ${investment['return_value']:.2f}, Date: {investment['date']}")
            print(f"   Notes: {investment['notes']}")

def invest(user, investment_options):
    clear_screen()
    print("You have the following investment options:")
    for i, option in enumerate(investment_options, start=1):
        print(f"{i}. {option['name']} ({option['option_type'].capitalize()}) - "
              f"Rate of Return: {option['rate_of_return'] * 100}%")

    while True:
        try:
            choice = int(input("Choose an investment option (number): "))
            if choice < 1 or choice > len(investment_options):
                raise ValueError("Invalid choice")
            break
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and", len(investment_options))

    option = investment_options[choice - 1]
    max_investment = min(option['max_investment'], user.balance)
    min_investment = option['min_investment']
    
    print(f"\nSelected Option: {option['name']} ({option['option_type'].capitalize()})")
    print(f"Minimum Investment: ${min_investment:.2f}")
    print(f"Maximum Investment: ${max_investment:.2f}")
    
    while True:
        try:
            amount = float(input(f"Enter the amount you want to invest (between ${min_investment:.2f} and ${max_investment:.2f}): "))
            if amount < min_investment or amount > max_investment:
                raise ValueError(f"Invalid amount. Please enter an amount between ${min_investment:.2f} and ${max_investment:.2f}")
            if amount > user.balance:
                raise ValueError("Insufficient funds. Please enter an amount within your available balance.")
            break
        except ValueError as ve:
            print(ve)

    # Additional feature: Confirm investment
    confirm = input(f"\nConfirm investment of ${amount:.2f} in {option['name']}? (yes/no): ").lower()
    if confirm != 'yes':
        print("Investment cancelled.")
        return

    try:
        if option['option_type'] == "fixed":
            return_value = option['rate_of_return'] * amount
        else:
            return_value = amount * (1 + option['rate_of_return'])
        
        investment = {
            "user": user.username,
            "investment_option": option,
            "amount": amount,
            "return_value": return_value,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "notes": input("Enter any notes for this investment (optional): ")
        }
        user.investments.append(investment)
        user.balance -= amount

        # Log investment activity
        logging.info(f"Investment: User '{user.username}' invested ${amount:.2f} in '{option['name']}'.")

        print(f"\nInvestment of ${amount:.2f} in {option['name']} has been added to your account.")
        display_investments(user)
        print(f"Remaining balance: ${user.balance:.2f}")
    except Exception as e:
        print("An error occurred while processing your investment. Please try again later.")
        logging.error(f"Investment Error: {e}")

def educational_resources():
    clear_screen()
    print("Educational Resources:")
    
    topics = {
        1: {
            "title": "Basics of Investing",
            "content": "Investing involves committing money to an asset with the expectation of earning a positive return. "
                       "It's a way to grow wealth over time by making your money work for you. "
                       "Common investment vehicles include stocks, bonds, mutual funds, and real estate."
        },
        2: {
            "title": "Understanding Interest Rates",
            "content": "Interest rates represent the cost of borrowing money or the return on investment. "
                       "They have a significant impact on various financial activities, including saving, borrowing, and investing. "
                       "Higher interest rates typically mean higher returns but may also result in higher borrowing costs."
        },
        3: {
            "title": "Equity and Shares Explained",
            "content": "Equity refers to ownership in a company, represented by shares of stock. "
                       "When you buy shares, you become a partial owner of the company and may benefit from its growth and profitability. "
                       "Shares can provide capital appreciation and income through dividends."
        },
        4: {
            "title": "Risk Management in Investments",
            "content": "Risk management involves identifying, assessing, and mitigating potential risks in your investment portfolio. "
                       "Diversification, asset allocation, and hedging are common strategies to manage risk. "
                       "Understanding your risk tolerance and investment goals is crucial for effective risk management."
        },
        5: {
            "title": "How to Diversify Your Portfolio",
            "content": "Diversification involves spreading your investments across different asset classes, industries, and geographic regions. "
                       "It helps reduce the impact of individual asset volatility on your overall portfolio. "
                       "Diversifying can improve risk-adjusted returns and protect against significant losses."
        },
        6: {
            "title": "Long-term vs Short-term Investments",
            "content": "Long-term investments are held for several years and are expected to provide gradual but steady returns. "
                       "Short-term investments are held for a shorter period and can be more volatile but may offer quicker returns. "
                       "Choosing between them depends on your financial goals and risk tolerance."
        },
        7: {
            "title": "The Importance of Liquidity",
            "content": "Liquidity refers to how easily you can convert your investments into cash without significant loss in value. "
                       "High liquidity is important for meeting short-term financial needs and providing flexibility in your investment strategy."
        },
        8: {
            "title": "Reading Financial Statements",
            "content": "Financial statements like balance sheets, income statements, and cash flow statements provide crucial information about a company's financial health and performance. "
                       "Understanding these documents can help you make informed investment decisions."
        },
        9: {
            "title": "Introduction to Micro-Investing",
            "content": "Micro-investing involves making small, automated investments in stocks, ETFs, or other financial assets. "
                       "It allows individuals to invest small amounts of money regularly, even with limited funds. Apps like Acorns and Stash facilitate micro-investing."
        },
        10: {
            "title": "Gamification in Investing",
            "content": "Gamification involves incorporating game-like elements, such as rewards, badges, or leaderboards, into the investment process to make it more engaging and enjoyable. "
                       "This can help motivate new investors to learn and participate more actively in the market."
        },
        11: {
            "title": "Building an Investment Community",
            "content": "Building a community of like-minded investors can provide support, insights, and opportunities for collaboration. "
                       "Online forums, social media groups, or investment clubs are common ways to connect with others who share your investment interests."
        },
        12: {
            "title": "Mobile Investing Tips",
            "content": "With the increasing popularity of mobile devices, it's essential to know how to invest effectively using mobile apps. "
                       "Tips include conducting thorough research, monitoring investments regularly, and utilizing security features to protect your data and funds."
        },
        13: {
            "title": "Customer Support Guide",
            "content": "Having access to reliable customer support is crucial for investors. This guide covers common issues, support channels (such as live chat, email, or phone), and best practices for seeking assistance. "
                       "Knowing how to get help quickly can save time and prevent potential financial losses."
        }
    }

    for index, topic in topics.items():
        print(f"{index}. {topic['title']}")

    try:
        choice = int(input("Choose a topic to learn about (1-13): "))
        if choice < 1 or choice > len(topics):
            raise ValueError("Invalid choice")
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 13.")
        input("Press Enter to continue...")
        return

    selected_topic = topics[choice]
    print(f"\n{selected_topic['title']}:")
    print(selected_topic['content'])

    input("\nPress Enter to return to the main menu...")

def list_company(user):
    clear_screen()
    print("List a Company for Investment\n")

    name = input("Enter the company name: ").strip()
    if not name:
        print("Company name cannot be empty.")
        logging.error("Empty company name entered.")
        return

    option_type = input("Enter the investment type (interest, fixed, equity): ").lower()
    if option_type not in ["interest", "fixed", "equity"]:
        print("Invalid investment type")
        logging.error(f"Invalid investment type: {option_type}")
        return

    rate_of_return = None
    if option_type == "interest":
        rate_of_return = get_float_input("Enter the annual interest rate (as a decimal, e.g., 0.05 for 5%): ")
    elif option_type == "fixed":
        rate_of_return = get_float_input("Enter the fixed return amount: ")
    elif option_type == "equity":
        rate_of_return = get_float_input("Enter the expected equity return (as a decimal, e.g., 0.10 for 10%): ")

    if rate_of_return is None:
        return

    min_investment = get_float_input("Enter the minimum investment amount: ")
    max_investment = get_float_input("Enter the maximum investment amount: ")

    new_option = {
        "name": name,
        "option_type": option_type,
        "rate_of_return": rate_of_return,
        "min_investment": min_investment,
        "max_investment": max_investment
    }
    user.investment_options.append(new_option)
    print(f"{name} has been listed as an investment option.")
    logging.info(f"{name} listed as an investment option by {user.username}.")

def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
                logging.error("Negative value entered.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            logging.error("Invalid input for rate of return.")


def save_data(users):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    with open(os.path.join(DATA_DIR, "users.json"), "w") as f:
        json.dump(users, f)


def load_data():
    if os.path.exists(os.path.join(DATA_DIR, "users.json")):
        with open(os.path.join(DATA_DIR, "users.json"), "r") as f:
            return json.load(f)
    return {}


def login_or_signup(users):
    print("Welcome to InvestMinds!")
    print("1. Login")
    print("2. Sign Up")

    choice = input("Choose an option (1-2): ")

    if choice == "1":
        return login(users)
    elif choice == "2":
        return signup(users)
    else:
        print("Invalid choice. Please try again.")
        return login_or_signup(users)
    
def login(users):
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    if username in users and users[username]["password"] == hashlib.sha256(password.encode()).hexdigest():
        user_data = users[username]
        user = User(user_data["username"], user_data["age"], password, user_data.get("contact_info"), user_data.get("investment_goals"), user_data.get("risk_tolerance"), user_data.get("investment_experience"))
        user.balance = user_data["balance"]
        user.investments = user_data["investments"]    
        user.investment_options = user_data["investment_options"]
        return user
    else:
        print("Invalid username or password.")
        logging.error("Invalid username or password.")
        return login(users)
        
    return login_or_signup(users)
        
def signup(users):
    username = input("Enter a username: ")
    if username in users:
        print("Username already exists. Please choose another.")
        logging.error("Username already exists.")
        return signup(users)

    try:
        age = int(input("Enter your age: "))
        if age < 15:
            print("You must be at least 15 years old to sign up.")
            logging.error("User must be at least 15 years old to sign up.")
            return signup(users)
    except ValueError:
        print("Invalid input for age. Please enter a number.")
        logging.error("Invalid input for age.")
        return signup(users)

    password = input("Create a password: ")
    contact_info = input("Enter your contact information: ")
    investment_goals = input("Enter your investment goals: ")
    risk_tolerance = input("Enter your risk tolerance: ")
    investment_experience = input("Enter your investment experience: ")
    
    user = User(username, age, password, contact_info, investment_goals, risk_tolerance, investment_experience)
    users[username] = user.to_dict()
    save_data(users)
    print("Account created successfully!")
    logging.info("Account created successfully!")
    return user

def main_menu(user, users):
    while True:
        clear_screen()
        print(f"Welcome, {user.username}! Age: {user.age}")
        print(f"Current balance: ${user.balance:.2f}\n")

        print("Main Menu:")
        print("1. Invest")
        print("2. Educational Resources")
        print("3. List a Company for Investment")
        print("4. View Investments")
        print("5. Exit")

        try:
            choice = int(input("Choose an option (1-5): "))
            if choice < 1 or choice > 5:
                print("Invalid choice. Please enter a number between 1 and 5.")
                input("Press Enter to continue...")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            input("Press Enter to continue...")
            continue

        if choice == 1:
            invest(user, user.investment_options)
        elif choice == 2:
            educational_resources()
            input("Press Enter to continue...")
        elif choice == 3:
            list_company(user)
            input("Press Enter to continue...")
        elif choice == 4:
            display_investments(user)
            input("Press Enter to continue...")
        elif choice == 5:
            save_data(users)
            print("Exiting the application. Goodbye!")
            break

if __name__ == "__main__":
    users = load_data()
    if not users:
        users = {}
    user = login_or_signup(users)
    main_menu(user, users)
