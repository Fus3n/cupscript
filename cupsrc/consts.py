import string
import os

#######################################
# CONSTANTS
#######################################

DIGITS = string.digits
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

VERSION = '0.2.3'

STD_PATH = os.path.join(os.getcwd(), 'cupsrc/std')


#######################################
# TOKENS
#######################################

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_STRING = 'STRING'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_POW = 'POW'
TT_MOD = 'MOD'
TT_EQ = 'EQ'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_LSQUARE = 'LSQUARE'
TT_RSQUARE = 'RSQUARE'
TT_EE = 'EE'
TT_NE = 'NE'
TT_LT = 'LT'
TT_GT = 'GT'
TT_LTE = 'LTE'
TT_GTE = 'GTE'
TT_COMMA = 'COMMA'
TT_ARROW = 'ARROW'
TT_NEWLINE = 'NEWLINE'
TT_EOF = 'EOF'
TT_DOT = 'DOT'

KEYWORDS = [
    'var',
    'and',
    'or',
    'not',
    'if',
    'elif',
    'else',
    'for',
    'till',
    'do',
    'step',
    'while',
    'func',
    'then',
    'end',
    'return',
    'continue',
    'break',
    'import',
]

helpMsg = """help - [
            <builtin function>:
                help - print this message
                help_for(function_name) - print help for a function : args = function name -> string
                clear - clear the screen -> null
                exit - exit the script: -> null
                print(object) - print a string or any object : string, <- null
                sleep(seconds) - sleep for a number of seconds : int
                typeof(object) - get the type of the object: int, string, list, func, null, bool, File
                gets(string) - input / prompt for a value and return it : args = string
                is_num(object) - check if the value is a number : args = any type -> bool
                is_str(object) - check if the value is a string : args = any type -> bool
                is_list(object) - check if the value is a list -> bool : args = any type -> bool
                is_func(object) - check if the value is a function : args = any type -> bool
                append(string or list, object) - append a string to a string or any value to a list: args = object: string, value:any -> list
                extend(list, object) - extend a list with another list: args = list, list -> list
                replace(string, from, to) - replace a string with value: args = string, from, to -> string
                len(string or list) - get the length of a list or string: args = string, list -> int
                open_file(string) - open a file for reading or writing : open_file("file_name") returns File object to do file operations use read_stream/write_stream
                read_stream(File) - read string from entire file: args = File
                write_stream(File, string) - write string to file: args = File, string
                file_exists(File) - check if file exists: args = string -> bool
                split(string, sperator) - split a string into a list: args = string: string, seperator: string -> list
                tostr(object) - convert any value to a string: args = any type -> string
                toint(object, bool) - convert a String/Number value to an integer, takes value and boolean as to supress error if bad value: args = string, bool -> int
                tofloat(object, bool) - convert a String/Number value to a float, takes value and boolean as to supress error if bad value: args = string, bool -> float
                get_now - get the current time: -> int
                get_env(string) - get the value of an environment variable: string -> string
                set_env(string, string) - set an environment variable: string, string -> null
                get_dir - get the current working directory: -> string
                set_dir(string) - set the current working directory: string -> null
                random - get a random number: -> float
                rand_int(min, max) - get a random integer: -> int
                rand_seed(int) - set the random seed: int -> null
                rand_pick(list) - pick a random item from a list: list -> any
                run(string) - run a cupscript file: Run("file_name")
                error(message) - raise an runtime error: string -> null
            <builtin types>:
                int - integer : 123
                string - string : "hello"
                list - list : [string, int, list, func, null, bool]
                func - function:  lambdas,  func name(arg1, arg2) -> arg1 + arg2
                null - null: null = 0
                bool - boolean : true, false, 1, 0

            <lang rules>:
                get index element from list: list_name>index
                get index element from string: string_name>index

    ]
exit() - exit the shell 
"""



help_dict =  {
    'clear': {
        'args': '',
        'text': 'clear the screen',
        'returns': 'null'
    },
    'help': {
        'args': '',
        'text': 'print this message',
        'returns': 'string'
    },
    'help_for': {
        'args': 'function_name',
        'text': 'print help for a function',
        'returns': 'string'
    },
    'split': {
        'args': 'string, separator',
        'text': 'split a string into a list',
        'returns': 'list'
    },
    'exit': {
        'args': '',
        'text': 'exit the script',
        'returns': 'null'
    },
    'print': {
        'args': 'string/object',
        'text': 'print a string or any object',
        'returns': 'string'
    },
    'sleep': {
        'args': 'int',
        'text': 'sleep for a number of seconds',
        'returns': 'null'
    },
    'typeof': {
        'args': 'any type',
        'text': 'get the type of the object',
        'returns': 'string'
    },
    'gets': {
        'args': 'string',
        'text': 'input / prompt for a value and return it',
        'returns': 'string'
    },
    'is_num': {
        'args': 'any type',
        'text': 'check if the value is a number object',
        'returns': 'bool'
    },
    'is_str': {
        'args': 'any type',
        'text': 'check if the value is a string object',
        'returns': 'bool'
    },
    'is_list': {
        'args': 'any type',
        'text': 'check if the value is a list object',
        'returns': 'bool'
    },
    'is_func': {
        'args': 'any type',
        'text': 'check if the value is a function object',
        'returns': 'bool'
    },
    'append': {
        'args': 'string, string/list',
        'text': 'append a string to a string or any value to a list',
        'returns': 'null'
    },
    'extend': {
        'args': 'list, list',
        'text': 'extend a list with another list',
        'returns': 'null'
    },
    'len': {
        'args': 'list/string',
        'text': 'get the length of a list or string',
        'returns': 'int'
    },
    'replace': {
        "args": "string, from, to",
        "text": "replace a string with value: args = string, from, to -> string",
        "returns": "string"
    },
    'open_file': {
        'args': 'string',
        'text': 'open a file for reading or writing to do file operations use read_stream/write_stream',
        'returns': 'File'
    },
    'read_stream': {
        'args': 'File',
        'text': 'read string from entire file',
        'returns': 'string'
    },
    'write_stream': {
        'args': 'File, string',
        'text': 'write string to file',
        'returns': 'null'
    },
    'file_exists': {
        'args': 'string',
        'text': 'check if file exists',
        'returns': 'bool'
    },
    'sleep': {
        'args': 'int',
        'text': 'sleep for a number of seconds',
        'returns': 'null'
    },
    'tostr': {
        'args': 'any type',
        'text': 'convert any value to a string',
        'returns': 'string'
    },
    'toint': {
        'args': 'any type',
        'text': 'convert a String/Number value to an integer',
        'returns': 'int'
    },
    'get_now': {
        'args': '',
        'text': 'get the current time',
        'returns': 'int'
    },
    'get_env': {
        'args': 'string',
        'text': 'get the value of an environment variable',
        'returns': 'string'
    },
    'set_env': {
        'args': 'string, string',
        'text': 'set an environment variable',
        'returns': 'null'
    },
    'get_dir': {
        'args': '',
        'text': 'get the current working directory',
        'returns': 'string'
    },
    'set_dir': {
        'args': 'string',
        'text': 'set the current working directory',
        'returns': 'null'
    },
    'random': {
        'args': '',
        'text': 'get a random number',
        'returns': 'int'
    },
    'rand_int': {
        'args': 'min, max',
        'text': 'get a random integer',
        'returns': 'int'
    },
    'rand_seed': {
        'args': 'int',
        'text': 'set the random seed',
        'returns': 'null'
    },
    'rand_pick': {
        'args': 'list',
        'text': 'pick a random item from a list',
        'returns': 'any'
    },
    'join': {
        'args': 'string, list',
        'text': 'join a list of strings into a string',
        'returns': 'string'
    },
    'run': {
        'args': 'string',
        'text': 'run a cupscript file',
        'returns': 'null'
    },
    "error": {
        'args': 'string',
        'text': 'raise an runtime error with message',
        'returns': 'null'
    },
    '<builtin types>': {
        'int': 'integer',
        'string': 'string',
        'list': 'list',
        'func': 'function',
        'null': 'null',
        'bool': 'boolean'
    }
}

