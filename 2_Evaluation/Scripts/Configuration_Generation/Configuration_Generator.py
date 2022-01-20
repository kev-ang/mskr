import getopt
import sys
from string import Template


def main(argv):
    if len(argv) != 8:
        print('-d: \t Path to database that should be used in the configuration')
        print('-n: \t Name of the final configuration file')
        print('-r: \t Path to rules that should be used in the configuration')
        print('-t: \t Path to configuration template')
        sys.exit()

    opts, args = getopt.getopt(argv, "d:n:r:t:")
    for opt, arg in opts:
        # Dataset that should be used for the current configuration
        if opt == '-d':
            database = arg
        # Name used for the final configuration file
        elif opt == '-n':
            filename = arg
        # Rules that should be used for the current configuration
        elif opt == '-r':
            rules = arg
        # Template that should be used
        elif opt == '-t':
            template = arg

    fillTemplate(template, database, rules, filename)


def fillTemplate(template, database, rules, filename):
    variables = {
        'database': database,
        'rules': rules
    }

    with open(template, 'r') as f:
        src = Template(f.read())
        result = src.substitute(variables)
        with open(filename, 'w') as out:
            out.write(result)
            out.close


if __name__ == '__main__':
    main(sys.argv[1:])
