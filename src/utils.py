'''
Utils
'''

# cycle through an array, return the new position : should be used in menus
def cycle(direc,menu,choice):
    if direc == "up":
        temp = menu[0]
        for i in range(len(menu) - 1):
            menu[i] = menu[i+1]
        menu[len(menu)-1] = temp
        choice = (choice - 1) % len(menu)
    elif direc == "down":
        temp = menu[len(menu)-1]
        for i in range(len(menu)-1,0,-1):
            menu[i] = menu[i-1]
        menu[0] = temp
        choice = (choice + 1) % len(menu)
    return choice