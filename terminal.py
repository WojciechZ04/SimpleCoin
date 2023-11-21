class Terminal:
    def __init__(self):
        self.commands = {
            'show_bch': self.show_blockchain,
            'show_nodes': self.show_nodes,
            'help': self.help
        }

    def run_terminal(self):
        while True:
            command = input(">>>")
            if command.lower() in self.commands:
                self.commands[command.lower()]()
            else:
                print("Unknown command. Type 'help' to see all commands.")

    def show_blockchain(self):
        exit()

    def show_nodes(self):
        exit()

    def help(self):
        print("Available commands: ")
        for command in self.commands:
            print(f"{command}")


if __name__ == "__main__":
    terminal = Terminal()
    terminal.run_terminal()
