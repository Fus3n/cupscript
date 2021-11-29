
#######################################
# Object
#######################################
from .cup_lex import RTResult
from .error import RTError


#######################################
# CONTEXT
#######################################


class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

#######################################
# SYMBOL TABLE
#######################################


class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]




class Object:
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def type(self):
        return 'Object'

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)

    def moduled_by(self, other):
        return None, self.illegal_operation(other)

    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self, other):
        return None, self.illegal_operation(other)

    def execute(self, args):
        return RTResult().failure(self.illegal_operation())

    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False

    def illegal_operation(self, other=None, error_str=None):
        if not other:
            other = self
        return RTError(
            self.pos_start, other.pos_end,
            f'Illegal operation -> {error_str or "unknown"}',
            self.context
        )


class BaseFunction(Object):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names, args):
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(arg_names)} too many args passed into {self}",
                self.context
            ))

        if len(args) < len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(arg_names) - len(args)} too few args passed into {self}",
                self.context
            ))

        return res.success(None)

    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return():
            return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)

class Null(Object):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        return other, None

    def copy(self):
        copy = Null(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return False

    def __str__(self):
        return 'null'
    
    def __repr__(self):
        return str(self.value)
    
    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

Null.null = Null('null')

class Number(Object):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other, f"Can't add a number to a type of '{other.type()}'")

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other ,f"Can't subtract a number from a type of '{other.type()}'")

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other, f"Can't multiply a number by a type of '{other.type()}'")

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )

            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other, f"Can't divide a number by a type of '{other.type()}'")

    def moduled_by(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other, f"Can't mod a number by a type of '{other.type()}'")

    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other, f"Can't power a number by a type of '{other.type()}'")

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other, f"Can't compare a number to a type of '{other.type()}'")

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other ,f"Can't compare a number to a type of '{other.type()}'")

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other, f"Can't compare a number to a type of '{other.type()}'")

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other, f"Can't compare a number to a type of '{other.type()}'")

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other, f"Can't compare a number to a type of '{other.type()}'")

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other ,f"Can't compare a number to a type of '{other.type()}'")

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other, f"Can't compare a number to a type of '{other.type()}'")

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other, f"Can't compare a number to a type of '{other.type()}'")

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    
    def type(self):
        if self.value % 1 == 0:
            return '<int>'
        else:
            return '<float>'

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)


class String(Object):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other, f"Can't add a string to a type of '{other.type()}'")

    def multed_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other, f"Can't multiply a string by a type of '{other.type()}'")

    def get_comparison_eq(self, other):
        if isinstance(other, String):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other, f"Can't compare a string to a type of '{other.type()}'")

    def get_comparison_ne(self, other):
        if isinstance(other, String):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Object.illegal_operation(self, other, f"Can't compare a string to a type of '{other.type()}'")

    def get_comparison_gt(self, other):
        # this function gets the value of the string index passed if cant get then throw error
        if isinstance(other, Number):
            try:
                return String(self.value[other.value]).set_context(self.context), None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'String index out of bounds',
                    self.context
                )
        else:
            return None, Object.illegal_operation(self, other, f"Can't compare a string to a type of '{other.type()}'")


    def is_true(self):
        return len(self.value) > 0

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def type(self):
        return '<string>'

    def __str__(self):
        return self.value

    def __repr__(self):
        return_value = f'"{self.value}"'
        if return_value.endswith('""'):
            return_value = return_value[:-1]
        elif return_value.endswith("'\""):
            return_value = return_value[:-2]
        return return_value


class List(Object):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def subbed_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Element at this index could not be removed from list because index is out of bounds',
                    self.context
                )
        else:
            return None, Object.illegal_operation(self, other, f"Can't subtract a list by a type of '{other.type()}'")

    def multed_by(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Object.illegal_operation(self, other, f"Can't multiply a list by a type of '{other.type()}'")

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Element at this index could not be retrieved from list because index is out of bounds',
                    self.context
                )
        else:
            return None, Object.illegal_operation(self, other, "Index must be a number type")

    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def type(self):
        return '<list>'

    def __str__(self):
        return ", ".join([str(x) for x in self.elements])

    def __repr__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'



class File(Object):
    def __init__(self, name, path):
        super().__init__()
        self.name = name
        self.path = path

    def get_comparison_eq(self, other):
        if isinstance(other, File):
            return self.path == other.path, None
        else:
            return None, Object.illegal_operation(self, other, f"Can't compare a File to a type of '{other.type()}'")

    def copy(self):
        copy = File(self.name, self.path)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def type(self):
        return '<file>'

    def __repr__(self):
        return f"<file {self.name}>"
