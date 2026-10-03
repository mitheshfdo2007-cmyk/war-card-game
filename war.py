import random
from datetime import datetime

# Card kit
suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
initial_deck = [rank + suit for rank in ranks for suit in suits] + ['JK', 'JK']  # 52 cards + 2 Jokers = 54

# Card values
card_values = {str(n): n for n in range(2, 11)}
card_values.update({'J': 11, 'Q': 12, 'K': 13, 'A': 14, 'JK': 15})

def get_value(card):
    return card_values[card[:-1]] if card != 'JK' else card_values['JK']

# WAR game explanation
def war(human_hand, pc_hand, h_cards, p_cards):
    war_pile = h_cards + p_cards
    war_count = 1

    while True:
        if len(human_hand) < 4 or len(pc_hand) < 4:
            if len(human_hand) < 4:
                war_pile += human_hand
                human_hand.clear()
                return 'P', war_pile, war_count
            else:
                war_pile += pc_hand
                pc_hand.clear()
                return 'H', war_pile, war_count

        h_battle = [human_hand.pop(0) for _ in range(4)]
        p_battle = [pc_hand.pop(0) for _ in range(4)]
        war_pile += h_battle + p_battle

        h_card = h_battle[-1]
        p_card = p_battle[-1]

        if get_value(h_card) > get_value(p_card):
            return 'H', war_pile, war_count
        elif get_value(h_card) < get_value(p_card):
            return 'P', war_pile, war_count
        else:
            war_count += 1
            continue

# User input
total_rounds = int(input("Enter how many rounds you want to play: "))
now = datetime.now()

# Shuffle deck 
random.shuffle(initial_deck)
half = len(initial_deck) // 2
human_hand = initial_deck[:half]
pc_hand = initial_deck[half:]

# Tracking results
round_details = []
cumulative_wars = 0

for current_round in range(1, total_rounds + 1):
    human_discard = []
    pc_discard = []
    round_results = []
    war_count = 0
    battle_num = 1
    if current_round>5:
        break

    while human_hand and pc_hand:
        h_card = human_hand.pop(0)
        p_card = pc_hand.pop(0)

        if get_value(h_card) > get_value(p_card):
            human_discard += [h_card, p_card]
            round_results.append((battle_num, h_card, p_card, 'H'))
        elif get_value(h_card) < get_value(p_card):
            pc_discard += [h_card, p_card]
            round_results.append((battle_num, h_card, p_card, 'P'))
        else:
            winner, war_pile, war_rounds = war(human_hand, pc_hand, [h_card], [p_card])
            war_count += war_rounds
            if winner == 'H':
                human_discard += war_pile
            else:
                pc_discard += war_pile
            round_results.append((battle_num, h_card, p_card, 'WAR'))

        battle_num += 1

    # Carry over all cards: deck + discard
    human_hand = human_hand + human_discard
    pc_hand = pc_hand + pc_discard
    cumulative_wars += war_count

    # Check all cards
    assert len(human_hand) + len(pc_hand) == 54, "Total cards lost! Check logic."

    round_details.append((current_round, round_results, len(pc_hand), len(human_hand), war_count))

    if not human_hand or not pc_hand:
        break

# Prepare results
output_content = []
output_content.append(f"Date : {now.strftime('%Y-%m-%d')}")
output_content.append(f"Time : {now.strftime('%H:%M')}")
output_content.append("")
output_content.append(f"Total Rounds    :  {len(round_details)}")
output_content.append("")

for round_num, results, pc_count, human_count, war_count in round_details:
    output_content.append(f"Round {round_num} results")
    output_content.append("-------------------------")
    output_content.append("No : Hum vs PC - Winner")
    for num, h, p, result in results:
        output_content.append(f"{num:2} : {h:<3} vs {p:<3} - {result}")
    output_content.append("")
    output_content.append(f"PC card count      {pc_count}")
    output_content.append(f"Human card count   {human_count}")
    output_content.append(f"War count          {war_count}")
    output_content.append("-" * 35)
    output_content.append("")

# Final counts
final_pc = len(pc_hand)
final_human = len(human_hand)

if final_pc > final_human:
    output_content.append(" PC won the game!")
elif final_human > final_pc:
    output_content.append(" Human won the game!")
else:
    output_content.append(" It's a tie!")

# Display results
print("\n".join(output_content))

# Save to file
filename = f"war_game_{now.strftime('%Y%m%d_%H%M%S')}.txt"
with open(filename, "w", encoding="utf-8") as file:
    file.write("\n".join(output_content))
    print(f"\nGame results saved to {filename}")

filename = f"war_game_{now.strftime('%Y%m%d_%H%M%S')}.html"
with open(filename, "w", encoding="utf-8") as file2:
    file2.write("<br>".join(output_content))
    print(f"<br>Game results saved to {filename}")

