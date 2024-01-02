import cvxpy as cp
import Parameters

class ProblemBuilder():
    def __init__(self, parameters: Parameters) -> None:
        self.parameters = parameters
    def createVariables(self):
        # Dynamic variables
        self.f = cp.Variable((self.parameters.dimensions,self.parameters.tSteps+1))
        self.p = cp.Variable((self.parameters.dimensions,self.parameters.tSteps+1))
        self.v = cp.Variable((self.parameters.dimensions,self.parameters.tSteps+1))
        # Constant variables
        self.gF = cp.Constant((0,0,-self.parameters.g))
        # Objective function intialization
        self.oF = 0
        # Build the container of the restrictions
        self.newtonRestrictions = []
        self.forceRestrictions = []
        self.positionRestrictions = []
    def createRestrictions(self):
        for t in range(self.parameters.tSteps):
            self.oF += cp.norm2(self.f[:,t])
            self.newtonRestrictions += [self.p[:, t + 1] == self.p[:, t] + (self.parameters.dT/2) * (self.v[:, t] + self.v[:, t + 1]),
                                self.v[:, t + 1] == self.v[:, t] + (self.parameters.dT/self.parameters.m) * (self.f[:, t]) + self.parameters.dT * self.gF]
            self.forceRestrictions += [cp.norm2(self.f[:,t]) <= self.parameters.fMax]
            self.positionRestrictions += [self.p[2,t] >= self.parameters.alpha * cp.norm(self.p[:2,t])]
        # Rectification by gamma:
        self.oF = self.parameters.gamma * self.oF 
        # Final constriction
        self.cF = self.newtonRestrictions + self.forceRestrictions + self.positionRestrictions
        # Restrict to initial conditions
        self.cF += [self.p[:, self.parameters.tSteps] == 0, self.p[:, 0] == self.parameters.p0, self.v[:, self.parameters.tSteps] == 0, self.v[:, 0] == self.parameters.v0] 
    def createProblem(self):
        self.problem = cp.Problem(cp.Minimize(self.oF), self.cF)
        return self.problem