import tkinter as tk
import re

token_patterns = {
    'PROGRAMA': r'\bprograma\b',
    'DECLARE': r'\bdeclare\b',
    'FIMPROG': r'\bfimprog\b',
    'SE': r'\bse\b',
    'ENTAO': r'\bentao\b',
    'SENAO': r'\bsenao\b',
    'ENQUANTO': r'\benquanto\b',
    'LEIA': r'\bleia\b',
    'ESCREVA': r'\bescreva\b',
    'FOR': r'\bfor\b',
    'INTEIRO': r'\binteiro\b',
    'REAL': r'\breal\b',
    'OP_ATRIB': r':=',
    'DOIS_PONTOS': r':',
    'PONTO_VIRGULA': r';',
    'OP_REL': r'(<=|>=|!=|==|<|>)',
    'OP_ARIT': r'(\+|\-|\*|/)',
    'OP_LOGICO': r'(&&|\|\||!)',
    'ID': r'\b[a-zA-Z_]\w*\b',
    'NUM': r'\b\d+(\.\d+)?\b',
    'TEXTO': r'"[^"]*"',
    'PONTO': r'\.',
    'VIRGULA': r',',
    'PARENTESES_ABRE': r'\(',
    'PARENTESES_FECHA': r'\)',
    'CHAVE_ABRE': r'\{',
    'CHAVE_FECHA': r'\}',
}

symbol_table = {}

def add_variable_to_symbol_table(name, var_type):
    if name in symbol_table:
        raise SyntaxError(f'Variável {name} já foi declarada.')
    symbol_table[name] = {'type': var_type, 'initialized': False, 'used': False}

def initialize_variable(name):
    if name not in symbol_table:
        raise SyntaxError(f'Variável {name} não foi declarada.')
    symbol_table[name]['initialized'] = True

def use_variable(name):
    if name not in symbol_table:
        raise SyntaxError(f'Variável {name} não foi declarada.')
    symbol_table[name]['used'] = True
    if not symbol_table[name]['initialized']:
        print(f'Warning: Variável {name} está sendo usada sem ter sido inicializada.')

def check_unused_variables():
    for var, info in symbol_table.items():
        if not info['used']:
            print(f'Warning: Variável {var} foi declarada, mas não foi usada.')

def tokenize(code):
    tokens = []
    while code:
        match = None
        code = code.lstrip()
        if not code:
            break
        for token_type, pattern in token_patterns.items():
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                tokens.append((token_type, match.group(0)))
                code = code[match.end():]
                break
        if not match:
            print(f"Erro ao processar: {code}")
            raise SyntaxError(f'Unexpected character: {code[0]}')
    return tokens

tokens = []
current_token = 0
generated_code = ""

def match(expected_token_type):
    global current_token
    if current_token < len(tokens) and tokens[current_token][0] == expected_token_type:
        current_token += 1
    else:
        raise SyntaxError(f'Esperado {expected_token_type}, mas encontrado {tokens[current_token][0]}')

def parse_prog():
    global generated_code
    generated_code += "#include <stdio.h>\n\nint main() {\n"
    match('PROGRAMA')
    while tokens[current_token][0] == 'DECLARE':
        parse_declara()
    parse_bloco()
    match('FIMPROG')
    generated_code += "    return 0;\n}\n"

def parse_declara():
    global generated_code
    match('DECLARE')
    var_names = parse_id_list()
    match('DOIS_PONTOS')
    var_type = parse_tipo()
    match('PONTO')
    if var_type == 'INTEIRO':
        generated_code += f"    int {', '.join(var_names)};\n"
    elif var_type == 'REAL':
        generated_code += f"    float {', '.join(var_names)};\n"
    for var_name in var_names:
        add_variable_to_symbol_table(var_name, var_type)

def parse_id_list():
    var_names = []
    match('ID')
    var_names.append(tokens[current_token - 1][1])
    while tokens[current_token][0] == 'VIRGULA':
        match('VIRGULA')
        match('ID')
        var_names.append(tokens[current_token - 1][1])
    return var_names

def parse_tipo():
    if tokens[current_token][0] == 'INTEIRO':
        match('INTEIRO')
        return 'INTEIRO'
    elif tokens[current_token][0] == 'REAL':
        match('REAL')
        return 'REAL'
    else:
        raise SyntaxError(f'Tipo inválido: {tokens[current_token][0]}')

def parse_bloco():
    global current_token
    while tokens[current_token][0] != 'CHAVE_FECHA' and tokens[current_token][0] != 'FIMPROG':
        if tokens[current_token][0] == 'PONTO':
            match('PONTO')
        else:
            parse_cmd()

def parse_cmd():
    if tokens[current_token][0] == 'LEIA':
        parse_cmd_leitura()
    elif tokens[current_token][0] == 'ESCREVA':
        parse_cmd_escrita()
    elif tokens[current_token][0] == 'ID':
        parse_cmd_expr()
    elif tokens[current_token][0] == 'SE':
        parse_cmd_if()
    elif tokens[current_token][0] == 'ENQUANTO':
        parse_cmd_while()
    elif tokens[current_token][0] == 'FOR':
        parse_cmd_for()
    else:
        raise SyntaxError(f'Comando inválido: {tokens[current_token][0]}')

def parse_cmd_leitura():
    global generated_code
    match('LEIA')
    match('PARENTESES_ABRE')
    match('ID')
    var_name = tokens[current_token - 1][1]
    use_variable(var_name)
    var_type = symbol_table[var_name]['type']
    if var_type == 'INTEIRO':
        generated_code += f'    scanf("%d", &{var_name});\n'
    elif var_type == 'REAL':
        generated_code += f'    scanf("%f", &{var_name});\n'
    match('PARENTESES_FECHA')

def parse_cmd_escrita():
    global generated_code
    match('ESCREVA')
    match('PARENTESES_ABRE')
    if tokens[current_token][0] == 'TEXTO':
        generated_code += f'    printf({tokens[current_token][1]});\n'
        match('TEXTO')
    elif tokens[current_token][0] == 'ID':
        var_name = tokens[current_token][1]
        use_variable(var_name)
        var_type = symbol_table[var_name]['type']
        if var_type == 'INTEIRO':
            generated_code += f'    printf("%d", {var_name});\n'
        elif var_type == 'REAL':
            generated_code += f'    printf("%f", {var_name});\n'
        match('ID')
    else:
        raise SyntaxError(f'Esperado TEXTO ou ID, mas encontrado {tokens[current_token][0]}')
    match('PARENTESES_FECHA')

def parse_cmd_expr():
    global generated_code
    match('ID')
    var_name = tokens[current_token - 1][1]
    initialize_variable(var_name)
    use_variable(var_name)
    match('OP_ATRIB')
    generated_code += f'    {var_name} = '
    parse_expr()
    generated_code += ";\n"

def parse_expr():
    global generated_code
    parse_termo()
    while tokens[current_token][0] in ['OP_ARIT', 'OP_REL', 'OP_LOGICO']:
        operator = tokens[current_token][1]
        generated_code += f' {operator} '
        match(tokens[current_token][0])
        parse_termo()

def parse_termo():
    global generated_code
    if tokens[current_token][0] == 'NUM':
        generated_code += tokens[current_token][1]
        match('NUM')
    elif tokens[current_token][0] == 'ID':
        var_name = tokens[current_token][1]
        use_variable(var_name)
        generated_code += var_name
        match('ID')
    elif tokens[current_token][0] == 'PARENTESES_ABRE':
        match('PARENTESES_ABRE')
        generated_code += '('
        parse_expr()
        match('PARENTESES_FECHA')
        generated_code += ')'
    else:
        raise SyntaxError(f'Esperado NUM, ID ou parênteses, mas encontrado {tokens[current_token][0]}')

def parse_cmd_if():
    global generated_code
    match('SE')
    match('PARENTESES_ABRE')
    generated_code += "    if ("
    parse_expr()
    generated_code += ") {\n"
    match('PARENTESES_FECHA')
    match('ENTAO')
    match('CHAVE_ABRE')
    parse_bloco()
    match('CHAVE_FECHA')
    generated_code += "    }\n"
    if tokens[current_token][0] == 'SENAO':
        match('SENAO')
        match('CHAVE_ABRE')
        generated_code += "    else {\n"
        parse_bloco()
        match('CHAVE_FECHA')
        generated_code += "    }\n"

def parse_cmd_while():
    global generated_code
    match('ENQUANTO')
    match('PARENTESES_ABRE')
    generated_code += "    while ("
    parse_expr()
    generated_code += ") {\n"
    match('PARENTESES_FECHA')
    match('CHAVE_ABRE')
    parse_bloco()
    match('CHAVE_FECHA')
    generated_code += "    }\n"

def parse_cmd_for():
    global generated_code
    match('FOR')
    match('PARENTESES_ABRE')
    match('ID')
    var_name = tokens[current_token - 1][1]
    initialize_variable(var_name)
    use_variable(var_name)
    match('OP_ATRIB')
    generated_code += f"    for ({var_name} = "
    parse_expr()
    match('PONTO_VIRGULA')
    generated_code += "; "
    parse_expr()
    match('PONTO_VIRGULA')
    generated_code += "; "
    match('ID')
    var_name_inc = tokens[current_token - 1][1]
    use_variable(var_name_inc)
    match('OP_ATRIB')
    generated_code += f"{var_name_inc} = "
    parse_expr()
    match('PARENTESES_FECHA')
    generated_code += ") {\n"
    match('CHAVE_ABRE')
    parse_bloco()
    match('CHAVE_FECHA')
    generated_code += "    }\n"

def parse(tokens_list):
    global tokens, current_token, generated_code, symbol_table
    tokens = tokens_list
    current_token = 0
    generated_code = ""
    symbol_table = {}
    parse_prog()
    check_unused_variables()

codigo_exemplo = '''
programa
declare a, b, c: inteiro.
declare x, y: real.
declare z: inteiro.

a := 10.
b := 5.
c := a + b * 2.

x := 3.14.
y := x / 2.0.

se (a > b && x < y) entao {
   escreva("A é maior que B e X é menor que Y").
} senao {
   escreva("Condição falsa").
}

enquanto (b > 0) {
   b := b - 1.
   escreva(b).
}

for (a := 0; a < 10; a := a + 1) {
   escreva(a).
}

escreva(c).

fimprog.
'''

tokens = tokenize(codigo_exemplo)
parse(tokens)

def toggle_dark_mode():
    if dark_mode_var.get() == 1:
        root.config(bg="#2e2e2e")
        editor.config(bg="#1e1e1e", fg="white", insertbackground="white")
        output_box.config(bg="#1e1e1e", fg="white", insertbackground="white")
        editor.tag_configure("keyword", foreground="yellow")
        editor.tag_configure("operator", foreground="blue")
        editor.tag_configure("number", foreground="green")
    else:
        root.config(bg="white")
        editor.config(bg="white", fg="black", insertbackground="black")
        output_box.config(bg="white", fg="black", insertbackground="black")
        editor.tag_configure("keyword", foreground="blue")
        editor.tag_configure("operator", foreground="yellow")
        editor.tag_configure("number", foreground="green")

def highlight_syntax(event=None):
    editor.tag_remove("keyword", "1.0", tk.END)
    editor.tag_remove("operator", "1.0", tk.END)
    editor.tag_remove("number", "1.0", tk.END)
    keywords = r"\b(programa|declare|inteiro|real|se|entao|senao|enquanto|leia|escreva|fimprog|for)\b"
    operators = r"(\+|\-|\*|\/|\=|\<|\>)"
    numbers = r"\b\d+\b"
    start = "1.0"
    while True:
        match = re.search(keywords, editor.get(start, tk.END))
        if not match:
            break
        start_idx = editor.index(f"{start}+{match.start()}c")
        end_idx = editor.index(f"{start}+{match.end()}c")
        editor.tag_add("keyword", start_idx, end_idx)
        start = end_idx
    start = "1.0"
    while True:
        match = re.search(operators, editor.get(start, tk.END))
        if not match:
            break
        start_idx = editor.index(f"{start}+{match.start()}c")
        end_idx = editor.index(f"{start}+{match.end()}c")
        editor.tag_add("operator", start_idx, end_idx)
        start = end_idx
    start = "1.0"
    while True:
        match = re.search(numbers, editor.get(start, tk.END))
        if not match:
            break
        start_idx = editor.index(f"{start}+{match.start()}c")
        end_idx = editor.index(f"{start}+{match.end()}c")
        editor.tag_add("number", start_idx, end_idx)
        start = end_idx

def compile_code():
    global generated_code
    code = editor.get("1.0", tk.END)
    try:
        tokens = tokenize(code)
        parse(tokens)
        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert("1.0", generated_code)
        output_box.see(tk.END)
        output_box.update_idletasks()
        output_box.config(state="disabled")
    except SyntaxError as e:
        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"Erro de Sintaxe: {str(e)}")
        output_box.config(state="disabled")

root = tk.Tk()
root.title("LGG para C")

dark_mode_var = tk.IntVar()
dark_mode_checkbox = tk.Checkbutton(root, text="Modo Noturno", variable=dark_mode_var, command=toggle_dark_mode)
dark_mode_checkbox.pack()

editor = tk.Text(root, wrap="word", font=("Courier New", 12))
editor.pack(fill="both", expand=True)

editor.tag_configure("keyword", foreground="blue")
editor.tag_configure("operator", foreground="yellow")
editor.tag_configure("number", foreground="green")

codigo_exemplo_LGG = '''
programa
declare a, b, c: inteiro.
declare x, y: real.
declare z: inteiro.

a := 10.
b := 5.
c := a + b * 2.

x := 3.14.
y := x / 2.0.

se (a > b && x < y) entao {
   escreva("A é maior que B e X é menor que Y").
} senao {
   escreva("Condição falsa").
}

enquanto (b > 0) {
   b := b - 1.
   escreva(b).
}

for (a := 0; a < 10; a := a + 1) {
   escreva(a).
}

escreva(c).

fimprog.
'''

editor.insert("1.0", codigo_exemplo_LGG)

compile_button = tk.Button(root, text="Compilar", command=compile_code)
compile_button.pack()

output_box = tk.Text(root, wrap="word", height=10, state="disabled", font=("Courier New", 12))
output_box.pack(fill="both", expand=True)

editor.bind("<KeyRelease>", highlight_syntax)

root.mainloop()
