# -*- coding: utf-8 -*-
import argparse

from .parser import url_to_question


def scrape(args: argparse.Namespace) -> None:
    url = args.url
    question = url_to_question(url)
    print(question)


def main() -> None:
    parser = argparse.ArgumentParser('ros-answers-miner')
    subparsers = parser.add_subparsers()

    p = subparsers.add_parser(
        'scrape',
        help='extracts information from a given ROS Answers question URL')
    p.add_argument('url', type=str, help='the URL of the ROS Answers question')
    p.set_defaults(func=scrape)

    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
