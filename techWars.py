import random
import os
from colorama import init, Fore, Style

init(autoreset=True)  # Initialize colorama

# Game data
items = [
    {"name": "Zero-Day Exploit", "base_price": 1500, "var": 0.5},
    {"name": "Ransomware Kit", "base_price": 800, "var": 0.4},
    {"name": "Phishing Template", "base_price": 200, "var": 0.3},
    {"name": "DDoS Bot", "base_price": 500, "var": 0.35},
    {"name": "Keylogger", "base_price": 100, "var": 0.25},
    {"name": "SQL Injection Tool", "base_price": 300, "var": 0.3},
    {"name": "xAI Backdoor", "base_price": 2000, "var": 0.6},
    {"name": "Crypto Wallet Cracker", "base_price": 1200, "var": 0.45}
]

marketplaces = [
    {"name": "Dark Web Forum"},
    {"name": "Zero-Day Bazaar"},
    {"name": "Phishing Nets"},
    {"name": "Exploit Underground"},
    {"name": "Botnet Hive"}
]

upgrades = [
    {"name": "Fast Travel", "cost": 1000, "description": "Travel without advancing the day", "effect": {"type": "fastTravel", "value": True}},
    {"name": "Extra Bag Space", "cost": 800, "description": "Increase carrying capacity by 5", "effect": {"type": "carryingCapacity", "value": 5}},
    {"name": "Cool Down", "cost": 500, "description": "Reduce heat by 3%", "effect": {"type": "reduceHeat", "value": 3}}
]

price_cache = {}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_prices(player):
    day = player['day']
    loc_name = player['location']['name']
    city_idx = next(i for i, m in enumerate(marketplaces) if m['name'] == loc_name)
    key = (day, city_idx)
    if key not in price_cache:
        random.seed(day + city_idx * 31)
        prices_list = []
        for item in items:
            base = item['base_price']
            variation = base * item['var'] * random.uniform(-1, 1)
            city_mult = 1 + (city_idx - 2) * 0.1
            inflation = 1 + (day / 300)
            price = max(10, int((base + variation) * city_mult * inflation))
            prices_list.append(price)
        price_cache[key] = dict(zip([i['name'] for i in items], prices_list))
    return price_cache[key].copy()

def perform_buy(player, item_name, quantity, prices):
    if item_name not in prices:
        return False, 'Invalid item'
    price = prices[item_name]
    cost = quantity * price
    if player['cash'] < cost:
        return False, 'Not enough cash!'
    current_load = sum(player['inventory'].values())
    if current_load + quantity > player['carryingCapacity']:
        return False, f'Exceeds carrying capacity ({player["carryingCapacity"]})!'
    player['inventory'][item_name] = player['inventory'].get(item_name, 0) + quantity
    player['cash'] -= cost
    player['heat'] += quantity * 2  # Scale for 0-100%
    player['heat'] = min(100, player['heat'])
    return True, f'Bought {quantity} x {item_name} for ${cost:,}'

def perform_sell(player, item_name, quantity, prices):
    if item_name not in player['inventory'] or player['inventory'][item_name] < quantity:
        return False, 'Not enough in inventory!'
    price = prices[item_name]
    revenue = quantity * price
    player['inventory'][item_name] -= quantity
    if player['inventory'][item_name] == 0:
        del player['inventory'][item_name]
    player['cash'] += revenue
    player['heat'] = max(0, player['heat'] - quantity * 1)
    return True, f'Sold {quantity} x {item_name} for ${revenue:,}'

def apply_upgrade_effect(player, effect):
    typ = effect['type']
    val = effect['value']
    if typ == 'fastTravel':
        player['fastTravel'] = True
    elif typ == 'carryingCapacity':
        player['carryingCapacity'] += val
    elif typ == 'reduceHeat':
        player['heat'] = max(0, player['heat'] - val)

def check_events(player):
    messages = []
    if random.random() < 0.2:
        r = random.random()
        if r < 0.25:
            messages.append('Market crash! All prices drop 20% today.')
        elif r < 0.5:
            messages.append('Black market boom! Sell prices up 30%!')
        elif r < 0.75:
            player['heat'] = min(100, player['heat'] + 20)
            messages.append('Cops on your tail! Heat +20%')
        else:
            player['cash'] += 200
            messages.append('Found a loose xAI token! +$200')
    # Check for bust
    if player['heat'] >= 100 or random.random() < (player['heat'] / 1000):
        if player['inventory']:
            num_types = random.randint(1, min(3, len(player['inventory'])))
            to_lose = random.sample(list(player['inventory'].keys()), num_types)
            for key in to_lose:
                del player['inventory'][key]
            messages.append(f'BUSTED! Lost {len(to_lose)} random item types from inventory.')
            player['heat'] = 0
            player['cash'] = max(0, player['cash'] - 500)  # Fine
    return messages

def check_win_lose(player):
    if player['cash'] >= player['debt']:
        return {'over': True, 'win': True, 'message': 'CONGRATS! Paid off debt. You win TechWars!\nYou\'ve built an underground hacker empire. What\'s next? Legit pentest firm?'}
    if player['day'] > player['maxDays']:
        return {'over': True, 'win': False, 'message': 'Game Over! You couldn\'t pay the debt. Back to square one in the cyber underworld.'}
    return {'over': False}

def check_day_events(player):
    messages = check_events(player)
    for msg in messages:
        print(Fore.YELLOW + f'>>> {msg} <<<')
    result = check_win_lose(player)
    if result['over']:
        print(Fore.GREEN + result['message'] if result['win'] else Fore.RED + result['message'])
        return True
    return False

def display_status(player):
    clear_screen()
    print(Fore.WHITE + f"[SYSTEM] DAY {player['day']}/{player['maxDays']}")
    print(Fore.RED + f"[LOCATION] {player['location']['name']}")
    print(Fore.GREEN + f"[CASH] ${player['cash']:,.0f}")
    print(Fore.RED + f"[DEBT] ${player['debt']:,.0f}")
    print(Fore.YELLOW + f"[HEAT] {player['heat']:.0f}%")
    print(Fore.WHITE + '[INVENTORY]')
    if len(player['inventory']) == 0:
        print(' Empty')
    else:
        for item, qty in player['inventory'].items():
            print(f" {item}: {qty}")
    print(Fore.WHITE + '-------------------')

def display_menu():
    print(Fore.WHITE + '1. BUY ITEMS')
    print(Fore.WHITE + '2. SELL ITEMS')
    print(Fore.WHITE + '3. MOVE MARKET')
    print(Fore.WHITE + '4. UPGRADES')
    print(Fore.WHITE + '5. END DAY')
    print(Fore.WHITE + '0. BACK (main menu only)')

def buy_items(player):
    prices = get_current_prices(player)
    print(Fore.WHITE + '[AVAILABLE ITEMS]')
    for i, item in enumerate(items):
        print(f"{i+1}. {item['name']}: ${prices[item['name']]:,}")
    choice = input(Fore.CYAN + '> BUY (number or 0 to cancel): ').strip()
    if choice == '0':
        return False
    try:
        item_idx = int(choice) - 1
        if not (0 <= item_idx < len(items)):
            raise ValueError
        item_name = items[item_idx]['name']
        qty_str = input(Fore.CYAN + '> QUANTITY: ').strip()
        quantity = int(qty_str)
        if quantity <= 0:
            raise ValueError
        success, message = perform_buy(player, item_name, quantity, prices)
        color = Fore.GREEN if success else Fore.RED
        print(color + f'>>> {message} <<<')
    except ValueError:
        print(Fore.RED + 'Invalid selection')
    input('\nPress Enter to continue...')
    return False

def sell_items(player):
    if len(player['inventory']) == 0:
        print(Fore.RED + 'No items to sell')
        input('\nPress Enter to continue...')
        return False
    prices = get_current_prices(player)
    print(Fore.WHITE + '[INVENTORY]')
    inv_entries = list(player['inventory'].items())
    for i, (item, qty) in enumerate(inv_entries):
        sell_price = prices[item]
        print(f"{i+1}. {item}: {qty} (Sell Price: ${sell_price:,})")
    choice = input(Fore.CYAN + '> SELL (number or 0 to cancel): ').strip()
    if choice == '0':
        return False
    try:
        item_idx = int(choice) - 1
        if not (0 <= item_idx < len(inv_entries)):
            raise ValueError
        item_name, max_qty = inv_entries[item_idx]
        qty_str = input(Fore.CYAN + '> QUANTITY: ').strip()
        quantity = int(qty_str)
        if quantity <= 0 or quantity > max_qty:
            raise ValueError
        success, message = perform_sell(player, item_name, quantity, prices)
        color = Fore.GREEN if success else Fore.RED
        print(color + f'>>> {message} <<<')
    except ValueError:
        print(Fore.RED + 'Invalid selection')
    input('\nPress Enter to continue...')
    return False

def move_market(player):
    print(Fore.WHITE + '[MARKETPLACES]')
    for i, market in enumerate(marketplaces):
        print(f"{i+1}. {market['name']}")
    choice = input(Fore.CYAN + '> MOVE (number or 0 to cancel): ').strip()
    if choice == '0':
        return False
    try:
        market_idx = int(choice) - 1
        if not (0 <= market_idx < len(marketplaces)):
            raise ValueError
        new_location = marketplaces[market_idx]
        if new_location['name'] == player['location']['name']:
            print(Fore.RED + 'Already at this market')
            input('\nPress Enter to continue...')
            return False
        player['location'] = new_location
        if not player['fastTravel']:
            player['day'] += 1
        print(Fore.GREEN + f'Moved to {player["location"]["name"]}')
        return check_day_events(player)
    except ValueError:
        print(Fore.RED + 'Invalid selection')
        input('\nPress Enter to continue...')
        return False

def upgrades_menu(player):
    print(Fore.WHITE + '[UPGRADES]')
    available_upgrades = [u for u in upgrades if u['name'] not in player['upgrades']]
    if len(available_upgrades) == 0:
        print(Fore.YELLOW + 'No more upgrades available.')
        input('\nPress Enter to continue...')
        return False
    for i, u in enumerate(available_upgrades):
        print(f"{i+1}. {u['name']}: ${u['cost']:,} - {u['description']}")
    choice = input(Fore.CYAN + '> UPGRADE (number or 0 to cancel): ').strip()
    if choice == '0':
        return False
    try:
        upgrade_idx = int(choice) - 1
        if not (0 <= upgrade_idx < len(available_upgrades)):
            raise ValueError
        upgrade = available_upgrades[upgrade_idx]
        if player['cash'] < upgrade['cost']:
            print(Fore.RED + 'Insufficient funds')
            input('\nPress Enter to continue...')
            return False
        player['cash'] -= upgrade['cost']
        player['upgrades'].append(upgrade['name'])
        apply_upgrade_effect(player, upgrade['effect'])
        print(Fore.GREEN + f'Purchased {upgrade["name"]}')
        input('\nPress Enter to continue...')
        return False
    except ValueError:
        print(Fore.RED + 'Invalid selection')
        input('\nPress Enter to continue...')
        return False

def end_day(player):
    player['day'] += 1
    return check_day_events(player)

def handle_command(player, choice):
    if choice == '1':
        return buy_items(player)
    elif choice == '2':
        return sell_items(player)
    elif choice == '3':
        return move_market(player)
    elif choice == '4':
        return upgrades_menu(player)
    elif choice == '5':
        return end_day(player)
    else:
        print(Fore.RED + 'Invalid command')
        input('\nPress Enter to continue...')
        return False

def game_loop(player):
    display_status(player)
    display_menu()
    choice = input(Fore.CYAN + '> COMMAND: ').strip()
    return handle_command(player, choice)

if __name__ == "__main__":
    print(Fore.RED + '[Tech Wars]')
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
        'upgrades': []
    }
    while True:
        over = game_loop(player)
        if over:
            break
