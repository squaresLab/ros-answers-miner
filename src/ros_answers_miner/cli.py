# -*- coding: utf-8 -*-
import argparse

from ros_answers_miner.parser import url_to_question


def scrap(args: argparse.Namespace) -> None:
    question = url_to_question(args.url)

def main() -> None:
    parser = argparse.ArgumentParser('ros-answers-miner')
    subparsers = parser.add_subparsers()

    p = subparsers.add_parser(
        'scrap',
        help='extracts information from a given ROS Answers question URL.')
    p.add_argument('url', type=str, help='the URL of the ROS Answers question')
    p.set_defaults(func=scrap)

    args = parser.parse_args()
    
    if 'func' in args:
        args.func(args)
