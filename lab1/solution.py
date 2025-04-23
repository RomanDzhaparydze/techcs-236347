from syntax.lambda_pure import LambdaExpr, Id, Lambda, App, Let
import copy


def alpha_equivalent(e1: LambdaExpr, e2: LambdaExpr) -> bool:
    """Check if two lambda expressions differ only in the names of their bound variables."""
    match (e1, e2):
        case (Id(n1), Id(n2)):
            return n1 == n2
        case (App(f1, a1), App(f2, a2)):
            return alpha_equivalent(f1, f2) and alpha_equivalent(a1, a2)
        case (Lambda(var1, body1), Lambda(var2, body2)):
            v1, v2 = var1.name, var2.name
            renamed = alpha_rename(body2, v2, v1)
            return alpha_equivalent(body1, renamed)
        case (Let(decl1, def1, body1), Let(decl2, def2, body2)):
            d1, d2 = decl1.name, decl2.name
            body2_adj = alpha_rename(body2, d2, d1) if d1 != d2 else body2
            return alpha_equivalent(def1, def2) and alpha_equivalent(body1, body2_adj)
        case _:
            return False


def substitute(expr: LambdaExpr, var: str, repl: LambdaExpr) -> LambdaExpr:
    """Substitute all free occurrences of `var` in `expr` with `repl`."""
    match expr:
        case Id(name):
            return copy.deepcopy(repl) if name == var else expr
        case Lambda(param, body) if param.name == var:
            return expr
        case Lambda(param, body):
            return Lambda(param, substitute(body, var, repl))
        case App(func, arg):
            return App(substitute(func, var, repl), substitute(arg, var, repl))
        case Let(decl, defn, body) if decl.name == var:
            return Let(decl, substitute(defn, var, repl), body)
        case Let(decl, defn, body):
            return Let(decl,
                       substitute(defn, var, repl),
                       substitute(body, var, repl))
        case _:
            return expr


def beta_reduce(expr: LambdaExpr) -> LambdaExpr:
    """Perform a single beta reduction step on the given lambda expression."""
    match expr:
        case App(Lambda(param, body), arg):
            return substitute(body, param.name, arg)
        case App(func, arg):
            new_func = beta_reduce(func)
            if new_func is not func:
                return App(new_func, arg)
            new_arg = beta_reduce(arg)
            return App(func, new_arg)
        case Let(decl, defn, body):
            return substitute(body, decl.name, defn)
        case _:
            return expr


def alpha_rename(expr: LambdaExpr, old: str, new: str) -> LambdaExpr:
    """Rename all occurrences of `old` to `new` throughout the expression."""
    match expr:
        case Id(name):
            if name == old:
                return Id(new)
            return expr
        case Lambda(param, body) if param.name == old:
            return Lambda(Id(new), alpha_rename(body, old, new))
        case Lambda(param, body):
            return Lambda(param, alpha_rename(body, old, new))
        case App(func, arg):
            return App(alpha_rename(func, old, new), alpha_rename(arg, old, new))
        case Let(decl, defn, body) if decl.name == old:
            return Let(Id(new), alpha_rename(defn, old, new), alpha_rename(body, old, new))
        case Let(decl, defn, body):
            return Let(decl, alpha_rename(defn, old, new), alpha_rename(body, old, new))
        case _:
            return expr


def interpret(expr: LambdaExpr, fuel: int = 100_000) -> LambdaExpr:
    """Keep performing normal-order reduction steps until you reach normal form, detect divergence or run out of fuel."""
    curr = expr
    for _ in range(fuel):
        next_expr = beta_reduce(curr)
        if next_expr == curr:
            return curr
        curr = next_expr
    return curr
