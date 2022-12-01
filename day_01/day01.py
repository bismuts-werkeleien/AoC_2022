import sys

with open(sys.argv[1], "r") as file:
    calorie_list = [value.strip("\n") for value in file]

# sum up for total calories per elf
calories = [0]
for i in range(len(calorie_list)):
    if calorie_list[i] != "":
        calories[-1] += int(calorie_list[i])
    else:
        calories.append(0)

# sort by number of calories
calories.sort()

print(f"Maximum three carried calories is {calories[-1:-4:-1]}, totalling {sum(calories[-1:-4:-1])}")

