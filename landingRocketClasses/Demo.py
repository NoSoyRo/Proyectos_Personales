import Parameters
import ProblemBuilder
import Solver
import numpy.linalg as lng
import matplotlib.pyplot as plt

def graphSolution(pBuilder, parameters):
    fig = plt.figure(figsize = (10, 7))
    ax = plt.axes(projection ="3d")
    ax.scatter3D(pBuilder.p[0,:].value,pBuilder.p[1,:].value,pBuilder.p[2,:].value, color = "green")
    plt.title("Positions")
    for i in range(parameters.tSteps):
        d = pBuilder.f[:,i].value
        d2 = pBuilder.v[:,i].value
        ax.quiver(pBuilder.p[0, i].value,pBuilder.p[1, i].value,pBuilder.p[2, i].value, d[0], d[1], d[2])
        ax.quiver(pBuilder.p[0, i].value,pBuilder.p[1, i].value,pBuilder.p[2, i].value, d2[0], d2[1], d2[2], color = 'r')
    plt.show()

if __name__ == '__main__':
    parameters = Parameters.Parameters()
    pBuilder   = ProblemBuilder.ProblemBuilder(parameters)
    pBuilder.createVariables()
    pBuilder.createRestrictions()
    problem = pBuilder.createProblem()
    solver = Solver.Solver(problem)
    solvedProblem = solver.solveProblem()
    graphSolution(pBuilder, parameters)