import unittest

import gcl
from gcl import ast_util

class TestEnumerateScope(unittest.TestCase):
  def testSiblingsInScope(self):
    scope = readAndQueryScope('henk = 5', 1, 1)
    assert 'henk' in scope

  def testScopeObjectHasLocation(self):
    scope = readAndQueryScope('henk = 5', 1, 1)
    assert isinstance(scope['henk'], gcl.ast.TupleMemberNode)
    self.assertEquals(1, scope['henk'].location.lineno)
    self.assertEquals(1, scope['henk'].location.col)

  def testInherited(self):
    source = """
    henk = 5;
    other = {
      foo = 1;
    }
    """.strip()
    scope = readAndQueryScope(source, 3, 8) # foo
    assert 'henk' in scope
    assert 'foo' in scope

  def testCompositeNeg(self):
    source = """
    A = { henk = 5 };
    B = A { foo = 1 };
    """.strip()
    scope = readAndQueryScope(source, 2, 14)  # foo
    assert 'henk' not in scope
    assert 'foo' in scope

  def testCompositeMixin(self):
    source = """
    A = { henk = 5 };
    B = A { henk; foo = 1 };
    """.strip()
    scope = readAndQueryScope(source, 2, 14)  # foo
    assert 'henk' in scope
    assert 'foo' in scope

  def testTupleWithInherits(self):
    source = """
    henk = 5;
    B = { inherit henk }
    """.strip()
    scope = readAndQueryScope(source, 2, 14)  # inner tuple
    assert 'henk' in scope
    assert scope['henk'].location.lineno == 2  # Find the right henk

  def testIncludeDefaultBuiltins(self):
    tree = gcl.reads('henk = 5', filename='input.gcl')
    rootpath = tree.find_tokens(gcl.SourceQuery('input.gcl', 1, 1))
    return ast_util.enumerate_scope(rootpath, include_default_builtins=True)
    assert '+' in scope


def readAndQueryScope(source, line, col):
    tree = gcl.reads(source, filename='input.gcl')
    rootpath = tree.find_tokens(gcl.SourceQuery('input.gcl', line, col))
    return ast_util.enumerate_scope(rootpath)