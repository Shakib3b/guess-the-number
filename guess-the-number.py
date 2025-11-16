import random

def choose_difficulty():
    print("\nChoose difficulty:")
    print("1 - Easy   (1-20, 10 attempts)")
    print("2 - Medium (1-100, 7 attempts)")
    print("3 - Hard   (1-500, 5 attempts)")
    print("4 - Custom (you set range and attempts)")
    while True:
        choice = input("Enter 1/2/3/4: ").strip()
        if choice == '1':
            return 1, 20, 10
        if choice == '2':
            return 1, 100, 7
        if choice == '3':
            return 1, 500, 5
        if choice == '4':
            try:
                low = int(input("Enter lower bound (>=1): ").strip())
                high = int(input("Enter upper bound (> lower bound): ").strip())
                attempts = int(input("Enter max attempts (>=1, 0 for unlimited): ").strip())
                if low >= high or low < 1 or attempts < 0:
                    print("Invalid custom values, try again.")
                    continue
                return low, high, (attempts if attempts != 0 else None)
            except ValueError:
                print("Please enter integer values. Try again.")
        else:
            print("Choose 1, 2, 3, or 4.")

def give_hint(secret, low, high, difficulty_label):
    """
    Returns a string hint and the 'cost' in attempts (1).
    Hint types:
      - parity + small divisibility
      - narrowed range around the secret
    """
    # parity/divisibility hint
    if random.random() < 0.5:
        parity = "even" if secret % 2 == 0 else "odd"
        div3 = "is" if secret % 3 == 0 else "is not"
        return f"Hint: The number is {parity} and it {div3} divisible by 3.", 1
    # range hint: window depends on difficulty
    if difficulty_label == "Easy":
        window = 4
    elif difficulty_label == "Medium":
        window = 10
    elif difficulty_label == "Hard":
        window = 20
    else:
        window = max(4, (high - low) // 10)
    start = max(low, secret - window)
    end = min(high, secret + window)
    return f"Hint: The number is between {start} and {end}.", 1

def play_round():
    low, high, max_attempts = choose_difficulty()
    # determine difficulty label for hint window
    diff_label = "Custom"
    if (low, high, max_attempts) == (1, 20, 10):
        diff_label = "Easy"
    elif (low, high, max_attempts) == (1, 100, 7):
        diff_label = "Medium"
    elif (low, high, max_attempts) == (1, 500, 5):
        diff_label = "Hard"

    secret = random.randint(low, high)
    attempts = 0
    hints_used = 0
    prev_distance = None
    prev_guess = None

    if max_attempts is None:
        print(f"\nGuess a number between {low} and {high}. You have unlimited attempts.")
    else:
        print(f"\nGuess a number between {low} and {high}. You have {max_attempts} attempts.")
    print("Type 'hint' to use a hint (costs 1 attempt). Type 'quit' to give up.")

    while True:
        if max_attempts is not None and attempts >= max_attempts:
            print(f"\nOut of attempts! The secret number was {secret}.")
            return False, attempts, hints_used  # lost

        raw = input(f"\nEnter your guess (attempt {attempts+1}): ").strip().lower()
        if raw == 'quit':
            print(f"You gave up. The number was {secret}.")
            return False, attempts, hints_used
        if raw == 'hint':
            hint_text, cost = give_hint(secret, low, high, diff_label)
            hints_used += 1
            # applying cost
            attempts += cost
            print(hint_text)
            # if after taking hint we exceed attempts, handle loop top to check losing condition
            continue

        try:
            guess = int(raw)
        except ValueError:
            print("Please enter a valid integer, 'hint', or 'quit'.")
            continue

        if guess < low or guess > high:
            print(f"Please guess a number within the range {low}-{high}.")
            continue

        attempts += 1
        distance = abs(secret - guess)

        if guess == secret:
            print(f"\nCorrect! You guessed the number in {attempts} attempt(s) with {hints_used} hint(s).")
            return True, attempts, hints_used

        # give high/low
        if guess > secret:
            print("Too high!")
        else:
            print("Too low!")

        # warmer/colder compared to previous guess
        if prev_distance is None:
            print("No warmer/colder comparison yet (this was your first guess).")
        else:
            if distance < prev_distance:
                print("Warmer — you're getting closer!")
            elif distance > prev_distance:
                print("Colder — you're moving away.")
            else:
                print("Same distance as your previous guess.")

        prev_distance = distance
        prev_guess = guess

def main():
    print("Welcome to Guess the Number! 🎯")
    while True:
        won, attempts, hints = play_round()
        if won:
            print("Well done! 🎉")
        else:
            print("Good try — you'll get it next time!")
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again not in ('y', 'yes'):
            print("Thanks for playing — goodbye!")
            break

if __name__ == "__main__":
    main()
