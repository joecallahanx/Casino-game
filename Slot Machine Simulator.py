import random
import time

# Reel symbols and their odds
symbols = ['🍒', '🍋', '🔔', '🍇', '💎', '7️⃣']
weights = [30, 30, 20, 20, 8, 2]

money = 1000

rounds = 1

print("Welcome to Cal's Slots! 💋")
print(f"You're starting with ${money}. Don't spend it all at once! 😉\n")

while money > 0:
    print("=" * 10, f"ROUND {rounds}", "=" * 10)

    try:
        bet = int(input("How much you betting? (Multiples of 10 only): "))
        while bet % 10 != 0 or bet > money or bet <= 0:
            bet = int(input("C’mon, that’s not valid. Try again: "))
    except:
        print("🙄 Dude, numbers only. Try again.")
        continue

    money -= bet
    print("\nAlright... spinning those juicy reels for you 🍒💫")
    time.sleep(0.5)

    print("Spinning", end="")
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.4)
    print()

    reel = random.choices(symbols, weights=weights, k=3)
    print(" | ".join(reel))

    if reel[0] == reel[1] == reel[2]:
        symbol = reel[0]
        print("💥 JACKPOT, baby!!! You're on fire! 🔥")
        if symbol in ['🍒', '🍋']:
            multiplier = 3
        elif symbol in ['🔔', '🍇']:
            multiplier = 5
        elif symbol == '💎':
            multiplier = 10
        else:  # 7️⃣
            multiplier = 20

        payout = bet * multiplier
        money += payout
        print(f"You hit 3x {symbol} – that's {multiplier}x your bet!")
        print(f"💸 You just won ${payout}! Damn, you're lucky 😘")
    elif reel[0] == reel[1] or reel[1] == reel[2] or reel[0] == reel[2]:
        payout = int(bet * 1.5)
        money += payout
        print("Ooooh two matches! Not bad, dude! 😏")
        print(f"💰 Here's ${payout} to keep you spinning.")
    else:
        print("No match this time, sweet cheeks 😢 Better luck next spin!")

    print(f"💼 Balance check: ${money}")
    again = input("Wanna hit the reels again? (y/n): ").lower()
    if again != "y":
        print("Leaving so soon?")
        break

    rounds += 1
if money <= 0:
    print("\nYou're broke, sugarplum! 💸 No more spins...")

