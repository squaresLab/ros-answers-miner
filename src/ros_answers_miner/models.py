# -*- coding: utf-8 -*-
"""
This module provides data structures that represent the contents of ROS
Answers.
"""
__all__ = ('Answer', 'Comment', 'Question', 'User')

from typing import AbstractSet

import attr

@attr.s(auto_attribs=True, frozen=True)
class User:
    url: str

@attr.s(auto_attribs=True)
class Comment:
    date: str
    votes: int
    content: str
    
    user: User

@attr.s(auto_attribs=True)
class Answer:
    accepted: bool

    date: str
    votes: int
    user: User

    content: str
    comments: AbstractSet[Comment]

@attr.s(auto_attribs=True)
class Question:
    # Default information about a question
    url: str
    date: str
    votes: int
    views: int
    user: User
    
    # Content of the question
    title: str
    content: str

    # Tags, comments and answers
    tags: AbstractSet[str]
    comments: AbstractSet[Comment]
    answers: AbstractSet[Answer]
    