#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, argparse

from bar.network.bar_server import bar_server

def parse_cli():

    parser = argparse.ArgumentParser(
    prog = "Bar Server", # %(prog)s : used to display the prog variable whenever you want
    usage = """%(prog)s ->"""
,
description="""
This is a bar server . Follow the commands to start the Bar Server

python2  bin/bar bar_server start
    """,

    epilog = "This is the Bar Server for anonymous communication and broadcasting",
    )

    subparsers = parser.add_subparsers(title='subcommands',
                                    description='This is the subcommands',
                                    help='additional help',
                                    dest = 'operation')

    barserver_parser = subparsers.add_parser('BARserver')


    subparsers = barserver_parser.add_subparsers(help='sub-command help', dest='BARserver_operation')

    startbarserver_parser = subparsers.add_parser('start', help='Subparser for starting the BAR server.')
    barserver_parser.add_argument('--name',help='Subparser for specifing a port number.' , required = True)
    barserver_parser.add_argument('--onport', type = int ,help='Subparser for specifing a port number.')

    return parser

def start_barserver(args):
    default = 6881
    if args.onport and args.name:
        bar_server(args.onport,args.name)
    else:
        bar_server(default)

def stop_barserver(args):
    print "stop_barserver"

def caller(func, args):

    return func(args)


def pybar():

    operations = {
        "BARserver":{
                "start" : start_barserver ,
                "stop" : stop_barserver
    } }
    parser = parse_cli()
    args = parser.parse_args()
    if type(operations[args.operation]) is dict:
        caller(operations[args.operation][getattr(args, args.operation + "_operation")], args)
    else:
        caller(operations[args.operation], args)

def run():
    pybar()
