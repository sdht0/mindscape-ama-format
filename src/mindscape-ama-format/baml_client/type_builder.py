###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml-py
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off
import typing
from baml_py.baml_py import FieldType, EnumValueBuilder, EnumBuilder, ClassBuilder
from baml_py.type_builder import TypeBuilder as _TypeBuilder, ClassPropertyBuilder, ClassPropertyViewer, EnumValueViewer
from .globals import DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_RUNTIME


class TypeBuilder(_TypeBuilder):
    def __init__(self):
        super().__init__(classes=set(
          ["QuestionExtraction","Snippets",]
        ), enums=set(
          []
        ), runtime=DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_RUNTIME)


    @property
    def QuestionExtraction(self) -> "QuestionExtractionAst":
        return QuestionExtractionAst(self)

    @property
    def Snippets(self) -> "SnippetsAst":
        return SnippetsAst(self)





class QuestionExtractionAst:
    def __init__(self, tb: _TypeBuilder):
        _tb = tb._tb # type: ignore (we know how to use this private attribute)
        self._bldr = _tb.class_("QuestionExtraction")
        self._properties: typing.Set[str] = set([ "count",  "lines", ])
        self._props = QuestionExtractionProperties(self._bldr, self._properties)

    def type(self) -> FieldType:
        return self._bldr.field()

    @property
    def props(self) -> "QuestionExtractionProperties":
        return self._props


class QuestionExtractionViewer(QuestionExtractionAst):
    def __init__(self, tb: _TypeBuilder):
        super().__init__(tb)

    
    def list_properties(self) -> typing.List[typing.Tuple[str, ClassPropertyViewer]]:
        return [(name, ClassPropertyViewer(self._bldr.property(name))) for name in self._properties]



class QuestionExtractionProperties:
    def __init__(self, bldr: ClassBuilder, properties: typing.Set[str]):
        self.__bldr = bldr
        self.__properties = properties

    

    @property
    def count(self) -> ClassPropertyViewer:
        return ClassPropertyViewer(self.__bldr.property("count"))

    @property
    def lines(self) -> ClassPropertyViewer:
        return ClassPropertyViewer(self.__bldr.property("lines"))

    

class SnippetsAst:
    def __init__(self, tb: _TypeBuilder):
        _tb = tb._tb # type: ignore (we know how to use this private attribute)
        self._bldr = _tb.class_("Snippets")
        self._properties: typing.Set[str] = set([ "question_found",  "question_snippet",  "answer_found",  "answer_snippet", ])
        self._props = SnippetsProperties(self._bldr, self._properties)

    def type(self) -> FieldType:
        return self._bldr.field()

    @property
    def props(self) -> "SnippetsProperties":
        return self._props


class SnippetsViewer(SnippetsAst):
    def __init__(self, tb: _TypeBuilder):
        super().__init__(tb)

    
    def list_properties(self) -> typing.List[typing.Tuple[str, ClassPropertyViewer]]:
        return [(name, ClassPropertyViewer(self._bldr.property(name))) for name in self._properties]



class SnippetsProperties:
    def __init__(self, bldr: ClassBuilder, properties: typing.Set[str]):
        self.__bldr = bldr
        self.__properties = properties

    

    @property
    def question_found(self) -> ClassPropertyViewer:
        return ClassPropertyViewer(self.__bldr.property("question_found"))

    @property
    def question_snippet(self) -> ClassPropertyViewer:
        return ClassPropertyViewer(self.__bldr.property("question_snippet"))

    @property
    def answer_found(self) -> ClassPropertyViewer:
        return ClassPropertyViewer(self.__bldr.property("answer_found"))

    @property
    def answer_snippet(self) -> ClassPropertyViewer:
        return ClassPropertyViewer(self.__bldr.property("answer_snippet"))

    




__all__ = ["TypeBuilder"]
