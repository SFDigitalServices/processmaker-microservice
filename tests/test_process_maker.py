"""Tests for Process Maker package"""
from unittest import TestCase
from service.resources.process_maker import ProcessMaker

def test_get_token_error():
    """ test get_token method error """

    username = "username"
    password = "password"
    scope = "scope"
    workspace = "workspace"

    process_maker = ProcessMaker()
    test_case = TestCase()
    with test_case.assertRaises(ValueError):
        process_maker.get_token(username, password, scope, workspace)

def test_post_error():
    """ test post method error """

    process_maker = ProcessMaker()
    test_case = TestCase()
    with test_case.assertRaises(ValueError):
        process_maker.post("path")
