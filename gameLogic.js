export const items = [
  { name: 'Stolen Credit Cards', basePrice: { min: 10, max: 50 }, risk: 'high' },
  { name: 'Zero-Day Exploits', basePrice: { min: 5000, max: 20000 }, risk: 'very high' },
  { name: 'Hacked Social Media Accounts', basePrice: { min: 5, max: 20 }, risk: 'low' },
  { name: 'Bitcurrency Wallets', basePrice: { min: 1000, max: 10000 }, risk: 'medium' },
];

export const marketplaces = [
  {
    name: 'Social Media Black Market',
    priceMultipliers: { 'Hacked Social Media Accounts': 1.3, 'Zero-Day Exploits': 0.7 },
    risks: { lawEnforcement: 0.02, scam: 0.05 }
  },
  {
    name: 'Hacker Forum',
    priceMultipliers: { 'Zero-Day Exploits': 1.2, 'Stolen Credit Cards': 0.8, 'Bitcurrency Wallets': 1.1 },
    risks: { lawEnforcement: 0.1, scam: 0.05 }
  },
  {
    name: 'DarkNet Auction House',
    priceMultipliers: { 'Zero-Day Exploits': 1.5, 'Stolen Credit Cards': 0.9, 'Bitcurrency Wallets': 1.2 },
    risks: { lawEnforcement: 0.15, scam: 0.04 }
  },
  {
    name: 'Cybercrime Bazaar',
    priceMultipliers: {},
    risks: { lawEnforcement: 0.05, scam: 0.05 }
  },
  {
    name: 'Malware Emporium',
    priceMultipliers: { 'Zero-Day Exploits': 1.1, 'Hacked Social Media Accounts': 0.8, 'Stolen Credit Cards': 0.7 },
    risks: { lawEnforcement: 0.08, scam: 0.07 }
  },
  {
    name: 'Silk Road',
    priceMultipliers: { 'Bitcurrency Wallets': 1.4, 'Stolen Credit Cards': 0.85, 'Zero-Day Exploits': 1.3 },
    risks: { lawEnforcement: 0.20, scam: 0.06 }
  },
];

export const upgrades = [
  { name: 'Better Encryption', cost: 5000, effect: 'reduceHeat', description: 'Reduces current heat by 20' },
  { name: 'Faster Internet', cost: 2000, effect: 'reduceTravelTime', description: 'Enables fast travel (moving doesn\'t take a day)' },
  { name: 'Secure Devices', cost: 3000, effect: 'increaseCapacity', description: 'Increases carrying capacity by 10' },
];

export const events = [
  {
    name: 'Marketplace Shutdown',
    probability: 0.05,
    effect: (player) => {
      const originalLocation = player.location.name;
      player.location = marketplaces[0]; // Move to Social Media Black Market
      player.inventory = {};
      player.current_prices = getCurrentPrices(player);
      return `ALERT: Agent Cyberstrike raided ${originalLocation}! Your inventory has been confiscated, and you've been forced to flee to ${player.location.name}.`;
    }
  },
  {
    name: 'Law Enforcement Trace',
    probability: 0.02,
    effect: (player) => {
      player.heat += 20;
      return "WARNING: Agent Cyberstrike has traced your activity! Heat increased by 20%.";
    }
  },
];

export function generateDailyPrices() {
  return marketplaces.map(marketplace => {
    const prices = {};
    items.forEach(item => {
      const base = item.basePrice;
      const multiplier = marketplace.priceMultipliers[item.name] || 1;
      const price = Math.floor((Math.random() * (base.max - base.min) + base.min) * multiplier);
      prices[item.name] = price;
    });
    return { marketplace: marketplace.name, prices };
  });
}

export function getCurrentPrices(player) {
  const dailyPrices = generateDailyPrices();
  return dailyPrices.find(m => m.marketplace === player.location.name).prices;
}

export function performBuy(player, itemName, quantity, prices) {
  const item = items.find(i => i.name === itemName);
  if (!item) return { success: false, message: 'Item not found' };
  const price = prices[itemName];
  const totalCost = price * quantity;
  const currentItems = Object.values(player.inventory).reduce((a, b) => a + b, 0);
  if (player.cash < totalCost) {
    return { success: false, message: 'Insufficient funds' };
  } else if (currentItems + quantity > player.carryingCapacity) {
    return { success: false, message: 'Carrying capacity exceeded' };
  } else {
    player.cash -= totalCost;
    player.inventory[itemName] = (player.inventory[itemName] || 0) + quantity;
    player.heat += item.risk === 'very high' ? 10 : item.risk === 'high' ? 5 : item.risk === 'medium' ? 3 : 1;
    return { success: true, message: `Acquired ${quantity} ${itemName} for $${totalCost}` };
  }
}

export function performSell(player, itemName, quantity, prices) {
  if (!player.inventory[itemName] || player.inventory[itemName] < quantity) {
    return { success: false, message: 'Not enough items to sell' };
  }
  const price = prices[itemName];
  const totalEarned = price * quantity;
  player.cash += totalEarned;
  player.inventory[itemName] -= quantity;
  if (player.inventory[itemName] === 0) delete player.inventory[itemName];
  player.heat = Math.max(0, player.heat - 2);
  return { success: true, message: `Sold ${quantity} ${itemName} for $${totalEarned}` };
}

export function applyUpgradeEffect(player, effect) {
  switch (effect) {
    case 'reduceHeat':
      player.heat = Math.max(0, player.heat - 20);
      break;
    case 'reduceTravelTime':
      player.fastTravel = true;
      break;
    case 'increaseCapacity':
      player.carryingCapacity += 10;
      break;
  }
}

export function checkEvents(player) {
  const messages = [];
  events.forEach(event => {
    if (Math.random() < event.probability) {
      const message = event.effect(player);
      if (message) messages.push(message);
    }
  });
  return messages;
}

export function checkWinLose(player) {
  if (player.heat >= 100) {
    return { over: true, win: false, message: 'Heat reached 100%. Agent Cyberstrike has arrested you!' };
  }
  if (player.day > player.maxDays) {
    if (player.cash >= player.debt) {
      return { over: true, win: true, message: 'Debt paid off after 30 days! You win!' };
    } else {
      return { over: true, win: false, message: "Time's up! Debt unpaid. You lose!" };
    }
  }
  return { over: false };
}
