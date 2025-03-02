from abc import ABC, abstractmethod


class LlmRunnerInterface(ABC):
    @abstractmethod
    def consultAi(self,data,isRiskAssessment,ignoreMockConfig=False):
        pass