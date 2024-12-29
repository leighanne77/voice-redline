from babel.messages.frontend import CommandLineInterface

def main():
    CommandLineInterface().run([
        'pybabel', 'extract',
        '-F', 'babel.cfg',
        '-o', 'translations/messages.pot',
        '.'
    ])
    
    # Initialize translation catalogs
    for lang in ['en', 'es']:
        CommandLineInterface().run([
            'pybabel', 'init',
            '-i', 'translations/messages.pot',
            '-d', 'translations',
            '-l', lang
        ])

if __name__ == '__main__':
    main() 