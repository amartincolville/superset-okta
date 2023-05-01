#!/usr/bin/env python

"""Tests for `superset_okta` package."""


import unittest
from click.testing import CliRunner

from superset_okta import superset_okta
from superset_okta import cli


class TestSuperset_okta(unittest.TestCase):
    """Tests for `superset_okta` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'superset_okta.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
