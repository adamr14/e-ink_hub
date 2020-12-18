import os
import sys

def clear_message_file():
    with open('./data/message.txt', 'w') as outfile:
        outfile.write('')
        
def main():
    os.chdir(os.path.dirname(sys.argv[0]))
    clear_message_file()

if __name__ == '__main__':
    main()