from syntax.lambda_pure import LambdaExpr, parse
from syntax.lambda_pure import Id, Lambda, App, Let


def alpha_equivalent(e1: LambdaExpr, e2: LambdaExpr) -> bool:
    """Check if two lambda expressions differ only in the names of their bound variables."""
    raise NotImplementedError
    
def beta_reduce(expr: LambdaExpr) -> LambdaExpr:
    substitute(expr.body, expr.body., expr.arg)
    """Perform a single beta reduction step on the given lambda expression."""
    raise NotImplementedError

def substitute(expr: LambdaExpr, old_var: str, new_var: str) -> LambdaExpr:
    print(type(expr.arg.))
    match expr:
        case Id(name):
            print("hui")
            if name == old_var:
                print()
                return Id(new_var)
        case Lambda(var, body):
            if var.name == old_var:
                return Lambda(var, body)
            else:
                return Lambda(Id(new_var), substitute(body, old_var, new_var))
        case App(func, arg):
            return App(substitute(func, old_var, new_var), substitute(arg, old_var, new_var))
        case Let(decl, defn, body):
            return Let(decl, substitute(defn, old_var, new_var), substitute(body, old_var, new_var))
        case _:
            return expr
    
    raise NotImplementedError

def alpha_rename(expr: LambdaExpr, old_var: str, new_var: str) -> LambdaExpr:

    """Rename all occurrences of old_var in e to new_var, ensuring that the new variable does not conflict with any existing variables."""
    


def interpret(e: LambdaExpr, fuel: int = 100_000) -> LambdaExpr:
    """Keep performing normal-order reduction steps until you reach normal form, detect divergence or run out of fuel."""
    raise NotImplementedError


lambda_expr = parse(r"(\x. x) (x 6)")
print(lambda_expr)
substituted = substitute(lambda_expr, "x", "y")
print(substituted)