/* glossary.js — site-wide term tooltips.
   Add a term here once and every article picks it up.
   Definitions are written for this site; they describe how a mechanic works
   rather than reproducing any card's printed text. */

(function () {
  var TERMS = {
    "Shield Trigger": "When a shield carrying this keyword breaks and enters your hand, you may cast it immediately without paying its cost \u2014 during your opponent's turn.",
    "Strike Back": "A spell that, when cast from hand, goes face-up on top of one of your own shields instead of to the graveyard, so it can be used a second time when that shield breaks.",
    "Revolution Change": "\u9769命チェンジ kakumei change — When a qualifying creature attacks, you may swap it with a Revolution Change card from your hand. The new creature continues the attack, arriving for no mana and already attacking.",
    "Rev. 0 Trigger": "革命0トリガー kakumei zero trigger — Playable from your hand for free, but only when a creature attacks you and you have no shields left. Several can be declared at once and resolve in the order you choose.",
    "Smash Burst": "\u30b9\u30de\u30c3\u30b7\u30e5\u30fb\u30d0\u30fc\u30b9\u30c8 \u2014 on a Twinpact creature: when it attacks, you may cast the card's own spell half without paying for it. The two halves stop being an either-or choice.",
    "Twinpact": "A single card with a creature on one half and a spell on the other. You choose which half to play; it has two costs printed on it.",
    "Blocker": "A keyword, not a default ability \u2014 only creatures with it can block. What it does is tap this creature and redirect the attack onto it.",
    "Speed Attacker": "Can attack the turn it arrives. Magic calls this haste.",
    "Mach Fighter": "Can attack a creature the turn it arrives, but not a player.",
    "GR summon": "GR召喚 GR shōkan — Turns over the top card of a separate twelve-card zone outside your deck and puts it into play. You do not choose which.",
    "Hyperspatial": "超次元 chōjigen — A zone outside the deck holding Psychic creatures. Unlike GR, cards here are summoned deterministically \u2014 an effect names what it brings out.",
    "Mana Arms": "マナ武装 mana busō — Switches on when your mana zone contains a stated number of cards of a given civilization.",
    "G-Zero": "Cast this card for free if a stated board condition is met.",
    "Slayer": "Destroys any creature it fights, whatever the power. Magic's deathtouch.",
    "Just Diver": "Untargetable and unblockable until the start of your next turn.",
    "Double Breaker": "Breaks two shields per attack.",
    "Triple Breaker": "Breaks three shields per attack.",
    "World Breaker": "Breaks all of the opponent's shields in one attack.",
    "New Division": "The rotating ranked format \u2014 older sets fall out over time. Used for the Grand Prix.",
    "All Division": "The ranked format that holds every set ever released. Separate ladder, separate metagame.",
    "Hall of Fame": "殿堂 dendō — The restriction system. Five categories rather than two, ranging from unrestricted to zero copies, plus pairs that cannot share a deck.",
    "mana zone": "マナゾーン — There are no land cards. Once per turn you put one card from your hand face-up here, permanently, and it counts as one mana.",
    "direct attack": "Attacking a player who has no shields left. This is how games are won.",
    "battle zone limit": "盤面制限 banmen seigen — PLAY'S caps each player at seven cards in the battle zone \u2014 creatures, Cross Gear and Dragheart combined. The paper game has no limit.",
    "B・A・D": "Lets you play the card for a stated amount less, at the price of it being destroyed at end of turn. On a Speed Attacker the drawback costs almost nothing on the turn you want it.",
    "G・G・G": "A conditional ability that switches on when your hand is down to one card or fewer \u2014 the state an aggressive deck ends up in naturally.",
    "shields": "Five face-down cards standing in for a life total. When one breaks it goes into the defender's hand, so attacking hands your opponent material.",
    "charge": "Putting a card from your hand into the mana zone, face-up and permanently. Once per turn, and the card is gone from your hand for good.",
    "civilization": "\u6587\u660e bunmei \u2014 the five colours, plus Zero. In PLAY'S a civilization is either present in your mana zone or it is not; the count does not matter.",
    "DP Hall of Fame": "DP\u6bbf\u5802 DP dend\u014d \u2014 the digital game's own restriction list, separate from paper. It can also do something paper cannot: rewrite a card's text.",
    "prohibited cards": "\u4f7f\u7528\u7981\u6b62\u30ab\u30fc\u30c9 shiy\u014d kinshi card \u2014 a short, unchanging banned list, separate from the Hall of Fame.",
    "Evolution": "進化 shinka — Placed on top of a creature you already control rather than summoned to an empty space. The stack counts as one creature, occupies one board slot, and can attack straight away if the one underneath could.",
    "Charger": "Spells only. After it resolves, the spell goes to your mana zone instead of the graveyard \u2014 an effect now, plus a mana afterwards.",
    "Invasion": "侵略 shinryaku — When a creature of a stated civilization and race attacks, you may stack this on top of it from hand for free, as an evolution. The attack carries on.",
    "Invasion ZERO": "\u4fb5\u7565ZERO \u2014 the defensive version: puts this into play for free on a stated trigger during your opponent's turn, rather than during your own attack.",
    "Ninja Strike": "Shinobi creatures only. Summons from your hand during your opponent's attack \u2014 a moment you normally could not act \u2014 with the condition tied to how few shields you have left.",
    "Seal": "封印 fūin — Cards placed face-down on top of a card in the battle zone. While sealed, that card is treated as though it were not there at all.",
    "Forbidden": "A card that starts in the battle zone before the game begins, sealed. Remove all its seals and it flips into an enormous creature.",
    "D2 Field": "Sits in the battle zone but is not a creature, so creature removal does not touch it. Only one can be out at a time.",
    "Denjara Switch": "A one-per-game effect on a D2 Field, used by turning the card upside down.",
    "O-Drive": "Pay an additional cost on top of the normal one when you use the card, and get an extra effect for it.",
    "Dragheart": "Arrives from outside the deck as a weapon or fortress rather than a creature, and flips to its creature side when a condition is met. Counts against the seven-card board limit.",
    "Dragsolution": "龍解 ryūkai — The flip that turns a Dragheart from its weapon or fortress side into its creature side.",
    "hand limit": "PLAY'S caps your hand at ten cards. Anything drawn beyond that goes straight to the graveyard. The paper game has no such cap.",
    "NEO Evolution": "NEO進化 NEO shinka — May be played either as an evolution or as an ordinary creature.",
    "Meteorburn": "Puts a stated number of cards from underneath an evolution creature into the graveyard to pay for an ability.",
    "Power Attacker": "Gains the stated power while attacking only \u2014 it is smaller on defence.",
    "Awakening": "覚醒 kakusei — A Psychic creature flips to a stronger reverse side once a stated condition is met.",
    "Final Revolution": "ファイナル革命 final kakumei — Triggers when the creature arrives specifically by Revolution Change. Playing it normally does not switch it on.",
    "Rinfinity": "輪廻∞ rinne infinity — Lets you cast a Twinpact's spell half while the creature stays in play, paying the cost, with an effect that scales off how many copies of the creature you control."
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
