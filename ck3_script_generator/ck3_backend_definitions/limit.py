
from .limit_base import *
from .context import CONTXET

RELATION_NE = -1
RELATION_EQ = 0
RELATION_GT = 1
RELATION_LT = 2
RELATION_GE = 3
RELATION_LE = 4

RELATION = {
    "!=": RELATION_NE,
    ">=": RELATION_GE,
    "<=": RELATION_LE,
    "=": RELATION_EQ,
    ">": RELATION_GT,
    "<": RELATION_LT,
}

class Compare(Limit):
    lhs: str
    relation: str
    rhs: str
    def __init__(self, cmp: str):
        cmp.replace(" ", "")
        for relation in RELATION.keys():
            r = cmp.split(relation)
            if len(r) == 2:
                self.lhs = r[0]
                self.rhs = r[1]
                self.relation = relation
            elif len(r) == 1:
                cmp = r[0]
            else:
                raise
        raise
    def is_satisfied(self):
        return CONTXET.compare(self.lhs, self.relation, self.rhs)
        # lhs = CONTXET.get_compare_value(self.lhs)
        # rhs = CONTXET.get_compare_value(self.rhs)
        # match self.relation:
        #     case "!=": return lhs != rhs
        #     case ">=": return lhs >= rhs
        #     case "<=": return lhs <= rhs
        #     case "=": return lhs == rhs
        #     case ">": return lhs > rhs
        #     case "<": return lhs < rhs
        #     case _: raise
    def format(self, indent_count):
        return f"{self.lhs} {self.relation} {self.rhs}"

""" class ScopeCompare(CompareBase):
    pass
    # def is_satisfied(self):
        # return True

class VariableCompare(CompareBase):
    pass """

class Trigger(Limit):
    key: str
    limit: Limit
    def __init__(self, key: str, limit: list[Limit]|Limit):
        self.key = key
        self.limit = AND(limit) if isinstance(limit, list) else limit
    def is_satisfied(self):
        return self.limit.is_satisfied()
    def format(self, indent_count):
        return curly_braces(0, self.key, [self.limit.format(indent_count+1)])
    def __call__(self, *args, **kwds):
        return TriggerCall(self)

class TriggerCall(Limit):
    trigger: Trigger
    def __init__(self, trigger: Trigger) -> None:
        self.trigger = trigger
    def is_satisfied(self) -> bool:
        return self.trigger.is_satisfied()
    def format(self, indent_count: int) -> str:
        return f"{self.trigger.key} = yes"
