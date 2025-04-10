import random
from itertools import combinations
import time
from operator import truediv

print("Welcome to Cal's Casino 🍾\n\n"
      "What game are you in the mood for today?\n"
      "Games available:\n")

while True: # Entire Game Loop
    game_choice = input("\n1 - Poker - Texas Hold'em\n"
                        "2 - Blackjack\n"
                        "3 - Roulette\n"
                        "(q to quit)").strip().lower()


    def poker():
        hand_ranks = {
            "High Card": 0, "One Pair": 1, "Two Pair": 2, "Three of a Kind": 3,
            "Straight": 4, "Flush": 5, "Full House": 6, "Four of a Kind": 7, "Straight Flush": 8
        }

        def card_value(card):
            face = card[:-1]
            face_values = {
                '2': 2, '3': 3, '4': 4, '5': 5,
                '6': 6, '7': 7, '8': 8, '9': 9,
                '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
            }
            return face_values[face]

        def is_flush(cards):
            suits = [c[-1] for c in cards]
            for s in set(suits):
                suited = [c for c in cards if c[-1] == s]
                if len(suited) >= 5:
                    return True, sorted(suited, key=card_value, reverse=True)[:5]
            return False, []

        def is_straight(values):
            values = sorted(set(values), reverse=True)
            for i in range(len(values) - 4):
                if values[i] - values[i + 4] == 4:
                    return True, values[i]
            if {14, 2, 3, 4, 5}.issubset(values):
                return True, 5
            return False, None

        def get_hand_rank(cards):
            values = [card_value(c) for c in cards]
            val_counts = {v: values.count(v) for v in set(values)}
            count_order = sorted(val_counts.items(), key=lambda x: (-x[1], -x[0]))
            is_flush_hand, flush_cards = is_flush(cards)
            is_straight_hand, straight_high = is_straight(values)

            if is_flush_hand and is_straight_hand:
                return ("Straight Flush", straight_high)
            if 4 in val_counts.values():
                four = count_order[0][0]
                kicker = max(v for v in values if v != four)
                return ("Four of a Kind", four, kicker)
            if sorted(val_counts.values()) == [2, 3]:
                three, pair = count_order[0][0], count_order[1][0]
                return ("Full House", three, pair)
            if is_flush_hand:
                return ("Flush", *sorted([card_value(c) for c in flush_cards], reverse=True))
            if is_straight_hand:
                return ("Straight", straight_high)
            if 3 in val_counts.values():
                three = count_order[0][0]
                kickers = [v for v in values if v != three][:2]
                return ("Three of a Kind", three, *kickers)
            if list(val_counts.values()).count(2) >= 2:
                pairs = [v for v, c in count_order if c == 2][:2]
                kicker = max(v for v in values if v not in pairs)
                return ("Two Pair", *pairs, kicker)
            if 2 in val_counts.values():
                pair = count_order[0][0]
                kickers = [v for v in values if v != pair][:3]
                return ("One Pair", pair, *kickers)
            return ("High Card", *sorted(values, reverse=True)[:5])

        def evaluate_hand(cards):
            best = ("High Card", 0)
            for combo in combinations(cards, 5):
                score = get_hand_rank(combo)
                if score > best:
                    best = score
            return best

        def betting_round(cash, bot_cash, pot, min_bet):
            while True:
                move = input("Your move (fold/call/raise): ").lower()
                if move == "fold":
                    print("You folded 💔 Bot scoops the pot.")
                    return "fold", cash, bot_cash, pot
                elif move == "call":
                    print("You called. Let's keep this spicy 🔥")
                    cash -= min_bet
                    bot_cash -= min_bet
                    pot += min_bet * 2
                    return "call", cash, bot_cash, pot
                elif move == "raise":
                    try:
                        r = int(input("Raise amount (min $10): "))
                        if r < 10:
                            print("C’mon, raise like you mean it 😉")
                            continue
                        if r > cash:
                            print("You can’t bet more than you got, babe 😅")
                            continue
                        if r > bot_cash:
                            print("Bot folds! You scared it off 😏")
                            cash += pot
                            return "fold_bot", cash, bot_cash, pot
                        cash -= r
                        bot_cash -= r
                        pot += r * 2
                        print(f"You raised ${r}. Bot matches.")
                        return "raise", cash, bot_cash, pot
                    except ValueError:
                        print("That's not a number, cutie 💀")
                else:
                    print("Say 'fold', 'call', or 'raise', darling 😘")

        def play_poker():
            print("♠️♥️ Welcome to Poker Night, darling 💋")
            name = input("What's your name, heartbreaker? ➡ ").strip().title()
            cash, bot_cash = 1000, 1000

            while True:
                print(f"\n{name}: ${cash} | Bot: ${bot_cash}")
                print("Shuffling the cards... 🎴")

                deck = [f"{v}{s}" for s in '♠♥♦♣' for v in
                        ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]
                random.shuffle(deck)

                pot, blind, bb = 30, 10, 20
                cash -= blind
                bot_cash -= bb

                hand = [deck.pop(), deck.pop()]
                bot_hand = [deck.pop(), deck.pop()]
                print(f"\nYour hand: {hand[0]}  {hand[1]}")

                move, cash, bot_cash, pot = betting_round(cash, bot_cash, pot, bb)
                if move in ["fold", "fold_bot"]:
                    continue

                community, stages = [], ["Flop", "Turn", "River"]
                for stage, count in zip(stages, [3, 1, 1]):
                    community += [deck.pop() for _ in range(count)]
                    print(f"{stage}: {'  '.join(community[-count:])}")
                    move, cash, bot_cash, pot = betting_round(cash, bot_cash, pot, bb)
                    if move in ["fold", "fold_bot"]:
                        break
                else:
                    print("\n👀 Showdown time!")
                    your_hand = evaluate_hand(hand + community)
                    bot_final = evaluate_hand(bot_hand + community)

                    print(f"\n{name}'s Hand: {your_hand[0]} ({your_hand[1:]})")
                    print(f"Bot's Hand: {bot_final[0]} ({bot_final[1:]})")

                    if hand_ranks[your_hand[0]] > hand_ranks[bot_final[0]] or (
                            hand_ranks[your_hand[0]] == hand_ranks[bot_final[0]] and your_hand[1:] > bot_final[1:]):
                        print(f"🏆 You win ${pot}! Damn, you’re good 😍")
                        cash += pot
                    elif hand_ranks[your_hand[0]] < hand_ranks[bot_final[0]] or (
                            hand_ranks[your_hand[0]] == hand_ranks[bot_final[0]] and your_hand[1:] < bot_final[1:]):
                        print("Bot takes it... but you looked hot doing it 😘")
                        bot_cash += pot
                    else:
                        print("Split pot! It’s a tie, just like us 🥰")
                        cash += pot // 2
                        bot_cash += pot // 2

                print(f"\n{name}'s 💼 Profit: ${cash - 1000}")
                print(f"Bot's 📉 Profit: ${bot_cash - 1000}")
                if input("Wanna play again? (yes/no): ").lower() != "yes":
                    print("Game over, sweetheart. I’ll be dreaming of our next round 😚")
                    break

        play_poker()


    def blackjack():
        suits_symbols = {"Spades": "♠", "Hearts": "♥", "Diamonds": "♦", "Clubs": "♣"}
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        values = {r: min(10, i + 2) if r.isdigit() else 10 for i, r in enumerate(ranks)}
        values['A'] = 11

        def create_deck():
            deck = []
            for suit, symbol in suits_symbols.items():
                for rank in ranks:
                    deck.append({'name': f"{rank}{symbol}", 'value': values[rank], 'rank': rank})
            random.shuffle(deck)
            return deck

        def calculate_hand_value(hand):
            value = sum(values[c['rank']] for c in hand)
            aces = sum(1 for c in hand if c['rank'] == 'A')
            while value > 21 and aces:
                value -= 10
                aces -= 1
            return value

        money = 100
        initial_money = money
        dealers_money = 100
        rounds = 1
        wins = losses = ties = 0
        deck = create_deck()

        def leaderboard():
            again = input("\nDo you want to play another round? (y/n): ").strip().lower()
            if again != 'y':
                print(f"\n🪙 Thanks for playing, darling. The house always remembers a good game.")
                profit = money - initial_money
                print(f"\nLEADERBOARD 📊")
                print(f"Total Rounds Played: {rounds - 1}")
                print(f"✅ Wins: {wins} | ❌ Losses: {losses} | 🤝 Ties: {ties}")
                if profit > 0:
                    print(f"💰 You made a profit of ${profit}! Well played, legend 😎")
                elif profit < 0:
                    print(f"😢 You lost ${-profit}. Better luck next time, sweetheart.")
                else:
                    print("⚖️ You broke even! Not bad at all 🃏")
                print(f"🧾 Final Stack: ${money}")
                exit()  # ends the game completely

        while True:
            print(f"\n{'=' * 10} ROUND {rounds} {'=' * 10}")
            rounds += 1
            bet = 0

            if money < 10:
                print(f"\n💸 You only have ${money} left.")
                buy = input("Do you want to buy more chips? (y/n): ").strip().lower()
                if buy == 'y':
                    while True:
                        try:
                            buy_in = int(input("Enter amount (multiples of 10): "))
                            if buy_in % 10 == 0:
                                break
                            else:
                                print("Must be a multiple of 10. Try again, cutie 😘")
                        except ValueError:
                            print("Enter a valid number, sweetheart 💁‍♀️")
                    money += buy_in
                    print(f"Your new balance: ${money}")
                else:
                    print("Thanks for playing! 🥹💔")
                    break

            if dealers_money < 10:
                print("\n🏆 The dealer is out of money!")
                print("🎉 YOU WIN THE GAME, Sweetheart! 💕")
                break

            while True:
                print(f"\n💰 Your Stack: ${money}")
                print(f"🏦 Dealer Stack: ${dealers_money}")
                betting = input("Do you want to bet $10? (y = yes, raise = raise amount, n = quit): ").strip().lower()
                if betting == 'y':
                    if money >= 10:
                        bet = 10
                        break
                    else:
                        print("You don't have enough money to bet!")
                elif betting == 'raise':
                    while True:
                        try:
                            raise_amt = int(input("Raise amount (must be multiple of 10): "))
                            if raise_amt % 10 == 0 and raise_amt <= money:
                                bet = raise_amt
                                break
                            else:
                                print("Invalid amount. Enter a valid raise, sweetheart 💋")
                        except ValueError:
                            print("Please enter a number, not letters cutie 😅")
                    break
                elif betting == 'n':
                    print("Thanks for playing, Sweetheart! 💕")
                    leaderboard()
                    break
                else:
                    print("Invalid choice!")

            if bet == 0:
                break

            money -= bet
            dealers_money -= bet

            if len(deck) < 15:
                print("🔁 Reshuffling deck for a fresh hand... ♣️")
                deck = create_deck()

            dealer_card1 = deck.pop()
            dealer_card2 = deck.pop()
            player_card1 = deck.pop()
            player_card2 = deck.pop()

            print(f"\n🃏 Dealer's Cards:\n{dealer_card1['name']}   🂠")
            print(f"\n🧍‍♂️ Your Cards:\n{player_card1['name']}   {player_card2['name']}")
            player_hand = [player_card1, player_card2]
            player_value = calculate_hand_value(player_hand)
            print(f"🎯 Your Hand Value: {player_value}")

            while player_value < 21:
                choice = input("Would you like to Hit or Stand? ").strip().lower()
                if choice == 'hit':
                    new_card = deck.pop()
                    player_hand.append(new_card)
                    player_value = calculate_hand_value(player_hand)
                    print(f"You drew: {new_card['name']}")
                    print(f"New Hand Value: {player_value}")
                elif choice == 'stand':
                    break
                else:
                    print("Please enter 'hit' or 'stand'")

            if player_value > 21:
                print("💥 Bust! You lose this round.")
                print("Dealer smirks. 'Better luck next time, sweetheart.' 😌")
                dealers_money += bet * 2
                losses += 1
                continue

            print("\n🎭 Dealer reveals hidden card...")
            time.sleep(1)
            print(f"{dealer_card1['name']}   {dealer_card2['name']}")
            dealer_hand = [dealer_card1, dealer_card2]
            dealer_value = calculate_hand_value(dealer_hand)
            print(f"Dealer's Hand Value: {dealer_value}")

            while dealer_value < 17:
                time.sleep(1)
                new_card = deck.pop()
                dealer_hand.append(new_card)
                dealer_value = calculate_hand_value(dealer_hand)
                print(f"Dealer draws: {new_card['name']}")
                print(f"Dealer's Hand Value: {dealer_value}")

            if dealer_value > 21 or player_value > dealer_value:
                print(f"\n🎉 You win ${bet * 2}!")
                money += bet * 2
                wins += 1
            elif player_value == dealer_value:
                print(f"\n🤝 It's a tie! You get your bet back.")
                money += bet
                dealers_money += bet
                ties += 1
            else:
                print(f"\n🏳️ Dealer wins this round and takes your bet.")
                dealers_money += bet * 2
                losses += 1

            leaderboard()


    def roulette():
        # Set of red and black numbers on the wheel
        reds = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        blacks = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

        # Flirty win/loss reactions for extra spice 😏
        win_lines = [
            "You're killing it! 🔥",
            "Oooohhh yessss 😘",
            "Told ya this was your game 💃",
            "Who’s the boss now? You are 😎",
            "Keep printing money, baby 💸",
            "You're on fire, baby! 🔥",
            "Oooh yes! Daddy likey 😘",
            "Told you luck’s on your side 😉",
            "That's how you roll, sugar 💃",
            "Money never looked so good on you 💸"
        ]

        loss_lines = [
            "Aww, rough spin 😢",
            "Next time, cutie... 😘",
            "Bad luck... but great vibes 💔",
            "We’ll bounce back hotter 😤",
            "That one hurt, ngl 🥲",
            "Oof. Let me kiss that pain away 😚",
            "We win some, we learn some 😢",
            "Bad luck, but hot spirit 🔥",
            "Don’t let it get you down, cutie 💋",
            "I’m still proud of you, babe 😘"
        ]

        # Helper to get the color of a number
        def get_color(n):
            if n == 0:
                return "Green"
            return "Red" if n in reds else "Black"

        # Helper to show number in color
        def print_spin_result(num, col):
            if col == "Red":
                print(f"The ball spins... and lands on \033[91m{num} {col}\033[0m! 🔴")
            elif col == "Black":
                print(f"The ball spins... and lands on \033[90m{num} {col}\033[0m! ⚫")
            else:
                print(f"The ball spins... and lands on \033[92m{num} {col}\033[0m! 🟢")

        # Function that does the wheel spin
        def spin():
            print("\nSpinning... hold your breath 💫")
            time.sleep(2)
            result = random.randint(0, 36)
            color = get_color(result)
            print_spin_result(result, color)
            return result, color

        # Main game loop
        def play():
            print("🎰 Welcome to the Cal's Roulette Lounge! Let's make some money, baby 💋")

            money = 500  # starting cash
            game_log = []
            og_cash = money

            while money > 0:
                print(f"\nYou have: ${money}")
                print("Place your bet:")
                print("1) Red/Black  2) Odd/Even  3) Exact Number")
                print("Or press Q to walk away with style 😎")

                choice = input("Pick your option (1/2/3 or Q): ").lower()
                if choice == 'q':
                    print("Okay, exiting like a classy legend 🕶️")
                    break

                try:
                    bet = int(input("How much you wanna bet? $"))
                except:
                    print("That’s not cash, cutie. Try again 😅")
                    continue

                if bet <= 0 or bet > money:
                    print("Not a valid amount, baby 💸")
                    continue
                if bet < 5:
                    print("C'mon, at least $5 to make it spicy 😏")
                    continue
                if bet > 1000:
                    print("Whoa there, Mr. Billionaire 😳")
                    continue

                guess = None
                if choice == '1':
                    guess = input("Red or Black? ").capitalize()
                    if guess not in ['Red', 'Black']:
                        print("That’s not on the color wheel, sweetheart 💋")
                        continue
                elif choice == '2':
                    guess = input("Odd or Even? ").capitalize()
                    if guess not in ['Odd', 'Even']:
                        print("Pick one, love 🥺")
                        continue
                elif choice == '3':
                    try:
                        guess = int(input("Your lucky number (0-36): "))
                        if guess < 0 or guess > 36:
                            print("That number’s not even on the wheel! 😅")
                            continue
                    except:
                        print("Use your digits, not letters, babe 💁")
                        continue
                else:
                    print("You’re pressing all the wrong buttons, sugar 😘")
                    continue

                spun, spin_color = spin()
                win = False
                payout = 0

                # Evaluation time!
                if choice == '1':
                    if guess == spin_color:
                        payout = bet
                        money += payout
                        print(random.choice(win_lines))
                        win = True
                    else:
                        money -= bet
                        print(random.choice(loss_lines))

                elif choice == '2':
                    if spun == 0:
                        money -= bet
                        print("Zero hits different. No win 🟢😔")
                    elif (spun % 2 == 0 and guess == 'Even') or (spun % 2 != 0 and guess == 'Odd'):
                        payout = bet
                        money += payout
                        print(random.choice(win_lines))
                        win = True
                    else:
                        money -= bet
                        print(random.choice(loss_lines))

                elif choice == '3':
                    if spun == guess:
                        payout = bet * 35
                        money += payout
                        print("BIG WIN!!! 🤑 Jackpot vibes only!")
                        win = True
                    else:
                        money -= bet
                        print("Not this time, hot stuff 💔")

                # Store round details
                game_log.append({
                    'bet_on': guess,
                    'spun': spun,
                    'color': spin_color,
                    'amount': bet,
                    'result': "Win" if win else "Loss",
                    'gain': payout
                })

                if money == 0:
                    print("You’re all out of cash... but you’re still rich in sex appeal 😘")
                    break

                cont = input("Play another round? (Y/N): ").lower()
                if cont != 'y':
                    break

            # Recap time 💌
            print(f"\nGame over, gorgeous! You finished with ${money}")
            net = money - og_cash
            print(f"💰 {'Profit' if net >= 0 else 'Loss'}: ${abs(net)}")

            if game_log:
                print("\nHere’s the hot gossip from your session:")
                for idx, g in enumerate(game_log, 1):
                    col_code = "\033[91m" if g['color'] == 'Red' else "\033[90m" if g[
                                                                                        'color'] == 'Black' else "\033[92m"
                    print(
                        f"{idx}. Bet on {g['bet_on']} | Landed: {col_code}{g['spun']} {g['color']}\033[0m → {g['result']} (+${g['gain']})")

        play()


    if game_choice == "1":
        poker()
    elif game_choice == "2":
        blackjack()
    elif game_choice == "3":
        roulette()
    elif game_choice == "q":
        print("Thanks for playing, darling. The house always remembers a good game.")
        break
    else:
        print("Sorry! We dont have that game right now")