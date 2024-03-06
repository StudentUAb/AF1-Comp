# Importação de módulos
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Tree import ParseTree
import matplotlib.pyplot as plt
import networkx as nx
# Importação do lexer e do parser de Expr (gerado pelo ANTLR)
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from ExprListener import ExprListener

# Implementação do listener
class EvalListener(ExprListener):
    # Construtor
    def __init__(self):
        self.stack = []
    # Método para entrada de expressões
    def push(self, item):
        self.stack.append(item)
        print(f"Empurrado: {item}, pilha agora: {self.stack}")

    # Método para saída de expressões de adição/subtração
    def exitAddExpr(self, ctx):
        if ctx.getChildCount() == 3: # se o número de filhos for 3
            right = self.stack.pop() if self.stack else None # pega o último elemento da pilha
            left = self.stack.pop() if self.stack else None # pega o penúltimo elemento da pilha
            op = ctx.getChild(1).getText() # pega o operador
            print(f"Processando expr: {left} {op} {right}") # imprime a expressão
            if left is not None and right is not None: # se ambos os operandos não forem None
                if op == '+': # se o operador for +
                    self.push(left + right) # empurra a soma dos operandos para a pilha
                elif op == '-': # se o operador for -
                    self.push(left - right) # empurra a subtração dos operandos para a pilha

    # Método para saída de expressões de multiplicação/divisão
    # def exitMultExpr(self, ctx):
    #     if ctx.getChildCount() == 3: # se o número de filhos for 3
    #         right = self.stack.pop() if self.stack else None # pega o último elemento da pilha
    #         left = self.stack.pop() if self.stack else None # pega o penúltimo elemento da pilha
    #         op = ctx.getChild(1).getText() # pega o operador
    #         print(f"Processando Multiexpr: {left} {op} {right}") # imprime a expressão
    #         if left is not None and right is not None: # se ambos os operandos não forem None
    #             if op == '*': # se o operador for *
    #                 self.push(left * right) # empurra a multiplicação dos operandos para a pilha
    #             elif op == '/': # se o operador for /
    #                 self.push(left / right)  # Atenção à divisão por zero

    # Método para saída de expressões de adição/subtração
    def exitAtom(self, ctx):
        if ctx.getChildCount() == 1 and ctx.INT() is not None: # se o número de filhos for 1 e o token INT não for None
            self.push(int(ctx.INT().getText())) # empurra o inteiro para a pilha
            print(f"Processado inteiro (INT): {ctx.INT().getText()}") # imprime o inteiro para a pilha
        # Não é necessário processar explicitamente '(', addExpr ')' porque a pilha cuida disso

    # Método para saída de inteiros
    def exitInt(self, ctx):
        # Este método pode não ser mais necessário se 'atom' estiver processando INTs,
        # mas é mantido aqui para compatibilidade com versões anteriores da gramática.
        self.push(int(ctx.getText())) # empurra o inteiro para a pilha
        print(f"Processado inteiro (INT): {ctx.getText()}") # imprime o inteiro

# Implementação do listener para lançar exceções em erros sintáticos
class ThrowingErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e): # método para erros sintáticos
        raise Exception(f"Linha {line}:{column} {msg}") # lança uma exceção com a mensagem de erro

# Implementação da função que avalia a expressão
def evaluate(expression):
    input_stream = InputStream(expression) # cria um objeto InputStream com a expressão
    lexer = ExprLexer(input_stream)  # cria um objeto ExprLexer com o InputStream
    stream = CommonTokenStream(lexer)  # cria um objeto CommonTokenStream com o lexer
    parser = ExprParser(stream)  # crie um objeto ExprParser com o CommonTokenStream

    parser.removeErrorListeners() # remove o listener padrão do parser
    parser.addErrorListener(ThrowingErrorListener())  # adiciona o listener de erros lançando exceções para erros sintáticos

    tree = parser.expr() # obtem a árvore de análise sintática

    print("\nÁrvore de Análise Sintática:") # imprime a árvore de análise sintática
    print(tree.toStringTree(recog=parser)) # imprime a árvore de análise sintática  

    listener = EvalListener()  # cria um objeto EvalListener
    walker = ParseTreeWalker()  # cria um objeto ParseTreeWalker
    walker.walk(listener, tree)  # percorre a árvore de análise sintática com o listener

    return listener.stack[-1] if listener.stack else None # retorna o último elemento da pilha do listener

# Função auxiliar para adicionar nós e arestas ao grafo a partir da árvore de análise
def add_nodes_edges(node, graph, labels, parent=None):
    node_id = id(node) # obtem o endereço de memória do nó  

    if isinstance(node, TerminalNode): # se o nó for um TerminalNode
        labels[node_id] = node.getText() # o rótulo do nó é o texto do nó
    else: # se o nó não for um TerminalNode
        labels[node_id] = ExprParser.ruleNames[node.getRuleIndex()] # o rótulo do nó é o nome da regra do nó

    graph.add_node(node_id) # adiciona o nó ao grafo

    if parent is not None: # se o nó tiver um pai
        graph.add_edge(parent, node_id) # adiciona uma aresta do pai para o nó

    if not isinstance(node, TerminalNode): # se o nó não for um TerminalNode
        for child in node.children: # para cada filho do nó 
            add_nodes_edges(child, graph, labels, node_id) # adiciona o nó e as arestas ao grafo

# Função para visualizar a árvore de análise sintática
def plot_parse_tree(tree, parser):
    graph = nx.DiGraph() # cria um grafo direcionado
    labels = {} # cria um dicionário para armazenar os rótulos dos nós
    add_nodes_edges(tree, graph, labels) # 
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(12, 8))
    nx.draw(graph, pos, labels=labels, with_labels=True, arrows=False)
    plt.show()

# Implementação da função principal com a funcionalidade de visualização da árvore
def main():
    expression = "1 + 2 - 3"
    print(f"Expressão de entrada: {expression}")
    input_stream = InputStream(expression)
    lexer = ExprLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ExprParser(stream)
    tree = parser.expr()  

    listener = EvalListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)  

    result = listener.stack[-1] if listener.stack else None
    print(f"Resultado final: {result}")  

    plot_parse_tree(tree, parser)  

if __name__ == "__main__":
    main()
