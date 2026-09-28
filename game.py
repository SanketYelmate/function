import random
item_list = ["rock","paper","scissor"]

user_choice = input("enter your choice = rock,paper,scissor ")
com_choice = random.choice(item_list) 
print(f"user choice = {user_choice},computer choice = {com_choice}")
if user_choice == com_choice:
    print("match is tie up")
elif user_choice = "Rock":
  if com_choice = "paper":
        print("paper cover rock = computer are win")
  else:
