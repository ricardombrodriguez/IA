

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

from typing import Any


class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:

    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl

    def __str__(self):
        return str(self.declarations)

    def insert(self,decl):
        self.declarations.append(decl)

    def query_local(self,user=None,e1=None,rel=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result

    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    def list_associations(self):
        return list(set([decl.relation.name for decl in self.declarations if type(decl.relation) is Association and decl.relation.name]))

    def list_objects(self):
        return list(set([decl.relation.entity1 for decl in self.declarations if type(decl.relation) is Member and decl.relation.entity1]))

    def list_users(self):
        return list(set([decl.user for decl in self.declarations]))

    def list_types(self):
        subtypes = set([decl.relation.entity1 and decl.relation.entity2 for decl in self.declarations if type(decl.relation) is Subtype])
        members = set([decl.relation.entity2 for decl in self.declarations if type(decl.relation) is Member])
        return list(set.union(subtypes, members))

    def list_local_associations(self, entity1):
        return list(set([decl.relation.name for decl in self.declarations if type(decl.relation) is Association and decl.relation.entity1 == entity1]))

    def list_relations_by_user(self, user):
        return list(set([decl.relation.name for decl in self.declarations if decl.user == user]))

    def associations_by_user(self, user):
        return len(set([decl.relation.name for decl in self.declarations if decl.user == user and type(decl.relation) is Association]))

    def list_local_associations_by_user(self,user):
        return list(set([(decl.relation.name, decl.user) for decl in self.declarations if decl.relation.entity1 == user and type(decl.relation) is Association]))

    def predecessor(self,A,B):

        relations = [d.relation.entity1 for d in self.declarations if type(d.relation) in [Member, Subtype] and d.relation.entity2 == A]
        for entity in relations:
            if entity == B:
                return True
        for entity in relations:
            if self.predecessor(entity, B):
                return True
        return False

    def predecessor_path(self,A,B):
        
        relations = [d.relation.entity1 for d in self.declarations if type(d.relation) in [Member, Subtype] and d.relation.entity2 == A]
        for entity in relations:
            if entity == B:
                return [A,B]
        for entity in relations:
            if self.predecessor(entity,B) is not None:
                return [A] + self.predecessor_path(entity, B)
        return []

    def query(self,entity,association=None):

        relations = [d.relation.entity2 for d in self.declarations if type(d.relation) in [Member, Subtype] and d.relation.entity1 == entity]
        declarations = [d for d in self.declarations if type(d.relation) == Association and d.relation.entity1 == entity] if association is None \
            else [d for d in self.declarations if type(d.relation) == Association and d.relation.name == association and d.relation.entity1 == entity]
        for super in relations:
            if self.query(super,association) is not None:
                declarations += self.query(super,association)
        return declarations


    def query2(self,entity,association=None):

        relations = [d.relation.entity2 for d in self.declarations if type(d.relation) in [Member, Subtype] and d.relation.entity1 == entity]
        declarations = [d for d in self.declarations if d.relation.entity1 == entity] if association is None \
            else [d for d in self.declarations if d.relation.name == association and d.relation.entity1 == entity]
        for super in relations:
            if self.query(super,association) is not None:
                declarations += self.query(super,association)
        return declarations

    def query_cancel(self,entity,association=None):

        relations = [d.relation.entity2 for d in self.declarations if type(d.relation) in [Member] and d.relation.entity1 == entity]
        declarations = [d for d in self.declarations if d.relation.entity1 == entity] if association is None \
            else [d for d in self.declarations if d.relation.name == association and d.relation.entity1 == entity]
        for super in relations:
            if self.query_cancel(super,association) is not None:
                declarations += self.query_cancel(super,association)
        return declarations

    def query_down(self,entity,association=None):

        descendents = [d.relation.entity1 for d in self.declarations if type(d.relation) in [Member, Subtype] and d.relation.entity2 == entity]
        declarations = []
        for desc in descendents:
            if self.query_down(desc,association) is not None:
                declarations += self.query_down(desc,association)
        declarations = [d for d in self.declarations if d.relation.entity1 == entity] if association is None \
            else [d for d in self.declarations if d.relation.name == association and d.relation.entity1 == entity]
        return declarations