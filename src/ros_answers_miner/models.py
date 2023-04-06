# -*- coding: utf-8 -*-
"""
This module provides data structures that represent the contents of ROS
Answers.
"""
__all__ = ('Answer', 'Comment', 'Question', 'User')

import attr
from sortedcollections import OrderedSet


@attr.s(auto_attribs=True, hash=True, eq=True)
class User:
    url: str

    def to_json(self):
        return {'__class__': 'User', 'url': self.url}


@attr.s(auto_attribs=True, hash=True, eq=True)
class Comment:
    date: str
    votes: int
    content: str

    user: User

    def to_json(self):
        return {
            '__class__': 'Comment',
            'date': str(self.date),
            'votes': self.votes,
            'content': self.content,
            'user': self.user.to_json()
        }


@attr.s(auto_attribs=True, hash=True, eq=True)
class Answer:
    accepted: bool
    date: str
    votes: int
    user: User

    content: str
    comments: OrderedSet[Comment] = attr.ib(hash=False, eq=False)

    def to_json(self):
        return {
            '__class__':
            'Answer',
            'accepted':
            self.accepted,
            'date':
            str(self.date),
            'votes':
            self.votes,
            'user':
            self.user.to_json(),
            'content':
            self.content,
            'comments':
            OrderedSet([comment.to_json() for comment in self.comments])
        }


@attr.s(auto_attribs=True, hash=True, eq=True)
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
    tags: OrderedSet[str] = attr.ib(hash=False, eq=False)
    comments: OrderedSet[Comment] = attr.ib(hash=False, eq=False)
    answers: OrderedSet[Answer] = attr.ib(hash=False, eq=False)

    def to_json(self):
        return {
            '__class__':
            'Question',
            'url':
            self.url,
            'date':
            str(self.date),
            'votes':
            self.votes,
            'views':
            self.views,
            'user':
            self.user.to_json(),
            'title':
            self.title,
            'content':
            self.content,
            'tags':
            OrderedSet(list(self.tags)),
            'comments':
            OrderedSet([comment.to_json() for comment in self.comments]),
            'answers':
            OrderedSet([answer.to_json() for answer in self.answers])
        }
