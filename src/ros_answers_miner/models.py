# -*- coding: utf-8 -*-
"""
This module provides data structures that represent the contents of ROS
Answers.
"""
__all__ = ('Answer', 'Comment', 'Question', 'User')

from sortedcollections import OrderedSet

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

    def to_json(self):
        return {
            '__class__': 'User',
            'url': self.url
        }


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

    def to_json(self):
        return {
            '__class__': 'Comment',
            'date': str(self.date),
            'votes': self.votes,
            'content': self.content,
            'user': self.user.to_json()
        }


class Answer:
    accepted: bool

    date: str
    votes: int
    user: User

    content: str
    comments: OrderedSet[Comment]

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

    def to_json(self):
        return {
            '__class__': 'Answer',
            'accepted': self.accepted,
            'date': str(self.date),
            'votes': self.votes,
            'user': self.user.to_json(),
            'content': self.content,
            'comments': OrderedSet([comment.to_json() for comment in self.comments])
        }


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
    tags: OrderedSet[str]
    comments: OrderedSet[Comment]
    answers: OrderedSet[Answer]

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

    def to_json(self):
        return {
            '__class__': 'Question',
            'url': self.url,
            'date': str(self.date),
            'votes': self.votes,
            'views': self.views,
            'user': self.user.to_json(),
            'title': self.title,
            'content': self.content,
            'tags': OrderedSet(list(self.tags)),
            'comments': OrderedSet([comment.to_json() for comment in self.comments]),
            'answers': OrderedSet([answer.to_json() for answer in self.answers])
        }
