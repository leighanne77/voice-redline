from babel.messages.frontend import CommandLineInterface

def main():
    CommandLineInterface().run([
        'pybabel', 'compile',
        '-d', 'translations'
    ])

if __name__ == '__main__':
    main() 