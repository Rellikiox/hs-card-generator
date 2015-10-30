# hs-card-generator

Simulate obtaining a complete collection of cards.


## Things that aren't done yet:

- Card chances are not properly set up. The way it's now rares, epics and  legendaries get an above average chance of appearing (because if you get 5 commons one gets rerolled). How to fix: run some simulations and adjust values until we get something more similar to what's expected.

- Be able to calculate dust left until full collection

- Dust cards as soon as you open them and keep track of current collection dust value. WIll probably speed things up quite a bit.

- Calculate and "buy" the best expected value pack (currently it's random)

- Double check everything. First tests have given values that seem higher than they should be.

- Document everything.


## Things done:

- Simulate a pack being opened

- Simulate a collection being filled and dusted.

- Calculate dust left until full collection
