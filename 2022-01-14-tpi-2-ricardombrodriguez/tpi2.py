#encoding: utf8

from semantic_network import *
from bayes_net import *

from itertools import product

class MySemNet(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)

    def source_confidence(self,user):
        correct,wrong = 0,0
        assocOneDeclarations = list(set([decl for decl in self.declarations if type(decl.relation) is AssocOne]))
        assocOneUser = [decl for decl in assocOneDeclarations if decl.user == user]
        for userDecl in assocOneUser:
            similarDecl = [decl for decl in assocOneDeclarations if decl.relation.entity1 == userDecl.relation.entity1 \
                                                                and decl.relation.name == userDecl.relation.name]
            incidence = {}
            for decl in similarDecl:
                if decl.relation.entity2 not in incidence:
                    incidence[decl.relation.entity2] = 1
                else:
                    incidence[decl.relation.entity2] += 1
            if incidence[userDecl.relation.entity2] == max(incidence.values()):
                correct += 1
            else:
                wrong += 1
        return self.conf1(correct,wrong)

    def query_with_confidence(self,entity,assoc):

        parents_confidence = [self.query_with_confidence(decl.relation.entity2, assoc) for decl in self.declarations if decl.relation.entity1 == entity and (decl.relation.name == "subtype" or decl.relation.name == "member")]

        assocOneDeclarations = list(set([decl for decl in self.declarations if type(decl.relation) is AssocOne]))
        similarEntities = [decl.relation.entity2 for decl in assocOneDeclarations if decl.relation.entity1 == entity and decl.relation.name == assoc]

        ocorrences = { entity2 : self.conf2(similarEntities.count(entity2), len(similarEntities)) for entity2 in set(similarEntities)}

        parent_ocorrences = {}

        for parent in parents_confidence:

            for entity,value in parent.items():

                if entity not in parent_ocorrences:
                    parent_ocorrences[entity] = value

                else:
                    parent_ocorrences[entity] += value
                        
        for key,value in parent_ocorrences.items():
            parent_ocorrences[key] = value / len(parents_confidence)

        # results from heritage
        if not ocorrences and parent_ocorrences:

            for k in parent_ocorrences:
                parent_ocorrences[k] *= 0.9

            return parent_ocorrences

        # local results + heritage results
        elif ocorrences and parent_ocorrences:

            for k,v in parent_ocorrences.items():

                if k not in ocorrences:
                    ocorrences[k] = 0.1 * v
                else:
                    ocorrences[k] = 0.9 * ocorrences[k] + 0.1 * v

            for k in ocorrences:

                if k not in parent_ocorrences:
                    ocorrences[k] *= 0.9

            return ocorrences

        # only local results
        else:
            return ocorrences

    def conf1(self,correct,wrong):
        return (1-0.75**correct)*0.75**wrong

    def conf2(self,n,T):
        return n/(2*T) + (1-n/(2*T))*(1-0.95**n)*0.95**(T-n)


class MyBN(BayesNet):

    def __init__(self):
        BayesNet.__init__(self)
        pass

    def individual_probabilities(self):

        variables = [var for var in self.dependencies.keys()]
        probabilities = {}

        for var in variables:
            other_variables = [key for key in variables if key != var]
            variable_conjunctions = self.conjunctions(other_variables)
            joint_probs = [self.jointProb([(var,True)] + conjuction) for conjuction in variable_conjunctions]
            probabilities[var] = sum(joint_probs)
        
        return probabilities

    def conjunctions(self, other_variables):

        variable_conjunctions = []
        if len(other_variables) == 1:
            return [[(other_variables[0],True)],[(other_variables[0],False)]]   #end
        
        for conjuction in self.conjunctions(other_variables[1:]):
            variable_conjunctions.append([(other_variables[0],True)] + conjuction)
            variable_conjunctions.append([(other_variables[0],False)] + conjuction)

        return variable_conjunctions


