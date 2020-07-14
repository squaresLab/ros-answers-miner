# -*- coding: utf-8 -*-
import argparse

from .parser import scrape_question


def scrape(args: argparse.Namespace) -> None:
    url = args.url   #todo fix for question
    question = url_to_question(url) #todo fix for question_id?
    print(question) #todo fix


def main() -> None:
    parser = argparse.ArgumentParser('ros-answers-miner')
    subparsers = parser.add_subparsers()

    p = subparsers.add_parser(
        'scrape',
        help='extracts information for a given ROS Answers question ID')
    p.add_argument('id', type=int, help='the ID of the ROS Answers question')
    p.set_defaults(func=scrape)

    args = parser.parse_args()
    if 'func' in args:
        args.func(args)