import random
import colorama
from colorama import Fore, Style

# Initialize colorama for colored console output
colorama.init()

# Define items with base prices and risk levels
items = [
    {'name': 'Stolen Credit Cards', 'basePrice': {'min': 10, 'max': 50}, 'risk': 'high'},
    {'name': 'Zero-Day Exploits', 'basePrice': {'min': 5000, 'max': 20000}, 'risk': 'very high'},
    {'name': 'Hacked Social Media Accounts', 'basePrice': {'min': 5, 'max': 20}, 'risk': 'low'},
    {'name': 'Bitcurrency Wallets', 'basePrice': {'min': 1000, 'max': 10000}, 'risk': 'medium'},
]

# Define marketplaces with price multipliers and risks
marketplaces = [
    {
        'name': 'Social Media Black Market',
        'priceMultipliers': {
            'Hacked Social Media Accounts': 1.3,
            'Zero-Day Exploits': 0.7
        },
        'risks': {
            'lawEnforcement': 0.02,
            'scam': 0.05
        }
    },
    {
        'name': 'Hacker Forum',
        'priceMultipliers': {
            'Zero-Day Exploits': 1.2,
            'Stolen Credit Cards': 0.8,
            'Bitcurrency Wallets': 1.1
        },
        'risks': {
            'lawEnforcement': 0.1,
            'scam': 0.05
        }
    },
    {
        'name': 'DarkNet Auction House',
        'priceMultipliers': {
            'Zero-Day Exploits': 1.5,
            'Stolen Credit Cards': 0.9,
            'Bitcurrency Wallets': 1.2
        },
        'risks': {
            'lawEnforcement': 0.15,
            'scam': 0.04
        }
    },
    {
        'name': 'Cybercrime Bazaar',
        'priceMultipliers': {},
        'risks': {
            'lawEnforcement': 0.05,
            'scam': 0.05
        }
    },
    {
        'name': 'Malware Emporium',
        'priceMultipliers': {
            'Zero-Day Exploits': 1.1,
            'Hacked Social Media Accounts': 0.8,
            'Stolen Credit Cards': 0.7
        },
        'risks': {
            'lawEnforcement': 0.08,
            'scam': 0.07
        }
    },
    {
        'name': 'Silk Road',
        'priceMultipliers': {
            'Bitcurrency Wallets': 1.4,  # High demand for crypto on Silk Road
            'Stolen Credit Cards': 0.85,  # Slightly discounted due to volume
            'Zero-Day Exploits': 1.3     # Premium for rare exploits
        },
        'risks': {
            'lawEnforcement': 0.20,       # High risk due to historical notoriety
            'scam': 0.06                  # Moderate scam risk
        }
    }
]

# Define upgrades with costs and effects
upgrades = [
    {
        'name': 'Better Encryption',
        'cost': 5000,
        'effect': 'reduceHeat',
        'description': 'Reduces current heat by 20'
    },
    {
        'name': 'Faster Internet',
        'cost': 2000,
        'effect': 'reduceTravelTime',
        'description': 'Enables fast travel (moving doesn\'t take a day)'
    },
    {
        'name': 'Secure Devices',
        'cost': 3000,
        'effect': 'increaseCapacity',
        'description': 'Increases carrying capacity by 10'
    },
]

# Define event effects
def marketplace_shutdown(player):
    """Event: Moves player to a safe marketplace and clears inventory with notification."""
    original_location = player['location']['name']
    player['location'] = marketplaces[0]  # Move to Social Media Black Market
    player['inventory'] = {}
    player['current_prices'] = generate_prices_for_marketplace(player['location'])
    return f"ALERT: Agent Cyberstrike raided {original_location}! Your inventory has been confiscated, and you've been forced to flee to {player['location']['name']}."

def law_enforcement_trace(player):
    """Event: Increases heat due to Agent Cyberstrike's surveillance."""
    player['heat'] += 20
    return "WARNING: Agent Cyberstrike has traced your activity! Heat increased by 20%."

# Define events
events = [
    {'name': 'Marketplace Shutdown', 'probability': 0.05, 'effect': marketplace_shutdown},
    {'name': 'Law Enforcement Trace', 'probability': 0.02, 'effect': law_enforcement_trace},
]

# Helper functions
def generate_prices_for_marketplace(marketplace):
    """Generate randomized prices for items in a marketplace."""
    prices = {}
    for item in items:
        base = item['basePrice']
        multiplier = marketplace['priceMultipliers'].get(item['name'], 1)
        price = int((random.random() * (base['max'] - base['min']) + base['min']) * multiplier)
        prices[item['name']] = price
    return prices

def perform_buy(player, item_name, quantity):
    """Handle buying items, updating cash, inventory, and heat."""
    if item_name not in player['current_prices']:
        return {'success': False, 'message': 'Item not found'}
    price = player['current_prices'][item_name]
    total_cost = price * quantity
    current_items = sum(player['inventory'].values())
    if player['cash'] < total_cost:
        return {'success': False, 'message': 'Insufficient funds'}
    elif current_items + quantity > player['carryingCapacity']:
        return {'success': False, 'message': 'Carrying capacity exceeded'}
    else:
        player['cash'] -= total_cost
        player['inventory'][item_name] = player['inventory'].get(item_name, 0) + quantity
        item = next(i for i in items if i['name'] == item_name)
        heat_increase = {'very high': 10, 'high': 5, 'medium': 3, 'low': 1}.get(item['risk'], 1)
        player['heat'] += heat_increase
        return {'success': True, 'message': f"Acquired {quantity} {item_name} for ${total_cost}"}

def perform_sell(player, item_name, quantity):
    """Handle selling items, updating cash, inventory, and heat."""
    if item_name not in player['inventory'] or player['inventory'][item_name] < quantity:
        return {'success': False, 'message': 'Not enough items to sell'}
    price = player['current_prices'][item_name]
    total_earned = price * quantity
    player['cash'] += total_earned
    player['inventory'][item_name] -= quantity
    if player['inventory'][item_name] == 0:
        del player['inventory'][item_name]
    player['heat'] = max(0, player['heat'] - 2)
    return {'success': True, 'message': f"Sold {quantity} {item_name} for ${total_earned}"}

def apply_upgrade_effect(player, effect):
    """Apply the effect of an upgrade to the player."""
    if effect == 'reduceHeat':
        player['heat'] = max(0, player['heat'] - 20)
    elif effect == 'reduceTravelTime':
        player['fastTravel'] = True
    elif effect == 'increaseCapacity':
        player['carryingCapacity'] += 10

def check_win_lose(player):
    """Check if the game is over and if the player won or lost."""
    if player['heat'] >= 100:
        return {'over': True, 'win': False, 'message': 'Heat reached 100%. Agent Cyberstrike has arrested you!'}
    if player['day'] > player['maxDays']:
        if player['cash'] >= player['debt']:
            return {'over': True, 'win': True, 'message': 'Debt paid off after 30 days! You win!'}
        else:
            return {'over': True, 'win': False, 'message': "Time's up! Debt unpaid. You lose!"}
    return {'over': False}

# UI functions
def display_status(player):
    """Display the player's current status."""
    print(Fore.WHITE + f"[SYSTEM] DAY {player['day']}/{player['maxDays']}")
    print(Fore.RED + f"[LOCATION] {player['location']['name']}")
    print(Fore.GREEN + f"[CASH] ${player['cash']}")
    print(Fore.RED + f"[DEBT] ${player['debt']}")
    print(Fore.YELLOW + f"[HEAT] {player['heat']}%")
    print(Fore.WHITE + "[INVENTORY]")
    if not player['inventory']:
        print("  Empty")
    else:
        for item, qty in player['inventory'].items():
            print(f"  {item}: {qty}")
    print(Fore.WHITE + "-------------------")

def display_menu():
    """Display the main menu options."""
    print(Fore.WHITE + "1. BUY ITEMS")
    print(Fore.WHITE + "2. SELL ITEMS")
    print(Fore.WHITE + "3. MOVE MARKET")
    print(Fore.WHITE + "4. UPGRADES")
    print(Fore.WHITE + "5. END DAY")
    print(Fore.WHITE + "0. BACK (main menu only)")

# Action functions
def buy_items(player):
    """Handle the buy items menu."""
    print(Fore.WHITE + "[AVAILABLE ITEMS]")
    for i, item in enumerate(items, 1):
        price = player['current_prices'][item['name']]
        print(f"{i}. {item['name']}: ${price}")
    choice = input(Fore.CYAN + "> BUY (number or 0 to cancel): " + Style.RESET_ALL).strip()
    if choice == '0':
        return
    try:
        item_index = int(choice) - 1
        if 0 <= item_index < len(items):
            item_name = items[item_index]['name']
            qty = input(Fore.CYAN + "> QUANTITY: " + Style.RESET_ALL).strip()
            try:
                quantity = int(qty)
                if quantity > 0:
                    result = perform_buy(player, item_name, quantity)
                    print(Fore.GREEN if result['success'] else Fore.RED + f">>> {result['message']} <<<")
                else:
                    print(Fore.RED + "Invalid quantity")
            except ValueError:
                print(Fore.RED + "Invalid quantity")
        else:
            print(Fore.RED + "Invalid selection")
    except ValueError:
        print(Fore.RED + "Invalid selection")

def sell_items(player):
    """Handle the sell items menu."""
    if not player['inventory']:
        print(Fore.RED + "No items to sell")
        return
    print(Fore.WHITE + "[INVENTORY]")
    inventory_items = list(player['inventory'].keys())
    for i, item_name in enumerate(inventory_items, 1):
        qty = player['inventory'][item_name]
        price = player['current_prices'][item_name]
        print(f"{i}. {item_name}: {qty} (Sell Price: ${price})")
    choice = input(Fore.CYAN + "> SELL (number or 0 to cancel): " + Style.RESET_ALL).strip()
    if choice == '0':
        return
    try:
        item_index = int(choice) - 1
        if 0 <= item_index < len(inventory_items):
            item_name = inventory_items[item_index]
            qty = input(Fore.CYAN + "> QUANTITY: " + Style.RESET_ALL).strip()
            try:
                quantity = int(qty)
                if quantity > 0:
                    result = perform_sell(player, item_name, quantity)
                    print(Fore.GREEN if result['success'] else Fore.RED + f">>> {result['message']} <<<")
                else:
                    print(Fore.RED + "Invalid quantity")
            except ValueError:
                print(Fore.RED + "Invalid quantity")
        else:
            print(Fore.RED + "Invalid selection")
    except ValueError:
        print(Fore.RED + "Invalid selection")

def move_market(player):
    """Handle moving to a different marketplace."""
    print(Fore.WHITE + "[MARKETPLACES]")
    for i, m in enumerate(marketplaces, 1):
        print(f"{i}. {m['name']}")
    choice = input(Fore.CYAN + "> MOVE (number or 0 to cancel): " + Style.RESET_ALL).strip()
    if choice == '0':
        return
    try:
        market_index = int(choice) - 1
        if 0 <= market_index < len(marketplaces):
            new_location = marketplaces[market_index]
            if new_location == player['location']:
                print(Fore.RED + "Already at this market")
            else:
                player['location'] = new_location
                player['current_prices'] = generate_prices_for_marketplace(new_location)
                if not player['fastTravel']:
                    player['day'] += 1
                print(Fore.GREEN + f"Moved to {new_location['name']}")
                check_day_events(player)
        else:
            print(Fore.RED + "Invalid selection")
    except ValueError:
        print(Fore.RED + "Invalid selection")

def upgrades_menu(player):
    """Handle the upgrades menu."""
    print(Fore.WHITE + "[UPGRADES]")
    available_upgrades = [u for u in upgrades if u['name'] not in player['upgrades']]
    for i, u in enumerate(available_upgrades, 1):
        print(f"{i}. {u['name']}: ${u['cost']} - {u['description']}")
    choice = input(Fore.CYAN + "> UPGRADE (number or 0 to cancel): " + Style.RESET_ALL).strip()
    if choice == '0':
        return
    try:
        upgrade_index = int(choice) - 1
        if 0 <= upgrade_index < len(available_upgrades):
            upgrade = available_upgrades[upgrade_index]
            if player['cash'] >= upgrade['cost']:
                player['cash'] -= upgrade['cost']
                player['upgrades'].append(upgrade['name'])
                apply_upgrade_effect(player, upgrade['effect'])
                print(Fore.GREEN + f"Purchased {upgrade['name']}")
            else:
                print(Fore.RED + "Insufficient funds")
        else:
            print(Fore.RED + "Invalid selection")
    except ValueError:
        print(Fore.RED + "Invalid selection")

def end_day(player):
    """End the current day and check for events."""
    player['day'] += 1
    check_day_events(player)

def check_day_events(player):
    """Check for and apply random events."""
    messages = []
    for event in events:
        if random.random() < event['probability']:
            message = event['effect'](player)
            if message:
                messages.append(message)
    for msg in messages:
        print(Fore.YELLOW + f">>> {msg} <<<")

# Game loop
def game_loop(player):
    """Main game loop."""
    while True:
        print('\033[H\033[J', end='')  # Clear console using ANSI escape code
        display_status(player)
        display_menu()
        choice = input(Fore.CYAN + "> COMMAND: " + Style.RESET_ALL).strip()
        if choice == '1':
            buy_items(player)
        elif choice == '2':
            sell_items(player)
        elif choice == '3':
            move_market(player)
        elif choice == '4':
            upgrades_menu(player)
        elif choice == '5':
            end_day(player)
        elif choice == '0':
            break  # Return to main menu or exit submenu
        else:
            print(Fore.RED + "Invalid command")
        result = check_win_lose(player)
        if result['over']:
            if result['win']:
                print(Fore.GREEN + result['message'])
            else:
                print(Fore.RED + result['message'])
            break

# Main execution
if __name__ == "__main__":
    # Initialize player state
    player = {
        'cash': 2000,
        'debt': 5000,
        'heat': 0,
        'inventory': {},
        'day': 1,
        'maxDays': 30,
        'location': marketplaces[0],
        'carryingCapacity': 10,
        'fastTravel': False,
        'upgrades': [],
        'current_prices': generate_prices_for_marketplace(marketplaces[0]),
    }
    game_loop(player)
