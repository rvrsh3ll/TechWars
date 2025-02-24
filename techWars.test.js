// techWars.test.js
import { generateDailyPrices, performBuy, performSell, applyUpgradeEffect, checkEvents, checkWinLose, items, marketplaces, upgrades } from './gameLogic.js';

describe('Tech Wars Game Logic', () => {
  describe('generateDailyPrices', () => {
    it('generates prices within base range for no multipliers', () => {
      jest.spyOn(Math, 'random').mockReturnValue(0.5);
      const dailyPrices = generateDailyPrices();
      const darkWeb = dailyPrices.find(m => m.marketplace === 'Dark Web Bazaar');
      const creditCardPrice = darkWeb.prices['Stolen Credit Cards'];
      const expected = Math.floor((0.5 * (50 - 10) + 10) * 1);
      expect(creditCardPrice).toBe(expected);
      Math.random.mockRestore();
    });

    it('applies multipliers correctly', () => {
      jest.spyOn(Math, 'random').mockReturnValue(0.5);
      const dailyPrices = generateDailyPrices();
      const hackerForum = dailyPrices.find(m => m.marketplace === 'Hacker Forum');
      const exploitPrice = hackerForum.prices['Zero-Day Exploits'];
      const base = items.find(i => i.name === 'Zero-Day Exploits').basePrice;
      const multiplier = marketplaces.find(m => m.name === 'Hacker Forum').priceMultipliers['Zero-Day Exploits'];
      const expected = Math.floor((0.5 * (base.max - base.min) + base.min) * multiplier);
      expect(exploitPrice).toBe(expected);
      Math.random.mockRestore();
    });
  });

  describe('performBuy', () => {
    let player;
    beforeEach(() => {
      player = { cash: 10000, inventory: {}, heat: 0, carryingCapacity: 10 };
    });

    it('buys item successfully', () => {
      const prices = { 'Stolen Credit Cards': 20 };
      const result = performBuy(player, 'Stolen Credit Cards', 2, prices);
      expect(result.success).toBe(true);
      expect(player.cash).toBe(9960);
      expect(player.inventory['Stolen Credit Cards']).toBe(2);
      expect(player.heat).toBe(5);
    });

    it('fails if insufficient funds', () => {
      const prices = { 'Zero-Day Exploits': 10000 };
      const result = performBuy(player, 'Zero-Day Exploits', 2, prices);
      expect(result.success).toBe(false);
      expect(player.cash).toBe(10000);
      expect(player.inventory).toEqual({});
    });

    it('fails if capacity exceeded', () => {
      player.inventory = { 'Stolen Credit Cards': 9 };
      const prices = { 'Stolen Credit Cards': 20 };
      const result = performBuy(player, 'Stolen Credit Cards', 2, prices);
      expect(result.success).toBe(false);
      expect(player.inventory['Stolen Credit Cards']).toBe(9);
    });
  });

  describe('performSell', () => {
    let player;
    beforeEach(() => {
      player = { cash: 1000, inventory: { 'Stolen Credit Cards': 5 }, heat: 10 };
    });

    it('sells item successfully', () => {
      const prices = { 'Stolen Credit Cards': 30 };
      const result = performSell(player, 'Stolen Credit Cards', 2, prices);
      expect(result.success).toBe(true);
      expect(player.cash).toBe(1060);
      expect(player.inventory['Stolen Credit Cards']).toBe(3);
      expect(player.heat).toBe(8);
    });

    it('fails if not enough items', () => {
      const prices = { 'Stolen Credit Cards': 30 };
      const result = performSell(player, 'Stolen Credit Cards', 6, prices);
      expect(result.success).toBe(false);
      expect(player.cash).toBe(1000);
      expect(player.inventory['Stolen Credit Cards']).toBe(5);
    });
  });

  describe('applyUpgradeEffect', () => {
    let player;
    beforeEach(() => {
      player = { heat: 30, carryingCapacity: 10, fastTravel: false };
    });

    it('reduces heat', () => {
      applyUpgradeEffect(player, 'reduceHeat');
      expect(player.heat).toBe(10);
    });

    it('enables fast travel', () => {
      applyUpgradeEffect(player, 'reduceTravelTime');
      expect(player.fastTravel).toBe(true);
    });

    it('increases capacity', () => {
      applyUpgradeEffect(player, 'increaseCapacity');
      expect(player.carryingCapacity).toBe(20);
    });
  });

  describe('checkEvents', () => {
    it('applies Marketplace Shutdown', () => {
      jest.spyOn(Math, 'random').mockReturnValue(0.01); // Trigger event
      const player = { location: marketplaces[1], inventory: { 'Stolen Credit Cards': 2 } };
      const messages = checkEvents(player);
      expect(player.location).toBe(marketplaces[0]);
      expect(player.inventory).toEqual({});
      expect(messages).toContain('Marketplace shut down! Moved to Dark Web Bazaar and lost all inventory.');
      Math.random.mockRestore();
    });
  });

  describe('checkWinLose', () => {
    it('loses if heat reaches 100', () => {
      const player = { heat: 100, day: 10, maxDays: 30, cash: 0, debt: 5000 };
      const result = checkWinLose(player);
      expect(result.over).toBe(true);
      expect(result.win).toBe(false);
    });

    it('wins if debt paid by day 30', () => {
      const player = { heat: 0, day: 31, maxDays: 30, cash: 6000, debt: 5000 };
      const result = checkWinLose(player);
      expect(result.over).toBe(true);
      expect(result.win).toBe(true);
    });

    it('loses if time out and debt unpaid', () => {
      const player = { heat: 0, day: 31, maxDays: 30, cash: 4000, debt: 5000 };
      const result = checkWinLose(player);
      expect(result.over).toBe(true);
      expect(result.win).toBe(false);
    });
  });
});
