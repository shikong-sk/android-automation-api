"""
脚本解析器模块

提供脚本的词法分析和语法分析功能，将脚本文本解析为抽象语法树(AST)。
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict, Union


class TokenType(Enum):
    """Token类型枚举"""

    # 命令关键字
    CLICK = auto()
    CLICK_TEXT = auto()
    CLICK_ID = auto()
    INPUT = auto()
    CLEAR = auto()
    SWIPE = auto()
    WAIT = auto()
    WAIT_ELEMENT = auto()
    WAIT_GONE = auto()
    BACK = auto()
    HOME = auto()
    MENU = auto()
    RECENT = auto()
    START_APP = auto()
    STOP_APP = auto()
    CLEAR_APP = auto()
    SCREEN_ON = auto()
    SCREEN_OFF = auto()
    UNLOCK = auto()
    SET = auto()
    GET_TEXT = auto()
    GET_INFO = auto()
    FIND_ELEMENT = auto()
    FIND_ELEMENTS = auto()
    DUMP_HIERARCHY = auto()
    EXISTS = auto()
    LOG = auto()
    SHELL = auto()

    # 人类模拟操作关键字
    HUMAN_CLICK = auto()
    HUMAN_DOUBLE_CLICK = auto()
    HUMAN_LONG_PRESS = auto()
    HUMAN_DRAG = auto()

    # 控制流关键字
    NOT = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    END = auto()
    LOOP = auto()
    WHILE = auto()
    TRY = auto()
    CATCH = auto()
    CALL = auto()
    BREAK = auto()
    CONTINUE = auto()

    # 选择器类型
    SELECTOR_ID = auto()
    SELECTOR_TEXT = auto()
    SELECTOR_XPATH = auto()
    SELECTOR_CLASS = auto()
    SELECTOR_COORDINATE = auto()

    # 选择器修饰符
    SELECTOR_PARENT = auto()
    SELECTOR_SIBLING = auto()
    SELECTOR_SIBLING_RELATION = auto()

    # 操作符和分隔符
    COLON = auto()
    COMMA = auto()
    LPAREN = auto()
    RPAREN = auto()
    EQUALS = auto()

    # 字面量
    STRING = auto()
    NUMBER = auto()
    IDENTIFIER = auto()

    # 特殊
    NEWLINE = auto()
    EOF = auto()
    COMMENT = auto()


@dataclass
class Token:
    """词法单元"""

    type: TokenType
    value: Any
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column})"


@dataclass
class ASTNode:
    """AST节点基类"""

    line: int = 0
    column: int = 0


@dataclass
class ConditionNode(ASTNode):
    """条件节点"""

    command: str = ""
    selector_type: Optional[str] = None
    selector_value: Optional[str] = None
    negated: bool = False
    args: List[Any] = field(default_factory=list)


@dataclass
class CommandNode(ASTNode):
    """命令节点"""

    command: str = ""
    args: List[Any] = field(default_factory=list)
    selector_type: Optional[str] = None
    selector_value: Optional[str] = None
    selector_modifiers: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SetNode(ASTNode):
    """变量赋值节点"""

    variable: str = ""
    value: Any = None
    command: Optional[str] = None
    command_args: List[Any] = field(default_factory=list)
    selector_type: Optional[str] = None
    selector_value: Optional[str] = None


@dataclass
class IfNode(ASTNode):
    """条件分支节点"""

    condition: Optional[ConditionNode] = None
    then_body: List[ASTNode] = field(default_factory=list)
    elif_branches: List[tuple] = field(default_factory=list)  # List of (condition, body)
    else_body: List[ASTNode] = field(default_factory=list)


@dataclass
class LoopNode(ASTNode):
    """循环节点"""

    count: int = 0
    variable: Optional[str] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class WhileNode(ASTNode):
    """While循环节点"""

    condition: Optional[ConditionNode] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class TryNode(ASTNode):
    """异常处理节点"""

    try_body: List[ASTNode] = field(default_factory=list)
    catch_body: List[ASTNode] = field(default_factory=list)


@dataclass
class CallNode(ASTNode):
    """函数调用节点"""

    function_name: str = ""
    args: List[Any] = field(default_factory=list)


@dataclass
class BreakNode(ASTNode):
    """Break节点"""

    pass


@dataclass
class ContinueNode(ASTNode):
    """Continue节点"""

    pass


class ScriptLexer:
    """词法分析器"""

    KEYWORDS: Dict[str, TokenType] = {
        "click": TokenType.CLICK,
        "click_text": TokenType.CLICK_TEXT,
        "click_id": TokenType.CLICK_ID,
        "input": TokenType.INPUT,
        "clear": TokenType.CLEAR,
        "swipe": TokenType.SWIPE,
        "wait": TokenType.WAIT,
        "wait_element": TokenType.WAIT_ELEMENT,
        "wait_gone": TokenType.WAIT_GONE,
        "back": TokenType.BACK,
        "home": TokenType.HOME,
        "menu": TokenType.MENU,
        "recent": TokenType.RECENT,
        "start_app": TokenType.START_APP,
        "stop_app": TokenType.STOP_APP,
        "clear_app": TokenType.CLEAR_APP,
        "screen_on": TokenType.SCREEN_ON,
        "screen_off": TokenType.SCREEN_OFF,
        "unlock": TokenType.UNLOCK,
        "set": TokenType.SET,
        "get_text": TokenType.GET_TEXT,
        "get_info": TokenType.GET_INFO,
        "find_element": TokenType.FIND_ELEMENT,
        "find_elements": TokenType.FIND_ELEMENTS,
        "dump_hierarchy": TokenType.DUMP_HIERARCHY,
        "exists": TokenType.EXISTS,
        "not": TokenType.NOT,
        "if": TokenType.IF,
        "elif": TokenType.ELIF,
        "else": TokenType.ELSE,
        "end": TokenType.END,
        "loop": TokenType.LOOP,
        "while": TokenType.WHILE,
        "try": TokenType.TRY,
        "catch": TokenType.CATCH,
        "call": TokenType.CALL,
        "log": TokenType.LOG,
        "shell": TokenType.SHELL,
        "break": TokenType.BREAK,
        "continue": TokenType.CONTINUE,
        # 人类模拟操作关键字
        "human_click": TokenType.HUMAN_CLICK,
        "human_double_click": TokenType.HUMAN_DOUBLE_CLICK,
        "human_long_press": TokenType.HUMAN_LONG_PRESS,
        "human_drag": TokenType.HUMAN_DRAG,
    }

    SELECTOR_KEYWORDS: Dict[str, TokenType] = {
        "id": TokenType.SELECTOR_ID,
        "text": TokenType.SELECTOR_TEXT,
        "xpath": TokenType.SELECTOR_XPATH,
        "class": TokenType.SELECTOR_CLASS,
        "coord": TokenType.SELECTOR_COORDINATE,
        "parent": TokenType.SELECTOR_PARENT,
        "sibling": TokenType.SELECTOR_SIBLING,
        "sibling_relation": TokenType.SELECTOR_SIBLING_RELATION,
    }

    MODIFIER_KEYWORDS: Dict[str, str] = {
        "parent": "parent",
        "parent_id": "parent_id",
        "parent_text": "parent_text",
        "parent_class": "parent_class",
        "sibling": "sibling",
        "sibling_id": "sibling_id",
        "sibling_text": "sibling_text",
        "sibling_class": "sibling_class",
        "sibling_relation": "sibling_relation",
        "offset_x": "offset_x",
        "offset_y": "offset_y",
        "offset": "offset",
    }

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def current_char(self) -> Optional[str]:
        """获取当前字符"""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]

    def peek_char(self, offset: int = 1) -> Optional[str]:
        """预览后续字符"""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]

    def advance(self) -> Optional[str]:
        """前进一个字符"""
        char = self.current_char()
        if char is not None:
            self.pos += 1
            if char == "\n":
                self.line += 1
                self.column = 1
            else:
                self.column += 1
        return char

    def skip_whitespace(self) -> None:
        """跳过空白字符（不包括换行）"""
        while self.current_char() is not None and self.current_char() in " \t\r":
            self.advance()

    def skip_comment(self) -> None:
        """跳过注释"""
        if self.current_char() == "#":
            while self.current_char() is not None and self.current_char() != "\n":
                self.advance()

    def read_string(self) -> str:
        """读取字符串"""
        quote_char = self.current_char()
        self.advance()  # 跳过开始引号

        result = []
        while self.current_char() is not None and self.current_char() != quote_char:
            if self.current_char() == "\\":
                self.advance()
                escape_char = self.current_char()
                if escape_char == "n":
                    result.append("\n")
                elif escape_char == "t":
                    result.append("\t")
                elif escape_char == "r":
                    result.append("\r")
                elif escape_char == "\\":
                    result.append("\\")
                elif escape_char == quote_char:
                    result.append(quote_char)
                else:
                    result.append(escape_char or "")
                self.advance()
            else:
                result.append(self.current_char())
                self.advance()

        if self.current_char() == quote_char:
            self.advance()  # 跳过结束引号

        return "".join(result)

    def read_number(self) -> Union[int, float]:
        """读取数字"""
        result = []
        has_dot = False

        while self.current_char() is not None:
            if self.current_char().isdigit():
                result.append(self.current_char())
                self.advance()
            elif self.current_char() == "." and not has_dot:
                has_dot = True
                result.append(self.current_char())
                self.advance()
            else:
                break

        num_str = "".join(result)
        return float(num_str) if has_dot else int(num_str)

    def read_identifier(self) -> str:
        """读取标识符"""
        result = []
        while self.current_char() is not None and (
            self.current_char().isalnum() or self.current_char() == "_"
        ):
            result.append(self.current_char())
            self.advance()
        return "".join(result)

    def tokenize(self) -> List[Token]:
        """执行词法分析"""
        self.tokens = []

        while self.current_char() is not None:
            # 跳过空白
            self.skip_whitespace()

            if self.current_char() is None:
                break

            start_line = self.line
            start_column = self.column

            char = self.current_char()

            # 注释
            if char == "#":
                self.skip_comment()
                continue

            # 换行
            if char == "\n":
                self.tokens.append(Token(TokenType.NEWLINE, "\n", start_line, start_column))
                self.advance()
                continue

            # 字符串
            if char in "\"'":
                value = self.read_string()
                self.tokens.append(Token(TokenType.STRING, value, start_line, start_column))
                continue

            # 数字
            if char.isdigit() or (char == "-" and self.peek_char() and self.peek_char().isdigit()):
                if char == "-":
                    self.advance()
                    value = -self.read_number()
                else:
                    value = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER, value, start_line, start_column))
                continue

            # 标识符和关键字
            if char.isalpha() or char == "_":
                identifier = self.read_identifier()
                lower_id = identifier.lower()

                # 检查是否是选择器关键字（后面跟着冒号）
                self.skip_whitespace()
                if lower_id in self.SELECTOR_KEYWORDS and self.current_char() == ":":
                    token_type = self.SELECTOR_KEYWORDS[lower_id]
                    self.tokens.append(Token(token_type, lower_id, start_line, start_column))
                    continue

                # 检查是否是普通关键字
                if lower_id in self.KEYWORDS:
                    self.tokens.append(
                        Token(self.KEYWORDS[lower_id], lower_id, start_line, start_column)
                    )
                else:
                    self.tokens.append(
                        Token(TokenType.IDENTIFIER, identifier, start_line, start_column)
                    )
                continue

            # 操作符和分隔符
            if char == ":":
                self.tokens.append(Token(TokenType.COLON, ":", start_line, start_column))
                self.advance()
                continue

            if char == ",":
                self.tokens.append(Token(TokenType.COMMA, ",", start_line, start_column))
                self.advance()
                continue

            if char == "(":
                self.tokens.append(Token(TokenType.LPAREN, "(", start_line, start_column))
                self.advance()
                continue

            if char == ")":
                self.tokens.append(Token(TokenType.RPAREN, ")", start_line, start_column))
                self.advance()
                continue

            if char == "=":
                self.tokens.append(Token(TokenType.EQUALS, "=", start_line, start_column))
                self.advance()
                continue

            # 未知字符，跳过
            self.advance()

        # 添加EOF
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens


class ScriptParser:
    """语法分析器"""

    COMMAND_TOKENS = {
        TokenType.CLICK,
        TokenType.CLICK_TEXT,
        TokenType.CLICK_ID,
        TokenType.INPUT,
        TokenType.CLEAR,
        TokenType.SWIPE,
        TokenType.WAIT,
        TokenType.WAIT_ELEMENT,
        TokenType.WAIT_GONE,
        TokenType.BACK,
        TokenType.HOME,
        TokenType.MENU,
        TokenType.RECENT,
        TokenType.START_APP,
        TokenType.STOP_APP,
        TokenType.CLEAR_APP,
        TokenType.SCREEN_ON,
        TokenType.SCREEN_OFF,
        TokenType.UNLOCK,
        TokenType.GET_TEXT,
        TokenType.GET_INFO,
        TokenType.FIND_ELEMENT,
        TokenType.FIND_ELEMENTS,
        TokenType.DUMP_HIERARCHY,
        TokenType.EXISTS,
        TokenType.LOG,
        TokenType.SHELL,
        # 人类模拟操作
        TokenType.HUMAN_CLICK,
        TokenType.HUMAN_DOUBLE_CLICK,
        TokenType.HUMAN_LONG_PRESS,
        TokenType.HUMAN_DRAG,
    }

    SELECTOR_TOKENS = {
        TokenType.SELECTOR_ID,
        TokenType.SELECTOR_TEXT,
        TokenType.SELECTOR_XPATH,
        TokenType.SELECTOR_CLASS,
    }

    MODIFIER_KEYWORDS: Dict[str, str] = {
        "parent": "parent",
        "parent_id": "parent_id",
        "parent_text": "parent_text",
        "parent_class": "parent_class",
        "sibling": "sibling",
        "sibling_id": "sibling_id",
        "sibling_text": "sibling_text",
        "sibling_class": "sibling_class",
        "sibling_relation": "sibling_relation",
        "offset_x": "offset_x",
        "offset_y": "offset_y",
        "offset": "offset",
    }

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        """获取当前token"""
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[self.pos]

    def peek_token(self, offset: int = 1) -> Token:
        """预览后续token"""
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[pos]

    def advance(self) -> Token:
        """前进一个token"""
        token = self.current_token()
        self.pos += 1
        return token

    def expect(self, token_type: TokenType) -> Token:
        """期望特定类型的token"""
        token = self.current_token()
        if token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type.name}, got {token.type.name} at line {token.line}, column {token.column}"
            )
        return self.advance()

    def skip_newlines(self) -> None:
        """跳过换行"""
        while self.current_token().type == TokenType.NEWLINE:
            self.advance()

    def parse(self) -> List[ASTNode]:
        """执行语法分析"""
        statements = []

        while self.current_token().type != TokenType.EOF:
            self.skip_newlines()

            if self.current_token().type == TokenType.EOF:
                break

            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)

        return statements

    def parse_statement(self) -> Optional[ASTNode]:
        """解析语句"""
        token = self.current_token()

        if token.type == TokenType.NEWLINE:
            self.advance()
            return None

        if token.type == TokenType.IF:
            return self.parse_if()

        if token.type == TokenType.LOOP:
            return self.parse_loop()

        if token.type == TokenType.WHILE:
            return self.parse_while()

        if token.type == TokenType.TRY:
            return self.parse_try()

        if token.type == TokenType.SET:
            return self.parse_set()

        if token.type == TokenType.CALL:
            return self.parse_call()

        if token.type == TokenType.BREAK:
            self.advance()
            return BreakNode(line=token.line, column=token.column)

        if token.type == TokenType.CONTINUE:
            self.advance()
            return ContinueNode(line=token.line, column=token.column)

        if token.type in self.COMMAND_TOKENS:
            return self.parse_command()

        # 跳过未知token
        self.advance()
        return None

    def parse_command(self) -> CommandNode:
        """解析命令"""
        token = self.advance()
        node = CommandNode(command=token.value, line=token.line, column=token.column)

        while self.current_token().type not in (TokenType.NEWLINE, TokenType.EOF):
            if self.current_token().type in self.SELECTOR_TOKENS:
                selector_token = self.advance()
                node.selector_type = selector_token.value
                self.expect(TokenType.COLON)
                value_token = self.advance()
                node.selector_value = value_token.value
            elif self.current_token().type == TokenType.STRING:
                node.args.append(self.advance().value)
            elif self.current_token().type == TokenType.NUMBER:
                node.args.append(self.advance().value)
            elif self.current_token().type == TokenType.IDENTIFIER:
                identifier = self.advance().value
                if self.current_token().type == TokenType.EQUALS:
                    self.advance()
                    if self.current_token().type in (
                        TokenType.STRING,
                        TokenType.NUMBER,
                        TokenType.IDENTIFIER,
                    ):
                        value = self.advance().value
                        if identifier in self.MODIFIER_KEYWORDS:
                            if identifier in ("offset_x", "offset_y", "offset"):
                                node.selector_modifiers[identifier] = int(value) if str(value).isdigit() else value
                            elif identifier in ("sibling_relation",):
                                node.selector_modifiers[identifier] = value
                            else:
                                parts = value.split(":")
                                if len(parts) == 2:
                                    node.selector_modifiers[f"{identifier}_type"] = parts[0]
                                    node.selector_modifiers[f"{identifier}_value"] = parts[1]
                                else:
                                    node.selector_modifiers[identifier] = value
                        else:
                            node.args.append(f"{identifier}={value}")
                    else:
                        node.args.append(identifier)
                else:
                    node.args.append(identifier)
            elif self.current_token().type == TokenType.COMMA:
                self.advance()
            else:
                break

        return node

    def parse_set(self) -> SetNode:
        """解析变量赋值"""
        token = self.advance()  # 消费 'set'
        node = SetNode(line=token.line, column=token.column)

        # 变量名
        var_token = self.expect(TokenType.IDENTIFIER)
        node.variable = var_token.value

        # 等号
        self.expect(TokenType.EQUALS)

        # 值：可以是字面量或命令结果
        if self.current_token().type in self.COMMAND_TOKENS:
            cmd_token = self.advance()
            node.command = cmd_token.value

            # 解析命令参数
            while self.current_token().type not in (TokenType.NEWLINE, TokenType.EOF):
                if self.current_token().type in self.SELECTOR_TOKENS:
                    selector_token = self.advance()
                    node.selector_type = selector_token.value
                    self.expect(TokenType.COLON)
                    value_token = self.advance()
                    node.selector_value = value_token.value
                elif self.current_token().type == TokenType.STRING:
                    node.command_args.append(self.advance().value)
                elif self.current_token().type == TokenType.NUMBER:
                    node.command_args.append(self.advance().value)
                elif self.current_token().type == TokenType.IDENTIFIER:
                    # 检查是否是命名参数（identifier = value）
                    identifier = self.advance().value
                    if self.current_token().type == TokenType.EQUALS:
                        self.advance()  # 消费 '='
                        # 获取值
                        if self.current_token().type in (
                            TokenType.STRING,
                            TokenType.NUMBER,
                            TokenType.IDENTIFIER,
                        ):
                            value = self.advance().value
                            # 将命名参数组合为 "key=value" 格式
                            node.command_args.append(f"{identifier}={value}")
                        else:
                            # 没有值，只添加标识符
                            node.command_args.append(identifier)
                    else:
                        node.command_args.append(identifier)
                elif self.current_token().type == TokenType.COMMA:
                    self.advance()
                else:
                    break
        elif self.current_token().type == TokenType.STRING:
            node.value = self.advance().value
        elif self.current_token().type == TokenType.NUMBER:
            node.value = self.advance().value
        elif self.current_token().type == TokenType.IDENTIFIER:
            node.value = self.advance().value

        return node

    def parse_condition(self) -> ConditionNode:
        """解析条件"""
        node = ConditionNode(line=self.current_token().line, column=self.current_token().column)

        # 检查是否有 not
        if self.current_token().type == TokenType.NOT:
            self.advance()
            node.negated = True

        # 条件命令（通常是 exists）
        if self.current_token().type in self.COMMAND_TOKENS:
            cmd_token = self.advance()
            node.command = cmd_token.value

            # 解析选择器和参数
            while self.current_token().type not in (
                TokenType.NEWLINE,
                TokenType.EOF,
                TokenType.IF,
                TokenType.ELIF,
                TokenType.ELSE,
                TokenType.END,
            ):
                if self.current_token().type in self.SELECTOR_TOKENS:
                    selector_token = self.advance()
                    node.selector_type = selector_token.value
                    self.expect(TokenType.COLON)
                    value_token = self.advance()
                    node.selector_value = value_token.value
                elif self.current_token().type == TokenType.STRING:
                    node.args.append(self.advance().value)
                elif self.current_token().type == TokenType.NUMBER:
                    node.args.append(self.advance().value)
                elif self.current_token().type == TokenType.IDENTIFIER:
                    # 检查是否是命名参数（identifier = value）
                    identifier = self.advance().value
                    if self.current_token().type == TokenType.EQUALS:
                        self.advance()  # 消费 '='
                        # 获取值
                        if self.current_token().type in (
                            TokenType.STRING,
                            TokenType.NUMBER,
                            TokenType.IDENTIFIER,
                        ):
                            value = self.advance().value
                            # 将命名参数组合为 "key=value" 格式
                            node.args.append(f"{identifier}={value}")
                        else:
                            # 没有值，只添加标识符
                            node.args.append(identifier)
                    else:
                        node.args.append(identifier)
                elif self.current_token().type == TokenType.COMMA:
                    self.advance()
                else:
                    break

        return node

    def parse_if(self) -> IfNode:
        """解析if语句"""
        token = self.advance()  # 消费 'if'
        node = IfNode(line=token.line, column=token.column)

        # 解析条件
        node.condition = self.parse_condition()

        self.skip_newlines()

        # 解析then分支
        while self.current_token().type not in (
            TokenType.ELIF,
            TokenType.ELSE,
            TokenType.END,
            TokenType.EOF,
        ):
            self.skip_newlines()
            if self.current_token().type in (
                TokenType.ELIF,
                TokenType.ELSE,
                TokenType.END,
                TokenType.EOF,
            ):
                break
            stmt = self.parse_statement()
            if stmt is not None:
                node.then_body.append(stmt)

        # 解析elif分支
        while self.current_token().type == TokenType.ELIF:
            self.advance()  # 消费 'elif'
            elif_condition = self.parse_condition()
            self.skip_newlines()

            elif_body = []
            while self.current_token().type not in (
                TokenType.ELIF,
                TokenType.ELSE,
                TokenType.END,
                TokenType.EOF,
            ):
                self.skip_newlines()
                if self.current_token().type in (
                    TokenType.ELIF,
                    TokenType.ELSE,
                    TokenType.END,
                    TokenType.EOF,
                ):
                    break
                stmt = self.parse_statement()
                if stmt is not None:
                    elif_body.append(stmt)

            node.elif_branches.append((elif_condition, elif_body))

        # 解析else分支
        if self.current_token().type == TokenType.ELSE:
            self.advance()  # 消费 'else'
            self.skip_newlines()

            while self.current_token().type not in (TokenType.END, TokenType.EOF):
                self.skip_newlines()
                if self.current_token().type in (TokenType.END, TokenType.EOF):
                    break
                stmt = self.parse_statement()
                if stmt is not None:
                    node.else_body.append(stmt)

        # 消费 'end'
        if self.current_token().type == TokenType.END:
            self.advance()

        return node

    def parse_loop(self) -> LoopNode:
        """解析loop语句"""
        token = self.advance()  # 消费 'loop'
        node = LoopNode(line=token.line, column=token.column)

        # 循环次数
        if self.current_token().type == TokenType.NUMBER:
            node.count = int(self.advance().value)

        # 可选的循环变量
        if self.current_token().type == TokenType.IDENTIFIER:
            node.variable = self.advance().value

        self.skip_newlines()

        # 解析循环体
        while self.current_token().type not in (TokenType.END, TokenType.EOF):
            self.skip_newlines()
            if self.current_token().type in (TokenType.END, TokenType.EOF):
                break
            stmt = self.parse_statement()
            if stmt is not None:
                node.body.append(stmt)

        # 消费 'end'
        if self.current_token().type == TokenType.END:
            self.advance()

        return node

    def parse_while(self) -> WhileNode:
        """解析while语句"""
        token = self.advance()  # 消费 'while'
        node = WhileNode(line=token.line, column=token.column)

        # 解析条件
        node.condition = self.parse_condition()

        self.skip_newlines()

        # 解析循环体
        while self.current_token().type not in (TokenType.END, TokenType.EOF):
            self.skip_newlines()
            if self.current_token().type in (TokenType.END, TokenType.EOF):
                break
            stmt = self.parse_statement()
            if stmt is not None:
                node.body.append(stmt)

        # 消费 'end'
        if self.current_token().type == TokenType.END:
            self.advance()

        return node

    def parse_try(self) -> TryNode:
        """解析try语句"""
        token = self.advance()  # 消费 'try'
        node = TryNode(line=token.line, column=token.column)

        self.skip_newlines()

        # 解析try体
        while self.current_token().type not in (TokenType.CATCH, TokenType.END, TokenType.EOF):
            self.skip_newlines()
            if self.current_token().type in (TokenType.CATCH, TokenType.END, TokenType.EOF):
                break
            stmt = self.parse_statement()
            if stmt is not None:
                node.try_body.append(stmt)

        # 解析catch体
        if self.current_token().type == TokenType.CATCH:
            self.advance()  # 消费 'catch'
            self.skip_newlines()

            while self.current_token().type not in (TokenType.END, TokenType.EOF):
                self.skip_newlines()
                if self.current_token().type in (TokenType.END, TokenType.EOF):
                    break
                stmt = self.parse_statement()
                if stmt is not None:
                    node.catch_body.append(stmt)

        # 消费 'end'
        if self.current_token().type == TokenType.END:
            self.advance()

        return node

    def parse_call(self) -> CallNode:
        """解析函数调用"""
        token = self.advance()  # 消费 'call'
        node = CallNode(line=token.line, column=token.column)

        # 函数名
        if self.current_token().type == TokenType.IDENTIFIER:
            node.function_name = self.advance().value
        elif self.current_token().type == TokenType.STRING:
            node.function_name = self.advance().value

        # 参数
        while self.current_token().type not in (TokenType.NEWLINE, TokenType.EOF):
            if self.current_token().type == TokenType.STRING:
                node.args.append(self.advance().value)
            elif self.current_token().type == TokenType.NUMBER:
                node.args.append(self.advance().value)
            elif self.current_token().type == TokenType.IDENTIFIER:
                # 检查是否是命名参数（identifier = value）
                identifier = self.advance().value
                if self.current_token().type == TokenType.EQUALS:
                    self.advance()  # 消费 '='
                    # 获取值
                    if self.current_token().type in (
                        TokenType.STRING,
                        TokenType.NUMBER,
                        TokenType.IDENTIFIER,
                    ):
                        value = self.advance().value
                        # 将命名参数组合为 "key=value" 格式
                        node.args.append(f"{identifier}={value}")
                    else:
                        # 没有值，只添加标识符
                        node.args.append(identifier)
                else:
                    node.args.append(identifier)
            elif self.current_token().type == TokenType.COMMA:
                self.advance()
            else:
                break

        return node


def parse_script(source: str) -> List[ASTNode]:
    """
    解析脚本源代码，返回AST节点列表

    Args:
        source: 脚本源代码字符串

    Returns:
        AST节点列表

    Raises:
        SyntaxError: 语法错误时抛出
    """
    lexer = ScriptLexer(source)
    tokens = lexer.tokenize()
    parser = ScriptParser(tokens)
    return parser.parse()


# 导出的公共接口
__all__ = [
    "TokenType",
    "Token",
    "ASTNode",
    "CommandNode",
    "SetNode",
    "IfNode",
    "LoopNode",
    "WhileNode",
    "TryNode",
    "CallNode",
    "BreakNode",
    "ContinueNode",
    "ConditionNode",
    "ScriptLexer",
    "ScriptParser",
    "parse_script",
]
