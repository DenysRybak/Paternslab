class ConsoleOutputStrategy:
    print("Starting console output")
    def output(self, data):
        for line in data:
            print(line)
