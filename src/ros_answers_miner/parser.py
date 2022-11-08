# -*- coding: utf-8 -*-
"""
This module provides a simple interface for scraping all relevant information
from a given ROS Answers URL.
"""
__all__ = ('url_to_question',)

import logging
import requests

from bs4 import BeautifulSoup
from typing import AbstractSet

from ros_answers_miner.models import Question, Answer, Comment, User

def build_link(url: str) -> str:
    """Builds a link to a ROS Answers page.

    Parameters
    ----------
    url : str
        The relative URL of the ROS Answers page.

    Returns
    -------
    str
        The final URL of the ROS Answers page.
    """
    return f'https://answers.ros.org/{url}'


def scrap_user(soup: BeautifulSoup) -> User:
    user_card = soup.find_all("div", {"class": "user-card"})

    # From user_card, obtain the link with class js-avatar-box
    link = user_card[0].find_all("a", {"class": "js-avatar-box"})[0]['href']
    
    return User(build_link(link))

def scrap_answer(soup: BeautifulSoup) -> AbstractSet[Answer]:
    
    # Get the div with the class post-body from the soup
    answers = soup.find_all("div", {"class": "post-body"})[1:]

    # Get span with class next 
    next = soup.find("span", {"class": "next"})
    next_link = next.find_all("a")[0]['href']

    # Gather all the answers
    while 'page=None' not in next_link:

        # Get the link from the next span
        next_link = next.find_all("a")[0]['href']
        
        # Get the soup from the link
        curr_soup: BeautifulSoup = BeautifulSoup(requests.get(build_link(next_link)).content, 'html.parser')
        
        # Get the div with the class post-body from the soup
        answers += curr_soup.find_all("div", {"class": "post-body"})[1:]

        # Get span with class next 
        next = curr_soup.find("span", {"class": "next"})
        next_link = next.find_all("a")[0]['href']
    
    for answer in answers:

        # Get div with class js-editable-content from the answer
        content = answer.find("div", {"class": "js-editable-content"})

        # Get the body from p from the content
        content = content.find("p").text
  
        # Get the title from the abbr with the class timeago
        date = answer.find("abbr", {"class": "timeago"})['title']



        break

    pass

def scrap_comment(soup: BeautifulSoup) -> AbstractSet[Comment]:
    pass


def scrap_question_info(soup: BeautifulSoup) -> tuple:
    
    # Get the div with the class post-body from the soup
    question = soup.find_all("div", {"class": "post-body"})[0]

    pass

def url_to_question(url: str) -> Question:
    """Produces a summary of the question at a given URL on ROS Answers.

    Raises
    ------
    KeyError
        If there is no question at the given URL.
    """
    logging.info(f'scraping question info at URL: {url}')
    
    # Obtain the question page
    soup: BeautifulSoup = BeautifulSoup(requests.get(url).content, 'html.parser')

    # Obtain the question information
    user: User = scrap_user(soup)
    answers: AbstractSet[Answer] = scrap_answer(soup)
    
    print(answers)
    assert False
    comments: AbstractSet[Comment] = scrap_comment(soup)
    
    date, votes, views, title, content, tags = scrap_question_info(soup)
    
    logging.info(f'scraping question info at URL: {url} - done')

    return Question(url, date, votes, views, user, title, content, tags, comments, answers)