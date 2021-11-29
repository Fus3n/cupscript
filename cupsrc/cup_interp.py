

#######################################
# Imports
#######################################

import os
import time
import random

from .consts import *
from .error import RTError, InvalidSyntaxError, KeyboardInterruptError, position_start, position_end
from .cup_nodes import *
from .cup_types import *
from .cup_lex import Lexer, RTResult
from .cup_types import *



class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, should_auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return

    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()

        res.register(self.check_and_populate_args(
            self.arg_names, args, exec_ctx))
        if res.should_return():
            return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.should_return() and res.func_return_value == None:
            return res

        ret_value = (
            value if self.should_auto_return else None) or res.func_return_value or Null.null
        return res.success(ret_value)

    def copy(self):
        copy = Function(self.name, self.body_node,
                        self.arg_names, self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def type(self):
        return '<function>'

    def __repr__(self):
        return f"<function {self.name}>"




class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(
            method.arg_names, args, exec_ctx))
        if res.should_return():
            return res

        return_value = res.register(method(exec_ctx))
        if res.should_return():
            return res
        return res.success(return_value)

    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"

    ###############- builtin funcitons -#####################

    def execute_print(self, exec_ctx):
        print(str(exec_ctx.symbol_table.get('value')))
        return RTResult().success(Null.null)
    execute_print.arg_names = ['value']

    def execute_print_ret(self, exec_ctx):
        return RTResult().success(String(str(exec_ctx.symbol_table.get('value'))))
    execute_print_ret.arg_names = ['value']

    def execute_input(self, exec_ctx):
        prompt = exec_ctx.symbol_table.get('prompt')
        text = input(prompt)
        return RTResult().success(String(text))
    execute_input.arg_names = ["prompt"]

    def execute_clear(self, exec_ctx):
        os.system('cls' if os.name == 'nt' else 'cls')
        return RTResult().success(Null.null)
    execute_clear.arg_names = []

    def execute_type_of(self, exec_ctx):
        data = exec_ctx.symbol_table.get('value')
        return RTResult().success(String(data.type()))
    execute_type_of.arg_names = ['value']

    def execute_is_number(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_number.arg_names = ["value"]

    def execute_is_string(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_string.arg_names = ["value"]

    def execute_is_list(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_list.arg_names = ["value"]

    def execute_is_function(self, exec_ctx):
        is_number = isinstance(
            exec_ctx.symbol_table.get("value"), BaseFunction)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_function.arg_names = ["value"]

    def execute_tostr(self, exec_ctx):
        return RTResult().success(String(str(exec_ctx.symbol_table.get("value"))))
    execute_tostr.arg_names = ["value"]

    def execute_append(self, exec_ctx):
        # this works for list and strings
        obj_ = exec_ctx.symbol_table.get("object")
        value = exec_ctx.symbol_table.get("value")

        if isinstance(obj_, List):
            obj_.elements.append(value)
            return RTResult().success(value)
        elif isinstance(obj_, String):
            return RTResult().success(String(obj_.value + value.value))
        else:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Invalid argument for 'append'",
                exec_ctx))
    execute_append.arg_names = ["object", "value"]


    def execute_pop(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument of 'pop' must be list",
                exec_ctx
            ))

        if not isinstance(index, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument of 'pop' must be number",
                exec_ctx
            ))

        try:
            element = list_.elements.pop(index.value)
        except:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                'Element at this index could not be removed from list because index is out of bounds',
                exec_ctx
            ))
        return RTResult().success(element)
    execute_pop.arg_names = ["list", "index"]

    def execute_extend(self, exec_ctx):
        listA = exec_ctx.symbol_table.get("listA")
        listB = exec_ctx.symbol_table.get("listB")

        if not isinstance(listA, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument of 'extend' must be list",
                exec_ctx
            ))

        if not isinstance(listB, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument of 'extend' must be list",
                exec_ctx
            ))

        listA.elements.extend(listB.elements)
        return RTResult().success(Null.null)
    execute_extend.arg_names = ["listA", "listB"]

    def execute_len(self, exec_ctx):
        value_ = exec_ctx.symbol_table.get("value")

        if isinstance(value_, List):
            return RTResult().success(Number(len(value_.elements)))
        elif isinstance(value_, String):
            return RTResult().success(Number(len(value_.value)))
        else:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument for 'len' must be list or string",
                exec_ctx
            ))
    execute_len.arg_names = ["value"]

    def execute_run(self, exec_ctx):
        fn = exec_ctx.symbol_table.get("fn")

        if not isinstance(fn, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be string",
                exec_ctx
            ))

        fn = fn.value

        try:
            with open(fn, "r") as f:
                script = f.read()
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to load script \"{fn}\"\n" + str(e),
                exec_ctx
            ))

        _, error = run(fn, script)

        if error:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to finish executing script \"{fn}\"\n" +
                str(error),
                exec_ctx
            ))

        return RTResult().success(Null.null)
    execute_run.arg_names = ["fn"]

    def execute_sleep(self, exec_ctx):
        seconds = exec_ctx.symbol_table.get("seconds")

        if not isinstance(seconds, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument for 'sleep' must be a number",
                exec_ctx
            ))

        time.sleep(seconds.value)
        return RTResult().success(Null.null)
    execute_sleep.arg_names = ["seconds"]

    def execute_exit(self, exec_ctx):
        exit(0)
    execute_exit.arg_names = []

    def execute_open_stream(self, exec_ctx):
        file_path = exec_ctx.symbol_table.get("file_path")

        if not isinstance(file_path, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument for 'open_stream' must be a string",
                exec_ctx
            ))

        try:
            file_name = os.path.splitext(file_path.value)[0]
            return RTResult().success(File(file_name, file_path.value))    
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to open file \"{file_path.value}\"\n" + str(e),
                exec_ctx
            ))
    execute_open_stream.arg_names = ["file_path"]

    def execute_read_stream(self, exec_ctx):
        file = exec_ctx.symbol_table.get("file")

        if not isinstance(file, File):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument for 'read_stream' must be a file",
                exec_ctx
            ))

        try:
            with open(file.path, "r") as f:
                return RTResult().success(String(f.read()))
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to read file \"{file.path}\"\n" + str(e),
                exec_ctx
            ))
    execute_read_stream.arg_names = ["file"]

    def execute_write_stream(self, exec_ctx):
        file = exec_ctx.symbol_table.get("file")
        text = exec_ctx.symbol_table.get("text")

        if not isinstance(file, File):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument for 'write_stream' must be a file",
                exec_ctx
            ))

        if not isinstance(text, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument for 'write_stream' must be a string",
                exec_ctx
            ))

        try:
            with open(file.path, "a") as f:
                f.write(text.value)
            return RTResult().success(Number.null)
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to write to file \"{file.path}\"\n" + str(e),
                exec_ctx
            ))
    execute_write_stream.arg_names = ["file", "text"]

    def execute_file_exists(self, exec_ctx):
        file_path = exec_ctx.symbol_table.get("file_path")

        if isinstance(file_path, String):
            file_path = file_path.value

        elif isinstance(file_path, File):
            file_path = file_path.path
        
        else:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument for 'file_exists' must be a string or file",
                exec_ctx
            ))
            
        try:
            return RTResult().success(Number.true if os.path.exists(file_path) else Number.false)
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to check if file exists \"{file_path}\"\n" + str(e),
                exec_ctx
            ))
    execute_file_exists.arg_names = ["file_path"]

    def execute_get_now(self, exec_ctx):
        return RTResult().success(Number(time.time()))
    execute_get_now.arg_names = []

    def execute_get_env(self, exec_ctx):
        name = exec_ctx.symbol_table.get("name")

        if not isinstance(name, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument for 'get_env' must be a string",
                exec_ctx
            ))

        value = os.getenv(name.value)

        if value is None:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Environment variable '{name.value}' not found",
                exec_ctx
            ))

        return RTResult().success(String(value))
    execute_get_env.arg_names = ["name"]

    def execute_set_env(self, exec_ctx):
        name = exec_ctx.symbol_table.get("name")
        value = exec_ctx.symbol_table.get("value")

        if not isinstance(name, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument for 'set_env' must be a string",
                exec_ctx
            ))

        if not isinstance(value, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument for 'set_env' must be a string",
                exec_ctx
            ))

        try:
            os.environ[name.value] = value.value
            return RTResult().success(Null.null)
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to set environment variable '{name.value}'\n" + str(e),
                exec_ctx
            ))
    execute_set_env.arg_names = ["name", "value"]

    def execute_get_dir(self, exec_ctx):
        try:
            return RTResult().success(String(os.getcwd()))
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to get current directory\n" + str(e),
                exec_ctx
            ))
    execute_get_dir.arg_names = []

    def execute_set_dir(self, exec_ctx):
        name = exec_ctx.symbol_table.get("name")

        if not isinstance(name, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument for 'set_dir' must be a string",
                exec_ctx
            ))

        try:
            os.chdir(name.value)
            return RTResult().success(Null.null)
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to set current directory to '{name.value}'\n" + str(e),
                exec_ctx
            ))
    execute_set_dir.arg_names = ["name"]

    def execute_random(self, exec_ctx):
        return RTResult().success(Number(random.random()))
    execute_random.arg_names = []

    def execute_rand_int(self, exec_ctx):
        min = exec_ctx.symbol_table.get("min")
        max = exec_ctx.symbol_table.get("max")

        if not isinstance(min, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument for 'rand_int' must be a number",
                exec_ctx
            ))

        if not isinstance(max, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument for 'rand_int' must be a number",
                exec_ctx
            ))

        return RTResult().success(Number(random.randint(min.value, max.value)))
    execute_rand_int.arg_names = ["min", "max"]

    def execute_rand_seed(self, exec_ctx):
        seed = exec_ctx.symbol_table.get("seed")

        if not isinstance(seed, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument for 'rand_seed' must be a number",
                exec_ctx
            ))

        random.seed(seed.value)
        return RTResult().success(Null.null)
    execute_rand_seed.arg_names = ["seed"]

    def execute_rand_pick(self, exec_ctx):
        arr = exec_ctx.symbol_table.get("arr")

        if not isinstance(arr, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument for 'rand_pick' must be an List",
                exec_ctx
            ))

        if len(arr.elements) == 0:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Array passed to 'rand_pick' is empty",
                exec_ctx
            ))

        return RTResult().success(arr.elements[random.randrange(0, len(arr.elements) - 1)])
    execute_rand_pick.arg_names = ["arr"]

    def execute_toint(self, exec_ctx):
        value          = exec_ctx.symbol_table.get("value")
        supress_error  = exec_ctx.symbol_table.get("supress_error")

        if not isinstance(supress_error, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument for 'toint' must be a number",
                exec_ctx
            ))
        
        if supress_error.value == 1:
            supress_error = True
        elif supress_error.value == 0:
            supress_error = False
        else:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument for 'toint' must be a boolean",
                exec_ctx
            ))

        if isinstance(value, Number):
            return RTResult().success(Number(int(value.value)))
        elif isinstance(value, String):
            try:
                return RTResult().success(Number(int(value.value)))
            except ValueError:
                if supress_error:
                    return RTResult().success(Number.null)
                else:
                    return RTResult().failure(RTError(
                        self.pos_start, self.pos_end,
                        f"Failed to convert '{value.value}' of type '{value.type()}' to integer",
                        exec_ctx
                    ))
        else:
            if supress_error:
                return RTResult().success(Number.null)
            else:
                return RTResult().failure(RTError(
                    self.pos_start, self.pos_end,
                    f"Failed to convert value of type '{value.type()}' to integer",
                    exec_ctx
                ))
    execute_toint.arg_names = ['value', 'supress_error']

    def execute_help(self, exec_ctx):
        helpMsg = """help - [
            <builtin function>:
                clear - clear the screen -> null
                exit - exit the script: -> null
                print - print a string or any object : string, <- null
                sleep - sleep for a number of seconds : int
                typeof - get the type of the object: int, string, list, func, null, bool, File
                sets - print but also returns the value: sets("hello") -> "hello"
                gets - input / prompt for a value and return it : args = string
                is_num - check if the value is a number : args = any type -> bool
                is_string - check if the value is a string : args = any type -> bool
                is_list - check if the value is a list -> bool : args = any type -> bool
                is_func - check if the value is a function : args = any type -> bool
                append - append a string to a string or any value to a list
                remove - remove an item from a list
                extend - extend a list with another list 
                len - get the length of a list or string
                File - open a file for reading or writing : File("file_name") to do file operations i.e. read_stream/write_stream
                read_stream - read string from entire file: args = File
                write_stream - write string to file: args = File, string
                file_exists - check if file exists
                sleep - sleep for a number of seconds
                tostr - convert any value to a string
                toint - convert a String/Number value to an integer
                get_now - get the current time: -> int
                get_env - get the value of an environment variable: string -> string
                set_env - set an environment variable: string, string -> null
                get_dir - get the current working directory: -> string
                set_dir - set the current working directory: string -> null
                random - get a random number: -> int
                rand_int - get a random integer: -> int
                rand_seed - set the random seed: int -> null
                rand_pick - pick a random item from a list: list -> any
                rand_range - get a random number between two values: int, int -> int
                Run - run a cupscript file: Run("file_name")
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

        return RTResult().success(String(helpMsg))
    execute_help.arg_names = []

    def execute_sys(self, exec_ctx):
        command = exec_ctx.symbol_table.get("command")

        if not isinstance(command, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument for 'sys' must be a string",
                exec_ctx
            ))
        
        try:
            os.system(command.value)
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to execute '{command.value}'\n" + str(e),
                exec_ctx
            ))
        
        return RTResult().success(Null.null)
    execute_sys.arg_names = ["command"]

    def execute_version(self, exec_ctx):
        return RTResult().success(String(VERSION))
    execute_version.arg_names = []


#######################################
# SETUP VARIABLE FOR ALL BUILT IN FUNCTION
#######################################

BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.print_ret = BuiltInFunction("print_ret")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.clear = BuiltInFunction("clear")
BuiltInFunction.is_number = BuiltInFunction("is_number")
BuiltInFunction.is_string = BuiltInFunction("is_string")
BuiltInFunction.is_list = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append = BuiltInFunction("append")
BuiltInFunction.pop = BuiltInFunction("pop")
BuiltInFunction.extend = BuiltInFunction("extend")
BuiltInFunction.len = BuiltInFunction("len")
BuiltInFunction.run = BuiltInFunction("run")
BuiltInFunction.type_of = BuiltInFunction("type_of")
BuiltInFunction.exit = BuiltInFunction("exit")
BuiltInFunction.sleep = BuiltInFunction("sleep")
BuiltInFunction.tostr = BuiltInFunction("tostr")
BuiltInFunction.toint = BuiltInFunction("toint")
BuiltInFunction.open_stream = BuiltInFunction("open_stream")
BuiltInFunction.read_stream = BuiltInFunction("read_stream")
BuiltInFunction.write_stream = BuiltInFunction("write_stream")
BuiltInFunction.file_exists = BuiltInFunction("file_exists")
BuiltInFunction.get_now = BuiltInFunction("get_now")
BuiltInFunction.get_env = BuiltInFunction("get_env")
BuiltInFunction.set_env = BuiltInFunction("set_env")
BuiltInFunction.get_dir = BuiltInFunction("get_dir")
BuiltInFunction.set_dir = BuiltInFunction("set_dir")
BuiltInFunction.random = BuiltInFunction("random")
BuiltInFunction.rand_int = BuiltInFunction("rand_int")
BuiltInFunction.rand_seed = BuiltInFunction("rand_seed")
BuiltInFunction.rand_pick = BuiltInFunction("rand_pick")
BuiltInFunction.help = BuiltInFunction("help")
BuiltInFunction.sys = BuiltInFunction("sys")
BuiltInFunction.version = BuiltInFunction("version")



#######################################
# PARSE RESULT
#######################################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self

#######################################
# PARSER
#######################################


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        self.update_current_tok()
        return self.current_tok

    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok

    def update_current_tok(self):
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

    def parse(self):
        res = self.statements()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Token cannot appear after previous tokens"
            ))
        return res

    ###################################

    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

        statement = res.register(self.statement())
        if res.error:
            return res
        statements.append(statement)

        more_statements = True

        while True:
            newline_count = 0
            while self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False

            if not more_statements:
                break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(
            statements,
            pos_start,
            self.current_tok.pos_end.copy()
        ))

    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.matches(TT_KEYWORD, 'return'):
            res.register_advancement()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))

        if self.current_tok.matches(TT_KEYWORD, 'continue'):
            res.register_advancement()
            self.advance()
            return res.success(ContinueNode(pos_start, self.current_tok.pos_start.copy()))

        if self.current_tok.matches(TT_KEYWORD, 'break'):
            res.register_advancement()
            self.advance()
            return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))

        expr = res.register(self.expr())
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'return', 'continue', 'break', 'var', 'if', 'for', 'while', 'func', int, float, identifier, '+', '-', '(', '[' or 'not'"
            ))
        return res.success(expr)

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'var'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier"
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '='"
                ))

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(
            self.comp_expr, ((TT_KEYWORD, 'and'), (TT_KEYWORD, 'or'))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'var', 'if', 'for', 'while', 'func', int, float, identifier, '+', '-', '(', '[' or 'not'"
            ))

        return res.success(node)

    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'not'):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.bin_op(
            self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected int, float, identifier, '+', '-', '(', '[', 'if', 'for', 'while', 'func' or 'not'"
            ))

        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_MOD))

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def power(self):
        return self.bin_op(self.call, (TT_POW, ), self.factor)

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error:
            return res

        if self.current_tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ')', 'var', 'if', 'for', 'while', 'func', int, float, identifier, '+', '-', '(', '[' or 'not'"
                    ))

                while self.current_tok.type == TT_COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error:
                        return res

                if self.current_tok.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected ',' or ')'"
                    ))

                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))

        elif tok.type == TT_LSQUARE:
            list_expr = res.register(self.list_expr())
            if res.error:
                return res
            return res.success(list_expr)

        elif tok.matches(TT_KEYWORD, 'if'):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(if_expr)

        elif tok.matches(TT_KEYWORD, 'for'):
            for_expr = res.register(self.for_expr())
            if res.error:
                return res
            return res.success(for_expr)

        elif tok.matches(TT_KEYWORD, 'while'):
            while_expr = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(while_expr)

        elif tok.matches(TT_KEYWORD, 'func'):
            func_def = res.register(self.func_def())
            if res.error:
                return res
            return res.success(func_def)

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int, float, identifier, '+', '-', '(', '[', IF', 'for', 'while', 'func'"
        ))

    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '['"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_RSQUARE:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']', 'var', 'if', 'for', 'while', 'func', int, float, identifier, '+', '-', '(', '[' or 'not'"
                ))

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                element_nodes.append(res.register(self.expr()))
                if res.error:
                    return res

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ']'"
                ))

            res.register_advancement()
            self.advance()

        return res.success(ListNode(
            element_nodes,
            pos_start,
            self.current_tok.pos_end.copy()
        ))

    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases('if'))
        if res.error:
            return res
        cases, else_case = all_cases
        return res.success(IfNode(cases, else_case))

    def if_expr_b(self):
        return self.if_expr_cases('elseif')

    def if_expr_c(self):
        res = ParseResult()
        else_case = None

        if self.current_tok.matches(TT_KEYWORD, 'else'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()

                statements = res.register(self.statements())
                if res.error:
                    return res
                else_case = (statements, True)

                if self.current_tok.matches(TT_KEYWORD, 'end'):
                    res.register_advancement()
                    self.advance()
                else:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected 'end'"
                    ))
            else:
                expr = res.register(self.statement())
                if res.error:
                    return res
                else_case = (expr, False)

        return res.success(else_case)

    def if_expr_b_or_c(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.current_tok.matches(TT_KEYWORD, 'elseif'):
            all_cases = res.register(self.if_expr_b())
            if res.error:
                return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.if_expr_c())
            if res.error:
                return res

        return res.success((cases, else_case))

    def if_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TT_KEYWORD, case_keyword):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '{case_keyword}'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, 'then'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'then'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            statements = res.register(self.statements())
            if res.error:
                return res
            cases.append((condition, statements, True))

            if self.current_tok.matches(TT_KEYWORD, 'end'):
                res.register_advancement()
                self.advance()
            else:
                all_cases = res.register(self.if_expr_b_or_c())
                if res.error:
                    return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.statement())
            if res.error:
                return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.if_expr_b_or_c())
            if res.error:
                return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return res.success((cases, else_case))

    def for_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'for'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'for'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected identifier"
            ))

        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '='"
            ))

        res.register_advancement()
        self.advance()

        start_value = res.register(self.expr())
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, 'till'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'till'"
            ))

        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error:
            return res

        if self.current_tok.matches(TT_KEYWORD, 'step'):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error:
                return res
        else:
            step_value = None

        if not self.current_tok.matches(TT_KEYWORD, 'then'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'then'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res

            if not self.current_tok.matches(TT_KEYWORD, 'end'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'end'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))

        body = res.register(self.statement())
        if res.error:
            return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body, False))

    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'while'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'while'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, 'then'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'then'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res

            if not self.current_tok.matches(TT_KEYWORD, 'end'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'end'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(WhileNode(condition, body, True))

        body = res.register(self.statement())
        if res.error:
            return res

        return res.success(WhileNode(condition, body, False))

    def func_def(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'func'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'func'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected '('"
                ))
        else:
            var_name_tok = None
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier or '('"
                ))

        res.register_advancement()
        self.advance()
        arg_name_toks = []

        if self.current_tok.type == TT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected identifier"
                    ))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ')'"
                ))
        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier or ')'"
                ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_ARROW:
            res.register_advancement()
            self.advance()

            body = res.register(self.expr())
            if res.error:
                return res

            return res.success(FuncDefNode(
                var_name_tok,
                arg_name_toks,
                body,
                True
            ))

        if self.current_tok.type != TT_NEWLINE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '->' or NEWLINE"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, 'end'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'end'"
            ))

        res.register_advancement()
        self.advance()

        return res.success(FuncDefNode(
            var_name_tok,
            arg_name_toks,
            body,
            False
        ))

    ###################################

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)



#######################
# Interpreter
#######################
class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ###################################

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(
                context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_StringNode(self, node, context):
        return RTResult().success(
            String(node.tok.value).set_context(
                context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return():
                return res

        return res.success(
            List(elements).set_context(context).set_pos(
                node.pos_start, node.pos_end)
        )

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return():
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.should_return():
            return res
        right = res.register(self.visit(node.right_node, context))
        if res.should_return():
            return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == TT_MOD:
            result, error = left.moduled_by(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TT_KEYWORD, 'and'):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, 'or'):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.should_return():
            return res

        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.matches(TT_KEYWORD, 'not'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node, context):
        res = RTResult()

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return():
                return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.should_return():
                    return res
                return res.success(Null.null if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            expr_value = res.register(self.visit(expr, context))
            if res.should_return():
                return res
            return res.success(Null.null if should_return_null else expr_value)

        return res.success(Null.null)

    def visit_ForNode(self, node, context):
        res = RTResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.should_return():
            return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.should_return():
            return res

        if node.step_value_node:
            step_value = res.register(
                self.visit(node.step_value_node, context))
            if res.should_return():
                return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            def condition(): return i < end_value.value
        else:
            def condition(): return i > end_value.value

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False:
                return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Null.null if node.should_return_null else
            List(elements).set_context(context).set_pos(
                node.pos_start, node.pos_end)
        )

    def visit_WhileNode(self, node, context):
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.should_return():
                return res

            if not condition.is_true():
                break

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False:
                return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Null.null if node.should_return_null else
            List(elements).set_context(context).set_pos(
                node.pos_start, node.pos_end)
        )

    def visit_FuncDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(
            context).set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return():
            return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return():
                return res

        return_value = res.register(value_to_call.execute(args))
        if res.should_return():
            return res
        return_value = return_value.copy().set_pos(
            node.pos_start, node.pos_end).set_context(context)

        return res.success(return_value)

    def visit_ReturnNode(self, node, context):
        res = RTResult()

        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return():
                return res
        else:
            value = Null.null

        return res.success_return(value)

    def visit_ContinueNode(self, node, context):
        return RTResult().success_continue()

    def visit_BreakNode(self, node, context):
        return RTResult().success_break()




#######################################
# SETUP GLOBAL VARIABLES FOR PRE BUILT FUNCTIONS / VARIABLES
#######################################

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null)
global_symbol_table.set("false", Number.false)
global_symbol_table.set("true", Number.true)
global_symbol_table.set("function", String("<function>"))
global_symbol_table.set("list", String("<list>"))
global_symbol_table.set("str", String("<str>"))
global_symbol_table.set("int", String("<int>"))
global_symbol_table.set("float", String("<float>"))
global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("sets", BuiltInFunction.print_ret)
global_symbol_table.set("gets", BuiltInFunction.input)
global_symbol_table.set("clear", BuiltInFunction.clear) 
global_symbol_table.set("is_num", BuiltInFunction.is_number)
global_symbol_table.set("is_str", BuiltInFunction.is_string)
global_symbol_table.set("is_list", BuiltInFunction.is_list)
global_symbol_table.set("is_func", BuiltInFunction.is_function)
global_symbol_table.set("append", BuiltInFunction.append)
global_symbol_table.set("pop", BuiltInFunction.pop)
global_symbol_table.set("extend", BuiltInFunction.extend)
global_symbol_table.set("len", BuiltInFunction.len)
global_symbol_table.set("Run", BuiltInFunction.run)
global_symbol_table.set("typeof", BuiltInFunction.type_of)
global_symbol_table.set("sleep", BuiltInFunction.sleep)
global_symbol_table.set("exit", BuiltInFunction.exit)
global_symbol_table.set("tostr", BuiltInFunction.tostr)
global_symbol_table.set("toint", BuiltInFunction.toint)
global_symbol_table.set("File", BuiltInFunction.open_stream)
global_symbol_table.set("read_stream", BuiltInFunction.read_stream)
global_symbol_table.set("write_stream", BuiltInFunction.write_stream)
global_symbol_table.set("file_exists", BuiltInFunction.file_exists)
global_symbol_table.set("get_now", BuiltInFunction.get_now)
global_symbol_table.set("get_env", BuiltInFunction.get_env)
global_symbol_table.set("set_env", BuiltInFunction.set_env)
global_symbol_table.set("get_dir", BuiltInFunction.get_dir)
global_symbol_table.set("set_dir", BuiltInFunction.set_dir)
global_symbol_table.set("random", BuiltInFunction.random)
global_symbol_table.set("rand_int", BuiltInFunction.rand_int)
global_symbol_table.set("rand_seed", BuiltInFunction.rand_seed)
global_symbol_table.set("rand_pick", BuiltInFunction.rand_pick)
global_symbol_table.set("help", BuiltInFunction.help)
global_symbol_table.set("sys", BuiltInFunction.sys)
global_symbol_table.set("version", BuiltInFunction.version)

#######################################
# RUN
#######################################

def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    result = None
    # Generate AST
    context = None

    try:
        parser = Parser(tokens)
        ast = parser.parse()
        if ast.error:
            return None, ast.error

        # Run program
        interpreter = Interpreter()
        context = Context('<main>')
        context.symbol_table = global_symbol_table
        result = interpreter.visit(ast.node, context)
        result.value = '' if str(result.value) == 'null' else result.value

        return result.value, result.error
    except KeyboardInterrupt:
        err = KeyboardInterruptError(
                position_start, position_end,
                "Execution interrupted"
            )
        return None, err
