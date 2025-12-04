import math
import sympy as sp
from typing import Optional, List, Dict, Any


class MetodoNewton:
    def __init__(self):
        self.x = sp.Symbol('x')

    def calcular_derivada(self, expressao: str):
        try:
            expr = sp.sympify(expressao)
            derivada = sp.diff(expr, self.x)
            return expr, derivada
        except:
            print("Erro: Expressão inválida!")
            return None, None

    def metodo_newton(self, expressao: str, x0: float, tol: float = 1e-6, max_iter: int = 100):
        f, f_deriv = self.calcular_derivada(expressao)

        if f is None:
            return None, []

        x_atual = x0
        historico = []

        print(f"\n--- Aplicando Método de Newton Padrão (Derivada Analítica) para: {expressao} ---")
        print("Fórmula: x_{n+1} = x_n - f(x_n) / f'(x_n)")
        print(f"Ponto inicial (x0) = {x0}")
        print("-" * 50)

        for iteracao in range(max_iter):
            f_num = sp.lambdify(self.x, f, 'math')
            f_deriv_num = sp.lambdify(self.x, f_deriv, 'math')

            fx = f_num(x_atual)
            fpx = f_deriv_num(x_atual)

            if abs(fpx) < 1e-10:
                print("Derivada muito próxima de zero! Tentando outro ponto inicial.")
                return None, historico

            x_novo = x_atual - fx / fpx

            historico.append({
                'iteracao': iteracao + 1,
                'x': x_atual,
                'f(x)': fx,
                "f'(x)": fpx,
                'x_novo': x_novo,
                'erro': abs(x_novo - x_atual)
            })

            print(f"Iteração {iteracao + 1}:")
            print(f"  x_n (x)     = {x_atual:.6f}")
            print(f"  f(x_n)      = {fx:.6f}")
            print(f"  f'(x_n)     = {fpx:.6f}")
            print(f"  x_n+1       = {x_novo:.6f}")
            print(f"  erro        = {abs(x_novo - x_atual):.6f}")
            print()

            if abs(x_novo - x_atual) < tol:
                print(f" Convergiu após {iteracao + 1} iterações!")
                print(f" Raiz encontrada: x = {x_novo:.8f}")
                print(f" f({x_novo:.8f}) = {fx:.2e}")
                return x_novo, historico

            x_atual = x_novo

        print(" Não convergiu após o número máximo de iterações")
        return None, historico

    # MÉTODO COM AS 3 APROXIMAÇÕES
    def metodo_newton_aproximado(self, expressao: str, x0: float, aproximacao: str = 'central',
                                 tol: float = 1e-6, max_iter: int = 100, delta: float = 1e-4):

        try:
            f = sp.sympify(expressao)
            f_num = sp.lambdify(self.x, f, 'math')
        except:
            print("Erro: Expressão inválida!")
            return None, []

        x_atual = x0
        historico = []

        formula_desc = {
            'avancada': f"Avançada: f'(x) ≈ (f(x+h) - f(x)) / h   | h = {delta}",
            'recuada':  f"Recuada:  f'(x) ≈ (f(x) - f(x-h)) / h   | h = {delta}",
            'central':  f"Central:  f'(x) ≈ (f(x+h) - f(x-h)) / (2*h) | h = {delta}"
        }

        if aproximacao not in formula_desc:
            print("Erro: Aproximação inválida. Use EXATAMENTE: avancada | recuada | central")
            return None, []

        print(f"\n  Método de Newton com APROXIMAÇÃO: {aproximacao.upper()}  ")
        print("Escolha disponível: avancada | recuada | central")
        print(f"Fórmula usada: {formula_desc[aproximacao]}")
        print(f"Ponto inicial (x0) = {x0}")
        print("-" * 50)

        for iteracao in range(max_iter):
            fx = f_num(x_atual)

            if aproximacao == 'avancada':
                fpx = (f_num(x_atual + delta) - fx) / delta

            elif aproximacao == 'recuada':
                fpx = (fx - f_num(x_atual - delta)) / delta

            elif aproximacao == 'central':
                fpx = (f_num(x_atual + delta) - f_num(x_atual - delta)) / (2 * delta)

            if abs(fpx) < 1e-10:
                print("Derivada aproximada próxima de zero!")
                return None, historico

            x_novo = x_atual - fx / fpx

            historico.append({
                'iteracao': iteracao + 1,
                'x': x_atual,
                'f(x)': fx,
                "f'(x)_aprox": fpx,
                'x_novo': x_novo,
                'erro': abs(x_novo - x_atual)
            })

            print(f"Iteração {iteracao + 1}:")
            print(f"  x_n = {x_atual:.6f}")
            print(f"  f(x_n) = {fx:.6f}")
            print(f"  f'(x_n) aprox = {fpx:.6f}")
            print(f"  x_n+1 = {x_novo:.6f}")
            print(f"  erro = {abs(x_novo - x_atual):.6f}\n")

            if abs(x_novo - x_atual) < tol:
                print(f" Convergiu após {iteracao + 1} iterações!")
                return x_novo, historico

            x_atual = x_novo

        print(" Não convergiu.")
        return None, historico


def resolver_desafios():
    newton = MetodoNewton()

    print("=" * 60)
    print("DESAFIO 1: 2^x = x^2   →   f(x) = 2**x - x**2")
    #print("=" * 60)

    desafio1 = "2**x - x**2"
    x0_desafio1 = 4.0

    for aprox in ['avancada', 'recuada', 'central']:
        newton.metodo_newton_aproximado(desafio1, x0_desafio1, aproximacao=aprox)

    print("\n" + "=" * 60)
    print("DESAFIO 2: tan(x) = 1/x   →   f(x) = tan(x) - 1/x")
    #print("=" * 60)

    desafio2 = "tan(x) - 1/x"
    x0_desafio2 = 0.5

    for aprox in ['avancada', 'recuada', 'central']:
        newton.metodo_newton_aproximado(desafio2, x0_desafio2, aproximacao=aprox)


def modo_interativo():
    newton = MetodoNewton()

    print("\n" + "=" * 60)
    print("MODO INTERATIVO - VOCÊ DEVE ESCOLHER:")
    print(" avancada")
    print(" recuada")
    print(" central")
    #print("=" * 60)

    while True:
        expressao = input("\nDigite a função f(x) (ou 'sair'): ")
        if expressao.lower() == 'sair':
            break

        f, derivada = newton.calcular_derivada(expressao)
        if f is None:
            print("Expressão inválida!")
            continue

        print("\nDerivada analítica apenas para referência:")
        print(f"f'(x) = {derivada}")
        #print("\nEscolha OBRIGATÓRIA da aproximação:")
        #print("[avancada]  |  [recuada]  |  [central]")

        try:
            x0 = float(input("Digite o ponto inicial x0: "))

            aprox = input(
                "Digite o tipo de aproximação(avancada/recuada/central): "
            ).strip().lower()

            if aprox not in ['avancada', 'recuada', 'central']:
                print("Tipo inválido! Usando CENTRAL.")
                aprox = 'central'

            newton.metodo_newton_aproximado(expressao, x0, aproximacao=aprox)

        except ValueError:
            print("Erro: x0 deve ser número!")


if __name__ == "__main__":
    print(" MÉTODO DE NEWTON")
    resolver_desafios()
    modo_interativo()