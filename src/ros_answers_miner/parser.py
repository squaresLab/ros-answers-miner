# -*- coding: utf-8 -*-
"""
This module provides a simple interface for scraping all relevant information
from a given ROS Answers URL.
"""
__all__ = ('url_to_question', )

import logging
import requests
from datetime import datetime

from bs4 import BeautifulSoup
from typing import AbstractSet

from ros_answers_miner.models import Question, Answer, Comment, User


def build_link(url: str) -> str:
    return f'https://answers.ros.org/{url}'


def scrap_user(soup: BeautifulSoup) -> User:
    user_card = soup.find_all("div", {"class": "user-card"})

    # From user_card, obtain the link with class js-avatar-box
    if user_card != []:
        link = user_card[0].find_all("a",
                                     {"class": "js-avatar-box"})[0]['href']
        link = build_link(link[1:])
    else:
        link = 'deleted'

    return User(build_link(link))


def scrap_answer(soup: BeautifulSoup) -> AbstractSet[Answer]:

    result = list()

    # Get the div with the class post-body from the soup
    answers = soup.find_all("div", {"class": "post answer"})

    # Get span with class next
    next = soup.find("span", {"class": "next"})

    if next:
        next_link = next.find_all("a")[0]['href']

        # Gather all the answers
        while 'page=None' not in next_link:

            # Get the link from the next span
            next_link = next.find_all("a")[0]['href']

            # Get the soup from the link
            curr_soup: BeautifulSoup = BeautifulSoup(
                requests.get(build_link(next_link)).content, 'html.parser')

            # Get the div with the class post-body from the soup
            answers += curr_soup.find_all("div", {"class": "post answer"})

            # Get span with class next
            next = curr_soup.find("span", {"class": "next"})
            next_link = next.find_all("a")[0]['href']

    # Get the accepted anser
    accepted_answer = soup.find("div",
                                {"class": "post answer accepted-answer"})

    if accepted_answer is not None:
        answers.insert(0, accepted_answer)

    # Obtain the information from the answers. Build the Answer object
    for i, ans in enumerate(answers):

        # These type of answers are not accepted
        accepted = False

        if i == 0 and accepted_answer is not None:
            accepted = True

        # Get content of the answer
        content = str(ans.find("div", {"class": "js-editable-content"}))

        # Get the date of the answer
        date = ans.find("abbr", {"class": "timeago"})['title']
        date = datetime.strptime(date[:-6], '%Y-%m-%d %H:%M:%S')

        # Get the votes of the answer
        votes = int(ans.find("div", {"class": "vote-number"}).text)

        # Get the user of the answer
        user = ans.find("div", {"class": "user-info"})

        # If the user does not exist, it is a deleted user
        if user is not None:
            user_link = build_link(user.find("a")['href'][1:])
        else:
            user_link = 'deleted'

        user = User(user_link)

        # Get the comments of the answer
        comments = scrap_comment(ans)

        # Build the answer
        answer = Answer(accepted, date, votes, user, content, comments)

        result.append(answer)

    return result


def scrap_comment(soup: BeautifulSoup) -> AbstractSet[Comment]:

    # Get the list of comments from the comments div with class comment js-comment
    comms = soup.find("div", {"class": "comments"})
    comms = comms.find_all("div", {"class": "comment js-comment"})

    comments = list()

    for comment in comms:

        # Get the vote of the comment from the div with the class upvote js-score
        comment_vote = comment.find("div", {"class": "upvote js-score"}).text

        if comment_vote == '':
            comment_vote = 0

        # Get the comment content from the div with the class comment-body
        comment_content = str(comment.find("div", {"class": "comment-body"}))

        # Get the comment author from the a href with the class author
        comment_author = comment.find("a", {"class": "author"})

        if comment_author is not None:
            comment_author = comment_author['href'][1:]
        else:
            comment_author = 'deleted'

        comment_author = User(build_link(comment_author))

        # Get the comment date from the abbr with the class timeago
        comment_date = comment.find("abbr", {"class": "timeago"})['title']
        comment_date = datetime.strptime(comment_date[:-6],
                                         '%Y-%m-%d %H:%M:%S')

        # Build the comment
        comment = Comment(comment_date, comment_vote, comment_content,
                          comment_author)
        comments.append(comment)

    return comments


def scrap_question_info(soup: BeautifulSoup) -> tuple:

    # Get the date of the question from the abbr with the class timeago
    date = soup.find("abbr", {"class": "timeago"})['title']
    date = datetime.strptime(date[:-6], '%Y-%m-%d %H:%M:%S')

    # Get the question number of votes from the div with the vote-number class
    votes = int(soup.find("div", {"class": "vote-number"}).text)

    # Get the question title
    title = soup.find(
        "h1", {"id": lambda l: l and l.startswith('js-question-title')})
    title = title.find("div", {"class": "js-editable-content"}).text

    # Get the question content. TODO: The images are not being scraped
    content = soup.find("div",
                        {"id": lambda l: l and l.startswith('js-post-body')})
    content = str(content.find("div", {"class": "js-editable-content"}))

    # Get the list of tags in a question from the ul with id question-tags. The name is saved in the text
    tags = soup.find("ul", {
        "id": "question-tags"
    }).find_all("a", {"class": "js-tag-name"})
    tags = [tag.text for tag in tags]

    return date, votes, title, content, tags


def url_to_question(url: str) -> Question:
    """Produces a summary of the question at a given URL on ROS Answers.

    Raises
    ------
    KeyError
        If there is no question at the given URL.
    """
    logging.info(f'scraping question info at URL: {url}')

    # Obtain the question page
    soup: BeautifulSoup = BeautifulSoup(
        requests.get(url).content, 'html.parser')

    question_soup = soup.find("div", {"class": "post js-question"})

    # Obtain the question information
    user: User = scrap_user(soup)
    answers: AbstractSet[Answer] = scrap_answer(soup)

    # Obtain the comments for the question
    comments: AbstractSet[Comment] = scrap_comment(question_soup)

    date, votes, title, content, tags = scrap_question_info(question_soup)

    # Obtain the div with class box statsWidget
    stats = soup.find("div", {"class": "box statsWidget"})
    views = stats.find_all("p")[1].text.strip().split(" ")[1]
    views = int(views.replace(",", ""))

    logging.info(f'scraping question info at URL: {url} - done')

    question = Question(url, date, votes, views, user, title, content, tags,
                        comments, answers)
    return question
