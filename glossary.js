/* glossary.js — site-wide term tooltips.
   Add a term here once and every article picks it up.
   Definitions are written for this site; they describe how a mechanic works
   rather than reproducing any card's printed text. */

(function () {
  var TERMS = {
    "Shield Trigger": "When a shield carrying this keyword breaks and enters your hand, you may cast it immediately without paying its cost \u2014 during your opponent's turn.",
    "S-Back": "A spell that, when cast from hand, goes face-up on top of one of your own shields instead of to the graveyard, so it can be used a second time when that shield breaks.",
    "Revolution Change": "When a qualifying creature attacks, you may swap it with a Revolution Change card from your hand. The new creature continues the attack, arriving for no mana and already attacking.",
    "Revolution 0 Trigger": "Playable from your hand for free, but only when a creature attacks you and you have no shields left. Several can be declared at once and resolve in the order you choose.",
    "Twinpact": "A single card with a creature on one half and a spell on the other. You choose which half to play; it has two costs printed on it.",
    "Blocker": "A keyword, not a default ability \u2014 only creatures with it can block. What it does is tap this creature and redirect the attack onto it.",
    "Speed Attacker": "Can attack the turn it arrives. Magic calls this haste.",
    "Mach Fighter": "Can attack a creature the turn it arrives, but not a player.",
    "GR summon": "Turns over the top card of a separate twelve-card zone outside your deck and puts it into play. You do not choose which.",
    "super-dimension": "A zone outside the deck holding Psychic creatures. Unlike GR, cards here are summoned deterministically \u2014 an effect names what it brings out.",
    "Mana Arms": "Switches on when your mana zone contains a stated number of cards of a given civilization.",
    "G-Zero": "Cast this card for free if a stated board condition is met.",
    "Slayer": "Destroys any creature it fights, whatever the power. Magic's deathtouch.",
    "Just Diver": "Untargetable and unblockable until the start of your next turn.",
    "W-Breaker": "Breaks two shields per attack.",
    "T-Breaker": "Breaks three shields per attack.",
    "World Breaker": "Breaks all of the opponent's shields in one attack.",
    "New Division": "The rotating ranked format \u2014 older sets fall out over time. Used for the Grand Prix.",
    "All Division": "The ranked format that holds every set ever released. Separate ladder, separate metagame.",
    "Hall of Fame": "The restriction system. Five categories rather than two, ranging from unrestricted to zero copies, plus pairs that cannot share a deck.",
    "mana zone": "There are no land cards. Once per turn you put one card from your hand face-up here, permanently, and it counts as one mana.",
    "direct attack": "Attacking a player who has no shields left. This is how games are won.",
    "battle zone limit": "PLAY'S caps each player at seven cards in the battle zone \u2014 creatures, Cross Gear and Dragheart combined. The paper game has no limit.",
    "Rinfinity": "Lets you cast a Twinpact's spell half while the creature stays in play, paying the cost, with an effect that scales off how many copies of the creature you control."
  };

  if (/glossary\.html/.test(location.pathname)) return;

  var SKIP = { A: 1, H1: 1, H2: 1, H3: 1, H4: 1, CODE: 1, SCRIPT: 1, STYLE: 1, TABLE: 1 };
  var root = document.querySelector("article");
  if (!root) return;

  var keys = Object.keys(TERMS).sort(function (a, b) { return b.length - a.length; });
  var used = {};

  function inSkipped(node) {
    for (var n = node.parentNode; n && n !== root; n = n.parentNode) {
      if (SKIP[n.nodeName]) return true;
      if (n.classList && n.classList.contains("gl")) return true;
    }
    return false;
  }

  var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
  var nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);

  nodes.forEach(function (node) {
    if (inSkipped(node)) return;
    var text = node.nodeValue;
    for (var i = 0; i < keys.length; i++) {
      var term = keys[i];
      if (used[term]) continue;
      var at = text.indexOf(term);
      if (at < 0) continue;

      var before = text.slice(0, at);
      var after = text.slice(at + term.length);
      var span = document.createElement("span");
      span.className = "gl";
      span.setAttribute("data-gl", TERMS[term]);
      span.setAttribute("tabindex", "0");
      span.textContent = term;

      var parent = node.parentNode;
      parent.insertBefore(document.createTextNode(before), node);
      parent.insertBefore(span, node);
      node.nodeValue = after;

      /* keep the bubble on screen near the right edge */
      if (span.getBoundingClientRect().left > window.innerWidth * 0.55) {
        span.classList.add("right");
      }

      used[term] = 1;
      text = after;
      i = -1; /* restart so several terms can match in one text node */
    }
  });
})();
