// techWars.js
import chalk from 'chalk';
import readline from 'readline';
import { generateDailyPrices, getCurrentPrices, performBuy, performSell, applyUpgradeEffect, checkEvents, checkWinLose, items, marketplaces, upgrades } from './gameLogic.js';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

let player = {
  cash: 2500,
  debt: 5000,
  heat: 0,
  inventory: {},
  day: 1,
  maxDays: 30,
  location: marketplaces[0],
  carryingCapacity: 10,
  fastTravel: false
};

function displayStatus() {
  console.clear();
  console.log(chalk.white(`[SYSTEM] DAY ${player.day}/${player.maxDays}`));
  console.log(chalk.green(`[CASH] $${player.cash}`));
  console.log(chalk.red(`[DEBT] $${player.debt}`));
  console.log(chalk.yellow(`[HEAT] ${player.heat}%`));
  console.log(chalk.white('[INVENTORY]'));
  if (Object.keys(player.inventory).length === 0) {
    console.log('  Empty');
  } else {
    for (const [item, qty] of Object.entries(player.inventory)) {
      console.log(`  ${item}: ${qty}`);
    }
  }
  console.log(chalk.white(`[LOCATION] ${player.location.name}`));
  console.log('-------------------');
}

function displayMenu() {
  console.log('1. BUY ITEMS');
  console.log('2. SELL ITEMS');
  console.log('3. MOVE MARKET');
  console.log('4. UPGRADES');
  console.log('5. END DAY');
  rl.question('> COMMAND: ', handleCommand);
}

function handleCommand(choice) {
  switch (choice.trim()) {
    case '1':
      buyItems();
      break;
    case '2':
      sellItems();
      break;
    case '3':
      moveMarket();
      break;
    case '4':
      upgradesMenu();
      break;
    case '5':
      endDay();
      break;
    default:
      console.log(chalk.red('Invalid command'));
      setTimeout(gameLoop, 1000);
  }
}

function buyItems() {
  const prices = getCurrentPrices(player);
  console.log(chalk.white('[AVAILABLE ITEMS]'));
  items.forEach((item, index) => {
    console.log(`${index + 1}. ${item.name}: $${prices[item.name]}`);
  });
  rl.question('> BUY (number or "back"): ', choice => {
    if (choice === 'back') return gameLoop();
    const itemIndex = parseInt(choice) - 1;
    if (itemIndex < 0 || itemIndex >= items.length) {
      console.log(chalk.red('Invalid selection'));
      return setTimeout(gameLoop, 1000);
    }
    const itemName = items[itemIndex].name;
    rl.question('> QUANTITY: ', qty => {
      const quantity = parseInt(qty);
      if (isNaN(quantity) || quantity <= 0) {
        console.log(chalk.red('Invalid quantity'));
        return setTimeout(gameLoop, 1000);
      }
      const result = performBuy(player, itemName, quantity, prices);
      console.log(result.success ? chalk.green(`>>> ${result.message} <<<`) : chalk.red(`>>> ${result.message} <<<`));
      setTimeout(gameLoop, 1000);
    });
  });
}

function sellItems() {
  if (Object.keys(player.inventory).length === 0) {
    console.log(chalk.red('No items to sell'));
    return setTimeout(gameLoop, 1000);
  }
  const prices = getCurrentPrices(player);
  console.log(chalk.white('[INVENTORY]'));
  Object.entries(player.inventory).forEach(([item, qty], index) => {
    console.log(`${index + 1}. ${item}: ${qty} (Sell Price: $${prices[item]})`);
  });
  rl.question('> SELL (number or "back"): ', choice => {
    if (choice === 'back') return gameLoop();
    const itemIndex = parseInt(choice) - 1;
    const inventoryItems = Object.keys(player.inventory);
    if (itemIndex < 0 || itemIndex >= inventoryItems.length) {
      console.log(chalk.red('Invalid selection'));
      return setTimeout(gameLoop, 1000);
    }
    const itemName = inventoryItems[itemIndex];
    rl.question('> QUANTITY: ', qty => {
      const quantity = parseInt(qty);
      if (isNaN(quantity) || quantity <= 0) {
        console.log(chalk.red('Invalid quantity'));
        return setTimeout(gameLoop, 1000);
      }
      const result = performSell(player, itemName, quantity, prices);
      console.log(result.success ? chalk.green(`>>> ${result.message} <<<`) : chalk.red(`>>> ${result.message} <<<`));
      setTimeout(gameLoop, 1000);
    });
  });
}

function moveMarket() {
  console.log(chalk.white('[MARKETPLACES]'));
  marketplaces.forEach((m, index) => {
    console.log(`${index + 1}. ${m.name}${m.name === player.location.name ? ' (Current)' : ''}`);
  });
  rl.question('> MOVE (number or "back"): ', choice => {
    if (choice === 'back') return gameLoop();
    const marketIndex = parseInt(choice) - 1;
    if (marketIndex < 0 || marketIndex >= marketplaces.length) {
      console.log(chalk.red('Invalid selection'));
      return setTimeout(gameLoop, 1000);
    }
    if (marketplaces[marketIndex].name === player.location.name) {
      console.log(chalk.red('Already at this market'));
      return setTimeout(gameLoop, 1000);
    }
    player.location = marketplaces[marketIndex];
    if (!player.fastTravel) player.day++;
    console.log(chalk.green(`Moved to ${player.location.name}`));
    checkDayEvents();
  });
}

function upgradesMenu() {
  console.log(chalk.white('[UPGRADES]'));
  upgrades.forEach((u, index) => {
    console.log(`${index + 1}. ${u.name}: $${u.cost} - ${u.description}`);
  });
  rl.question('> UPGRADE (number or "back"): ', choice => {
    if (choice === 'back') return gameLoop();
    const upgradeIndex = parseInt(choice) - 1;
    if (upgradeIndex < 0 || upgradeIndex >= upgrades.length) {
      console.log(chalk.red('Invalid selection'));
      return setTimeout(gameLoop, 1000);
    }
    const upgrade = upgrades[upgradeIndex];
    if (player.cash < upgrade.cost) {
      console.log(chalk.red('Insufficient funds'));
      return setTimeout(gameLoop, 1000);
    }
    player.cash -= upgrade.cost;
    applyUpgradeEffect(player, upgrade.effect);
    console.log(chalk.green(`Purchased ${upgrade.name}`));
    setTimeout(gameLoop, 1000);
  });
}

function endDay() {
  player.day++;
  checkDayEvents();
}

function checkDayEvents() {
  const eventMessages = checkEvents(player);
  eventMessages.forEach(msg => console.log(chalk.yellow(`>>> ${msg} <<<`)));
  const result = checkWinLose(player);
  if (result.over) {
    console.log(result.win ? chalk.green(result.message) : chalk.red(result.message));
    rl.close();
  } else {
    setTimeout(gameLoop, 1000);
  }
}

function gameLoop() {
  displayStatus();
  displayMenu();
}

console.log(chalk.red('[Social Media Black Market]'));
gameLoop();
