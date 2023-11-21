class Terminal:
    def __init__(self):
        self.commands = {
            'create': self.create_block,
            'show': self.show_blockchain,
            'verify': self.verify,
            'help': self.help
        }

    def run_terminal(self):
        while True:
            command = input(">>>")
            if command.lower() in self.commands:
                self.commands[command.lower()]()
            else:
                print("Unknown command. Type 'help' to see all commands.")

    def create_block(self):
        exit()

    def show_nodes(self):
        exit()

    def help(self):
        print("Available commands: ")
        for command in self.commands:
            print(f"{command}")
