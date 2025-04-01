import sys

game_over = False
won_game = False

# Dictionar pentru tranzitii
game_map = {
    'Entrance Hall': ['Armoury', 'Dining Room'],
    'Armoury': ['Treasury', 'Throne Room', 'Entrance Hall'],
    'Treasury': ['Library', 'Wizard\'s Study', 'Armoury', 'Dining Room'],
    'Library': ['Secret Exit', 'Treasury'],
    'Throne Room': ['Wizard\'s Study', 'Armoury'],
    'Wizard\'s Study': ['Secret Exit', 'Treasury', 'Throne Room'],
    'Dining Room': ['Kitchen', 'Treasury', 'Entrance Hall'],
    'Kitchen': ['Pantry', 'Dining Room'],
    'Pantry': ['Kitchen'],
    'Secret Exit': []
}

# starea initiala
current_room = 'Entrance Hall'

# inventarul trebuie sa fie initial gol
inventory = []

# dictionar pentru descrierea fiecarei camere
room_description = {
    'Entrance Hall': 'The grand foyer of the Castle of Illusions.',
    'Dining Room': 'A room with a large table filled with an everlasting feast.',
    'Kitchen': 'A room packed with peculiar ingredients.',
    'Armoury': 'A chamber filled with antiquated weapons and armour.',
    'Treasury': 'A glittering room overflowing with gold and gemstones.',
    'Library': 'A vast repository of ancient and enchanted texts.',
    'Pantry': 'A storage area for the Kitchen.',
    'Throne Room': 'The command center of the castle.',
    'Wizard\'s Study': 'A room teeming with mystical artifacts.',
    'Secret Exit': 'The hidden passage that leads out of the Castle of Illusions.'
}

# unde se afla initial fiecare item
item_found = {
    'key': 'Entrance Hall',
    'invitation': 'Dining Room',
    'chef\'s hat': 'Dining Room',
    'spoon': 'Kitchen',
    'sword': 'Armoury',
    'crown': 'Armoury',
    'ancient coin': 'Treasury',
    'spell book': 'Library',
    'magic wand': 'Wizard\'s Study'
}

# necesar pentru restart
item_found_cpy = {
    'key': 'Entrance Hall',
    'invitation': 'Dining Room',
    'chef\'s hat': 'Dining Room',
    'spoon': 'Kitchen',
    'sword': 'Armoury',
    'crown': 'Armoury',
    'ancient coin': 'Treasury',
    'spell book': 'Library',
    'magic wand': 'Wizard\'s Study'
}

# comenzi acceptate de joc
game_commands = ['go', 'look', 'inventory', 'take', 'drop']

def handle_input():
    # introducerea comenzilor
    user_in = input('\nEnter a command: ').split()

    # in 'command' retinem doar primul cuvant din comanda introdusa de user
    command = user_in[0].lower()

    # verificam daca ce a introdus user-ul este o comanda acceptata de joc
    if command not in game_commands:
        print('Invalid command! Try one of these: go [room name], look, inventory, take [item]')
        return

    # utilizam acest 'ok' pentru ca 'look'(comanda) sa poata fii reutilizata cu sens
    # altfel, de la primul 'look' functia look_room() se va apela automat si reutilizarea comenzii 'look' devine inutila
    # ok o sa fie adevarat (True) doar la momentul apelarii comenzii 'look'
    global ok

    # verificare pentru comanda 'go'
    if command == 'go':
        if len(user_in) < 1:
            print('Incomplete command! Try to specify a room')
            return
        # retinem camera specificata de user in 'room'
        room = ' '.join(user_in[1:])
        go_room(room)
        ok = False
    # verificam comanda 'look'
    elif command == 'look':
        look_room()
        ok = True
    # verificam comanda 'inventory'
    elif command == 'inventory':
        show_inventory()
    # verificam comanda 'take'
    elif command == 'take':
        if len(user_in) < 2:
            print('Incomplete command! Try to specify an item to pick up')
            return
        item = ' '.join(user_in[1:])
        take_item(item)
        ok = False
    # verificam comanda 'drop'
    elif command == 'drop':
        if len(user_in) < 2:
            print('Incomplete command! Try to specify an item to drop')
            return
        item = ' '.join(user_in[1:])
        drop_item(item)
        ok = False

def go_room(room):
    global current_room

    # verificam daca 'room' face parte din una din camerele asociate camerei in care suntem deja
    # user-ul se afla in current_room si prin comanda 'go' vrea sa ajunga in room
    # verificam si daca acesta are obiectele necesare in inventar pentru a ajunge in room
    if room in game_map[current_room]:
        if room == 'Armoury' and 'key' not in inventory:
            print('You need a key to access the Armoury.')
        elif room == 'Entrance Hall' and 'invitation' not in inventory:
            print('You need an invitation to return to the Entrance Hall.')
        elif room == 'Kitchen' and 'chef\'s hat' not in inventory:
            print('You need chef\'s hat to enter the Kitchen.')
        elif room == 'Pantry' and 'spoon' not in inventory:
            print('You need a spoon to enter the Pantry.')
        elif room == 'Treasury' and 'sword' not in inventory:
            print('You need a sword to enter the Treasury.')
        elif room == 'Throne Room' and 'crown' not in inventory:
            print('You need a crown to enter the Throne Room.')
        elif room == 'Library' and 'ancient coin' not in inventory:
            print('You need an ancient coin to enter the Library.')
        elif room == 'Wizard\'s Study' and 'spell book' not in inventory:
            print('You need the spell book to enter the Wizard\'s Study.')
        elif room == 'Secret Exit' and 'magic wand' not in inventory:
            print('You need the magic wand to enter this room.')
        else:
            current_room = room
            # conditia care opreste afisarea automata a datelor din look_room()
            if ok is True:
                look_room()
            check_game_status()
    else:
        print('You can\'t access the ', *room , ' from your current location!', sep='')

def look_room():
    # retinem lista de camera in care putem ajunge din current_room in adjacent_rooms
    adjacent_rooms = game_map[current_room]

    print('Current Room:', current_room)
    print('Description:', room_description[current_room])

    if adjacent_rooms:
        print('Adjacent Rooms:', ', '.join(adjacent_rooms))
    check_game_status()

def show_inventory():
    # afisarea obiectelor, daca exita in inventar
    if inventory:
        print('Inventory:', ', '.join(inventory))
    else:
        print('The inventory is empty.')

def take_item(item):
    # verificam daca item-ul introdus de user este in dictionarul de iteme si daca acesta(value) face parte din itemele din camera curenta, daca exista iteme in camera
    if item in item_found and item_found[item] == current_room:
        inventory.append(item)
        print('You picked up', item + '.')
        del item_found[item]
        check_game_status()
    else:
        print('Sorry! No such items found in this room')

def drop_item(item):
    # eliminarea unui item din inventar
    if item in inventory:
        inventory.remove(item)
        item_found[item] = current_room
        print('You dropped', item + '.')
        check_game_status()
    else:
        print('You don\'t have', item, 'in your inventory.')

def check_game_status():
    global game_over
    global won_game

    # in momentul in care ajungem in 'Secret Exit' jocul este castigat
    if current_room == 'Secret Exit':
        won_game = True
        game_over =True
        print('Congrats! You have escaped the Castle of Illusions!')
    elif not game_map[current_room]:
        game_over = True
        print('Game over! You are forever trapped in the Castle of Illusions :(')

    # se poate restarta jocul din momentul in care ajungi la final
    if game_over:
        play_again = input('\nWould you like to play again? (yes/no): ')
        if play_again.lower() == 'yes':
            reset_game()
        else:
            sys.exit('Thanks for playing 🏰')

def reset_game():
    # resetarea jocului pentru a putea juca avand inventarul gol, inapoi din starea initiala si itemele ssa se afle in camerele initiale
    global current_room
    global inventory
    global game_over
    global won_game

    current_room = 'Entrance Hall'
    inventory = []
    game_over = False
    won_game = False

    item_found.clear()
    item_found.update(item_found_cpy)

# introducerea
print('Welcome to the Castle of Illusions!')
print('You are trapped in this mystifying castle and must find the secret exit to escape.')
print('Use the available commands to navigate through the castle\n')
print('USER GUIDE:')
print('COMMANDS: go [room name], look, inventory, take [item], drop[item]')
print('The game is case sensitive! Please try to write the names of the rooms like in this example: Entrance Hall')
print('You must write the names of the rooms exactly how they are suggested when you use the command look.')
print('To reach some specific rooms you will need some items.')
print('LIST OF ITEMS IN THE GAME: key, invitation, chef\'s hat, spoon, sword, crown, ancient coin, spell book, magic wand.')
print('Analise every room carefully\n')
print('*We suggest using the command look at the begin, to see exactly where you are and where you can go*\n')
print('Good luck!!!')

while not game_over:
    handle_input()