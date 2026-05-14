from .boxing import BoxingKnowledge
from .strength import StrengthKnowledge
from .athletic import AthleticKnowledge
from .cardio import CardioKnowledge

class KnowledgeBase:
    boxing = BoxingKnowledge()
    strength = StrengthKnowledge()
    athletic = AthleticKnowledge()
    cardio = CardioKnowledge()
