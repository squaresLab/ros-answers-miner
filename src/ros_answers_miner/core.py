# -*- coding: utf-8 -*-
"""
This module provides data structures that represent the contents of ROS
Answers.
"""
__all__ = ('Question', 'Answer', 'Comment')

from typing import AbstractSet

import attr


@attr.s(auto_attribs=True)
class Question:
    url: str
    tags: AbstractSet[str]


@attr.s(auto_attribs=True)
class Answer:
    accepted: bool


@attr.s(auto_attribs=True)
class Comment:
    contents: str
