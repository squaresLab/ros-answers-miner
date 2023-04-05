# -*- coding: utf-8 -*-
"""
This module provides data structures that represent the contents of ROS
Answers.
"""
__all__ = ('Answer', 'Comment', 'Question', 'User')

from typing import AbstractSet

import attr


class User:
    url: str

    def __init__(self, url: str):
        self.url = url

    def __key(self):
        return (self.url)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, User) and self.__key() == other.__key()


class Comment:
    date: str
    votes: int
    content: str

    user: User

    def __init__(self, date, votes, content, user):
        self.date = date
        self.votes = votes
        self.content = content
        self.user = user

    def __key(self):
        return (self.votes, self.content)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, Comment) and self.__key() == other.__key()


class Answer:
    accepted: bool

    date: str
    votes: int
    user: User

    content: str
    comments: AbstractSet[Comment]

    def __init__(self, accepted, date, votes, user, content, comments):
        self.accepted = accepted
        self.date = date
        self.votes = votes
        self.user = user
        self.content = content
        self.comments = comments

    def __key(self):
        return (self.accepted, self.votes, self.content)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, Answer) and self.__key() == other.__key()


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

    def __init__(self, url, date, votes, views, user, title, content, tags, comments, answers):
        self.url = url
        self.date = date
        self.votes = votes
        self.views = views
        self.user = user
        self.title = title
        self.content = content
        self.tags = tags
        self.comments = comments
        self.answers = answers

    # Contains code: AbstractSet[str]
    def __key(self):
        return (self.url, self.votes, self.views, self.title)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, Question) and self.__key() == other.__key()
