class LogWriter:
    log_list = []
    save_file = "log.txt"

    @classmethod
    def clearlog(cls):
        with open(cls.save_file, 'w') as output:
            output.write(str("------new log") + '\n')

    @classmethod
    def log(cls, line):
        print(line)
        with open(cls.save_file, 'a') as output:
            output.write(str(line) + '\n')

    def __init__(self, save_file="log.txt"):
        with open(save_file, 'w') as output:
            for row in LogWriter.log_list:
                output.write(str(row) + '\n')

        print(f"log saved in {save_file}")

