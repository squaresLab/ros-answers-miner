# -*- coding: utf-8 -*-
"""
This module provides a simple interface for scraping all relevant information
from a given ROS Answers URL.
"""
__all__ = ('url_to_question',)

from loguru import logger

from .models import Question


def url_to_question(url: str) -> Question:
    """Produces a summary of the question at a given URL on ROS Answers.

    Raises
    ------
    KeyError
        If there is no question at the given URL.
    """
    logger.info(f'scraping question info at URL: {url}')
    raise NotImplementedError
