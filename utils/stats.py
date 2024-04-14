import discord
from discord.ext import commands

# Load command counts from a text file
def load_command_counts():
    try:
        with open('command_counts.txt', 'r') as file:
            for line in file:
                user_id, command_name, count = line.strip().split(':')
                user_id = int(user_id)
                count = int(count)
                if user_id not in command_counts:
                    command_counts[user_id] = {}
                command_counts[user_id][command_name] = count
    except FileNotFoundError:
        pass

# Save command counts to a text file
def save_command_counts():
    with open('command_counts.txt', 'w') as file:
        for user_id, counts in command_counts.items():
            for command_name, count in counts.items():
                file.write(f'{user_id}:{command_name}:{count}\n')