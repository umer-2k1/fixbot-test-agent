"""Unit tests for FixBot components."""

import pytest
import sys
import os

# Add parent directory to path to import fixbot module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fixbot import (
    TestFailure,
    FixSuggestion,
    TestRunner,
    FailureAnalyzer,
    FixGenerator,
)


class TestTestRunner:
    """Tests for TestRunner class."""
    
    def test_parse_failures_with_pytest_output(self):
        """Test parsing pytest failure output."""
        runner = TestRunner()
        output = """
        FAILED tests/test_example.py::test_addition - AssertionError: assert 5 == 6
        FAILED tests/test_example.py::test_subtraction - AssertionError: assert 3 == 2
        """
        
        failures = runner.parse_failures(output)
        
        assert len(failures) == 2
        assert failures[0].test_name == "test_addition"
        assert failures[0].file_path == "tests/test_example.py"
        assert "AssertionError" in failures[0].error_message


class TestFailureAnalyzer:
    """Tests for FailureAnalyzer class."""
    
    def test_classify_assertion_error(self):
        """Test classification of assertion errors."""
        analyzer = FailureAnalyzer()
        failure = TestFailure(
            test_name="test_foo",
            error_message="AssertionError: assert 5 == 6",
            traceback="",
            file_path="test.py"
        )
        
        analysis = analyzer.analyze_failure(failure)
        
        assert analysis['failure_type'] == 'assertion'
    
    def test_classify_import_error(self):
        """Test classification of import errors."""
        analyzer = FailureAnalyzer()
        failure = TestFailure(
            test_name="test_import",
            error_message="ModuleNotFoundError: No module named 'foo'",
            traceback="",
            file_path="test.py"
        )
        
        analysis = analyzer.analyze_failure(failure)
        
        assert analysis['failure_type'] == 'import'
    
    def test_identify_causes(self):
        """Test identifying likely causes."""
        analyzer = FailureAnalyzer()
        failure = TestFailure(
            test_name="test_assert",
            error_message="AssertionError: Expected value not found",
            traceback="",
            file_path="test.py"
        )
        
        analysis = analyzer.analyze_failure(failure)
        causes = analysis['likely_causes']
        
        assert len(causes) > 0
        assert any('assertion' in cause.lower() for cause in causes)


class TestFixGenerator:
    """Tests for FixGenerator class."""
    
    def test_extract_missing_module(self):
        """Test extracting module name from error message."""
        generator = FixGenerator()
        error_msg = "ModuleNotFoundError: No module named 'requests'"
        
        module = generator._extract_missing_module(error_msg)
        
        assert module == "requests"
    
    def test_generate_explanation(self):
        """Test generating fix explanation."""
        generator = FixGenerator()
        failure = TestFailure(
            test_name="test_foo",
            error_message="AssertionError: assert 5 == 6",
            traceback="",
            file_path="test.py"
        )
        analysis = {
            'failure_type': 'assertion',
            'likely_causes': ['Incorrect expected value']
        }
        
        explanation = generator._generate_explanation(failure, analysis, 'assertion')
        
        assert 'test_foo' in explanation
        assert 'assertion' in explanation.lower()
