# Tech Wars

Tech Wars is a text-based game where players engage in a simulated underground market, buying and selling tech-related items, managing resources like cash and inventory, and avoiding detection by law enforcement. The game is available in both Node.js and Python implementations, allowing you to choose your preferred environment.

**Objective**: Pay off your $5000 debt within 30 days while managing your cash, inventory, and "heat" level (risk of getting caught).

---

## Table of Contents

1. [Setup](#setup)
   - [Node.js Version](#nodejs-version)
   - [Python Version](#python-version)
2. [Running the Game](#running-the-game)
   - [Node.js](#nodejs)
   - [Python](#python)
3. [Running Unit Tests](#running-unit-tests)
   - [Node.js](#nodejs-1)
   - [Python](#python-1)
4. [Example Gameplay](#example-gameplay)
5. [Troubleshooting](#troubleshooting)
6. [Contributing](#contributing)

---

## Setup

### Node.js Version

1. **Prerequisites**:
   - Ensure you have [Node.js](https://nodejs.org/) installed (version 14.x or higher recommended).

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/techwars.git
   cd techwars
   ```

3. **Install Dependencies**:
   - The game requires `chalk` for colored console output. Install it using:
     ```bash
     npm install
     ```

### Python Version

1. **Prerequisites**:
   - Ensure you have [Python](https://python.org/) installed (version 3.6 or higher).

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/techwars.git
   cd techwars
   ```

3. **Install Dependencies**:
   - The game uses `colorama` for colored console output. Install it using:
     ```bash
     pip install colorama
     ```

---

## Running the Game

### Node.js

Navigate to the project directory and run:
```bash
node techWars.js
```

### Python

Navigate to the project directory and run:
```bash
python tech_wars.py
```

---

## Running Unit Tests

### Node.js

1. **Install Jest**:
   - If not already installed, add Jest as a development dependency:
     ```bash
     npm install --save-dev jest
     ```

2. **Run the Tests**:
   - Execute the following command to run the unit tests:
     ```bash
     npm test
     ```

### Python

1. **Run the Tests**:
   - Python's standard library includes `unittest`, so no additional installation is needed. Run the tests with:
     ```bash
     python -m unittest discover
     ```

---

## Example Gameplay

When you start the game, you'll be presented with a menu of options to buy items, sell items, move to a different market, purchase upgrades, or end the day. Below are examples of typical interactions, including buying and selling items in different locations.

### Example 1: Buying Items in the Social Media Black Market

```
[SYSTEM] DAY 2/30
[LOCATION] Social Media Black Market
[CASH] $2384
[DEBT] $5000
[HEAT] 1%
[INVENTORY]
  Empty
-------------------
1. BUY ITEMS
2. SELL ITEMS
3. MOVE MARKET
4. UPGRADES
5. END DAY
> COMMAND: 1
```

After selecting **"1. BUY ITEMS"**, you'll see a list of available items with their current prices:

```
[AVAILABLE ITEMS]
1. Stolen Credit Cards: $28
2. Zero-Day Exploits: $12795
3. Botnet Access: $1269
4. Fake Social Media Accounts: $11
5. Bitcoin Currency Wallets: $4507
> BUY (number or 'back'): 1
```

- **Choosing an Item**: Enter the number "1" to buy Stolen Credit Cards.
- **Specifying Quantity**: You'll then be prompted to enter the quantity (e.g., "2").
- **Transaction Outcome**: The game will update your cash, inventory, and heat level based on the transaction.

### Example 2: Selling Items in the Hacker Forum

```
[SYSTEM] DAY 3/30
[LOCATION] Hacker Forum
[CASH] $2355
[DEBT] $5000
[HEAT] 6%
[INVENTORY]
  Stolen Credit Cards: 1
-------------------
1. BUY ITEMS
2. SELL ITEMS
3. MOVE MARKET
4. UPGRADES
5. END DAY
> COMMAND: 2
```

After selecting **"2. SELL ITEMS"**, you'll see your current inventory:

```
[INVENTORY]
  Stolen Credit Cards: 1
> SELL (name or 'back'): Stolen Credit Cards
```

- **Choosing an Item to Sell**: Enter "Stolen Credit Cards" to sell the item.
- **Specifying Quantity**: You'll then be prompted to enter the quantity (e.g., "1").
- **Transaction Outcome**: The game will update your cash, inventory, and heat level based on the transaction.

This process repeats for other actions like moving to a different marketplace or buying upgrades, each affecting your resources and risk level.

---

## Troubleshooting

### Node.js Version
- **Dependency Issues**: If you encounter problems with dependencies, try deleting the `node_modules` folder and running `npm install` again.
- **Node.js Compatibility**: Ensure your Node.js version is compatible with the dependencies (version 14.x or higher is recommended).

### Python Version
- **Python Version**: The game requires Python 3.x. It may not work with Python 2.x.
- **Colorama Issues**: If colors are not displaying correctly, check your terminal settings or ensure `colorama` is installed properly.

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request with a clear description of your changes.

Please ensure that your code passes all unit tests and follows the project's coding standards.

---

