import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as LA

"""
Given 2x2 linear differential system x'(t) = Ax(t), this program will produce
the general solution x(t)
Jackson Lyons
"""

def graph_eigenvectors(eig_vec1, eig_vec2) -> None:
    """
    This function graphs the eigenvectors of the given 2x2 matrix using matplotlib
    :param eig_vec1: 1st eigenvector to be graphed
    :param eig_vec2: 2nd eigenvector to be graphed
    :return: None
    """
    origin = [0, 0]
    # graph eigenvectors of A
    v1 = plt.quiver(*origin, *eig_vec1, color=['r'], scale=5)
    v2 = plt.quiver(*origin, *eig_vec2, color=['g'], scale=5)
    plt.quiverkey(v1, -.5, -.9, .2, "eigenvector1", color='r', labelpos='E')
    plt.quiverkey(v2, -.4, -.8, .2, "eigenvector2", color='g', labelpos='E')


    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    plt.title("Eigenvectors")
    plt.grid()
    #plt.show()

def build_real_solution(eig_val1, eig_val2, eig_vec1, eig_vec2):
    # check for repeated eigen_values
    if eig_val1 == eig_val2:
        x_t = "c1*e^({lam1}t){v1} + c2*e^({lam1}t)({v1}t + {v2})".format(
            lam1=eig_val1, v1=eig_vec1, v2=eig_vec2)
    else:
        x_t = "c1*e^({lam1}t){v1} + c2*e^({lam2}t){v2}".format(lam1=eig_val1, lam2=eig_val2,
                                                     v1=eig_vec1, v2=eig_vec2)
    print("The general solution is of the form: x(t) = ", x_t)
    print("Where c1, c2 are real scalars")
    return x_t

def classify_real_sol(eig_val1, eig_val2) -> None:
    # check for repeated eigen_values
    if eig_val1 == eig_val2:
        if eig_val1 > 0:
            classification = "Degenerate Source"
        else:
            classification = "Degenerate Sink"
    else:
        if eig_val1 > 0 and eig_val2 > 0:
            classification = "Source Node"
        elif eig_val1 < 0 and eig_val2 < 0:
            classification = "Sink Node"
        else:
            classification = "Saddle Node"
    print("The solution at x=0 is classified as a ", classification)

def diagonalize(eig_val1, eig_val2, eig_vec1, eig_vec2):
    # check if you can diagonalize i.e. need n lin_indy eigenvectors.
    # i.e. need the matrix X with n eigenvectors to be nonsingular
    # check if det(x) != 0
    x = np.array([eig_vec1, eig_vec2])
    d1 = np.array([eig_val1, 0])
    d2 = np.array([0, eig_val2])
    d = np.array([d1, d2])
    if LA.det(x) == 0:
        print("This matrix is not diagonalizable")
    else:
        x_inv = LA.inv(x)
        print("This matrix is diagonalizable. X diagonalizes A")
        print("A = XDX^(-1):  X = {x}, D = {d}, X^(-1) = {x_inv}".format(
            x=x, d=d, x_inv=x_inv))

def build_equation(t, eig_val1, eig_val2, eig_vec1, eig_vec2):
    if eig_val1 == eig_val2:  # repeated eigenvalues
        x1_vec = np.exp(eig_val1*t)*eig_vec1[0] + np.exp(eig_val1*t) * (t*eig_vec1[0] + eig_vec2[0])
        x2_vec = np.exp(eig_val1*t)*eig_vec1[1] + np.exp(eig_val1*t) * (t*eig_vec1[1] + eig_vec2[1])
    else:
        x1_vec = np.exp(eig_val1*t)*eig_vec1[0] + np.exp(eig_val2*t)*eig_vec2[0]
        x2_vec = np.exp(eig_val1*t)*eig_vec1[1] + np.exp(eig_val2*t)*eig_vec2[1]
    return x1_vec, x2_vec

def build_solution_equation(eig_val1, eig_val2, eig_vec1, eig_vec2):
    dx = dt = 0.025
    t = np.arange(0, 0.1 + dt, dt)

    x1 = np.arange(-5, 5, 0.1)
    x2 = np.arange(-5, 5, 0.1)

    # Meshgrid
    X1, X2 = np.meshgrid(x1, x2)

    for i in range(len(t)):
        x1_vec, x2_vec = build_equation(t, eig_val1, eig_val2, eig_vec1, eig_vec2)
        #plt.plot(x1_vec, x2_vec, color ='tab:blue')
    plt.show()

def graph_direction_field(mat):
    x = np.arange(-5, 5, 0.6)
    y = np.arange(-5, 5, 0.6)

    for u in x:
        for v in y:
            point = np.array([u, v])
            result = np.matmul(mat, point)
            plt.quiver(u, v, *result, color='blue', scale=25)

    plt.grid()
    plt.show()


if __name__ == "__main__":
    A = input("Enter 2x2 matrix in the form 'a_11 a_12;a_21 a_22': ")

    mat = np.mat(A)
    mat = np.array(mat)

    eigen_values, eigen_vectors = LA.eig(mat)
    eig_val1 = eigen_values[0]
    eig_val2 = eigen_values[1]
    array_eig_vectors = np.squeeze(np.asarray(eigen_vectors))
    eig_vec1 = array_eig_vectors[:, 0]
    eig_vec2 = array_eig_vectors[:, 1]


    print("Eigenvalues: ", eigen_values)
    print("Eigenvectors: ", eigen_vectors)

    graph_eigenvectors(eig_vec1, eig_vec2)
    if True not in np.iscomplex(eigen_values):
        x_t = build_real_solution(eig_val1, eig_val2, eig_vec1, eig_vec2)
        graph_direction_field(mat)
        #graph_solution(x_t)
        #build_solution_equation(eig_val1, eig_val2, eig_vec1, eig_vec2)


    diagonalize_q = input("Would you like to diagonalize the inputted matrix? Y or N ")
    if diagonalize_q.lower() == "y":
        diagonalize(eig_val1, eig_val2, eig_vec1, eig_vec2)





