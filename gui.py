import os
import sys
import time

def clear_screen():
    os.system(['clear', 'cls'][os.name == 'nt'])


def main_menu():
    choice = 0

    print('1')
    print('2')
    print('3')
    print('4')
    print('5 to exit')
    try:
        choice = int(input('WAS TUN?: '))
    except ValueError:
        print("\nBITTE ETWAS EINGEBEN!?!?!?")

    if choice == 1:
        return 1
    elif choice == 2:
        return 2
    elif choice == 3:
        return 3
    elif choice == 4:
        return 4
    elif choice == 5:
        return 5
    else:
        return 0


def main():
    clear_screen()
    lernmodus = 0

    while (True):
        clear_screen()
        lernmodus = main_menu()
        if lernmodus == 1:
            clear_screen()
            print(1)
            time.sleep(3)
        elif lernmodus == 2:
            print(2)
        elif lernmodus == 3:
            print(3)
        elif lernmodus == 4:
            print(4)
        elif lernmodus == 5:
            clear_screen()
            sys.exit()
        else:
            print("extremely bad error")
            break

if __name__ == '__main__':
    main()
