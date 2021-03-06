# coding: utf-8

from fenics import *

NUM_ELEM = 32

# --- Problem data
a = 1.0  # m
b = 1.0  # m
h = 0.050  # m

E = 69e9  # Pa
nu = 0.35

u0 = Constant(0.0)
f = Constant(-10e3)  # Uniform load

# ---

#mesh = UnitSquareMesh(NUM_ELEM, NUM_ELEM)
mesh = Mesh("strange-plate.xml")

CG = FunctionSpace(mesh, 'CG', 2)
CG = FunctionSpace(mesh, 'CG', 2)

W = CG * CG  # MixedFunctionSpace

def boundary(x, on_boundary):
    return on_boundary

bc1 = DirichletBC(W.sub(0), u0, boundary)  # Zero displacement at the boundary
bc2 = DirichletBC(W.sub(1), Constant(0.0), boundary)
#bc = [bc1, bc2]  # Simply supported
bc = [bc1]  # Clamped

u, v = TrialFunctions(W)
psi, phi = TestFunctions(W)

D = E * h**3 / (12 * (1 - nu**2))

a = D * (inner(nabla_grad(u), nabla_grad(phi)) + inner(nabla_grad(v), nabla_grad(psi)) - inner(v, phi)) * dx
L = f * psi * dx

w = Function(W)
solve(a == L, w, bc)

u, v = w.split()

plot(u)
plot(v)
plot(mesh)
interactive()
