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

INT   : [0-9]+ ;
WS    : [ \t\r\n]+ -> skip ;
