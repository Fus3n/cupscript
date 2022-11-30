#######################################
# NODES
#######################################


class NumberNode:
    __slots__ = ['tok', 'pos_start', 'pos_end']

    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end


    def __repr__(self):
        return f"{self.tok}"


class StringNode:
    __slots__ = ['tok', 'pos_start', 'pos_end']

    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end


    def __repr__(self):
        return f"{self.tok}"


class ListNode:
    __slots__ = ['element_nodes', 'pos_start', 'pos_end']

    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end



class VarAccessNode:
    __slots__ = ['var_name_tok', 'pos_start', 'pos_end']

    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end



class VarAssignNode:
    __slots__ = ['var_name_tok', 'value_node', 'pos_start', 'pos_end']

    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end


class BinOpNode:
    __slots__ = ['left_node', 'op_tok', 'right_node', 'pos_start', 'pos_end']

    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end


    def __repr__(self):
        return f"({self.left_node}, {self.op_tok}, {self.right_node})"


class UnaryOpNode:
    __slots__ = ['op_tok', 'node', 'pos_start', 'pos_end']

    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end


    def __repr__(self):
        return f"({self.op_tok}, {self.node})"


class IfNode:
    __slots__ = ['cases', 'else_case', 'pos_start', 'pos_end']

    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1])[0].pos_end


class ForNode:
    __slots__ = ['var_name_tok', 'start_value_node', 'end_value_node', 'step_value_node', 'body_node', 'should_return_null', 'pos_start', 'pos_end']

    def __init__(
        self,
        var_name_tok,
        start_value_node,
        end_value_node,
        step_value_node,
        body_node,
        should_return_null,
    ):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end



class WhileNode:
    __slots__ = ['condition_node', 'body_node', 'should_return_null', 'pos_start', 'pos_end']

    def __init__(self, condition_node, body_node, should_return_null):
        self.condition_node = condition_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end



class FuncDefNode:
    __slots__ = ['var_name_tok', 'arg_name_toks', 'body_node', 'should_auto_return', 'pos_start', 'pos_end']

    def __init__(self, var_name_tok, arg_name_toks, body_node, should_auto_return):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node
        self.should_auto_return = should_auto_return

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end



class CallNode:
    __slots__ = ['node_to_call', 'arg_nodes', 'pos_start', 'pos_end']

    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end


class ReturnNode:
    __slots__ = ['node_to_return', 'pos_start', 'pos_end']

    def __init__(self, node_to_return, pos_start, pos_end):
        self.node_to_return = node_to_return

        self.pos_start = pos_start
        self.pos_end = pos_end



class ContinueNode:
    __slots__ = ['pos_start', 'pos_end']

    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end



class BreakNode:
    __slots__ = ['pos_start', 'pos_end']
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end


class AccessNode:
    def __init__(self, obj, index):
        self.obj = obj
        self.index = index    

class ImportNode:
    __slots__ = ['module_name_tok', 'file_path', 'pos_start', 'pos_end']

    def __init__(self, module_name_tok):
        self.module_name_tok = module_name_tok
        self.file_path = module_name_tok.value

        self.pos_start = self.module_name_tok.pos_start
        self.pos_end = self.module_name_tok.pos_end

