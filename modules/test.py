from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

# 设置自动完成列表
words = ['apple', 'orange', 'banana', 'pear', 'grape']
word_completer = WordCompleter(words)

def main():
    session = PromptSession()

    while True:
        try:
            text = session.prompt('Enter some text: ', completer=word_completer)
            print('You entered:', text)

        except KeyboardInterrupt:  # 捕捉 Ctrl+C
            print('KeyboardInterrupt: Exiting...')
            break

if __name__ == '__main__':
    main()
