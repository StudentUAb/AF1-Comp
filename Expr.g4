grammar Expr;

// A entrada principal para a gramática
expr   : addExpr EOF ;

// Adiciona suporte para operações de adição e subtração com precedência à esquerda
addExpr: addExpr ('+' | '-') multExpr
       | multExpr
       ;

// Adiciona suporte para multiplicação e divisão
multExpr: multExpr ('*' | '/') atom
        | atom
        ;

// Atomos da expressão, incluindo números inteiros e expressões entre parênteses
atom  : INT
      | '(' addExpr ')'
      ;

// Tokens que não são reconhecidos como palavras-chave
INT   : [0-9]+ ;
// Espaços em branco são ignorados 
WS    : [ \t\r\n]+ -> skip ;