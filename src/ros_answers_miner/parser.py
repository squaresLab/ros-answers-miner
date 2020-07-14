# -*- coding: utf-8 -*-
"""
This module provides a simple interface for scraping all relevant information
from a given ROS Answers URL.
"""
# after the loguru import
import requests

__all__ = ('url_to_question',)

from loguru import logger

from .models import Question
from urllib.parse import urlparse

def url_to_question(url: str) -> Question:
    """Produces a summary of the question at a given URL on ROS Answers.

    Raises
    ------
    KeyError
        If there is no question at the given URL.
    """
    logger.info(f'scraping question info at URL: {url}')
    question_id = 299232
    scrape_question(question_id)

    

def question_id_from_url(url: str) -> int:
    print('**************')
       
    
def scrape_question(question_id: int) -> Question:
    # TODO compute question_url using question_id
    question_url = f'https://answers.ros.org/api/v1/questions/{question_id}'
    r = requests.get(question_url)
    json_question = r.json()
    print(json_question)    

