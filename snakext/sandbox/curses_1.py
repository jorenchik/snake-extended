import curses
import sys


def add_centered_menu(window, menu_items, menu_choice):
    # Get the size of the window
    height, width = window.getmaxyx()

    # Calculate the vertical starting position
    start_y = (height // 2) - (len(menu_items) // 2)

    # Display each menu item, centered
    for i, item in enumerate(menu_items):

        # Calculate horizontal position for the item
        start_x = (width // 2) - (len(item) // 2)
        choice_prefix = f" {'>' if menu_choice == i else ' '} "

        # Add the item to the window
        window.addstr(start_y + i, start_x, f"{choice_prefix}{item}")


def main(stdscr: curses.window) -> None:
    # Clear the screen
    stdscr.clear()
    curses.cbreak()
    curses.curs_set(0)

    # Menu items
    menu_items = {
        "New game": 0,
        "Settings": 1,
        "Quit game": 2,
    }
    menu_choice = 0
    choice_count = len(menu_items)

    add_centered_menu(stdscr, menu_items.keys(), menu_choice)

    while True:
        # Wait for user input
        key = stdscr.getch()

        # React to input
        if key == ord('q'):  # Exit on 'q'
            break
        elif key == ord('\n'):
            if menu_choice == menu_items["Quit game"]:
                break
        elif key == ord('j'):
            menu_choice = (menu_choice + 1) % choice_count
        elif key == ord('k'):
            menu_choice = (menu_choice - 1) % choice_count

        # Add centered menu
        add_centered_menu(stdscr, menu_items.keys(), menu_choice)

        # Refresh the screen to show changes
        stdscr.refresh()


# Run the program
curses.wrapper(main)
print("continue execution")
