#!/usr/bin/env python3
"""
FixBot - AI Test Auto-Fix Agent

An intelligent agent that automatically detects and fixes failing tests using AI-powered analysis.
"""

import os
import re
import subprocess
import sys
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import json


@dataclass
class TestFailure:
    """Represents a test failure with context."""
    test_name: str
    error_message: str
    traceback: str
    file_path: str
    line_number: Optional[int] = None


@dataclass
class FixSuggestion:
    """Represents a suggested fix for a test failure."""
    file_path: str
    original_code: str
    fixed_code: str
    explanation: str


class TestRunner:
    """Handles running tests and collecting failure information."""
    
    def __init__(self, test_command: str = "pytest"):
        self.test_command = test_command
    
    def run_tests(self, test_path: str = ".") -> Tuple[bool, str]:
        """
        Run tests and return success status and output.
        
        Args:
            test_path: Path to test directory or specific test file
            
        Returns:
            Tuple of (success: bool, output: str)
        """
        try:
            result = subprocess.run(
                [self.test_command, test_path, "-v"],
                capture_output=True,
                text=True,
                timeout=60
            )
            output = result.stdout + result.stderr
            return result.returncode == 0, output
        except subprocess.TimeoutExpired:
            return False, "Test execution timed out"
        except Exception as e:
            return False, f"Error running tests: {str(e)}"
    
    def parse_failures(self, output: str) -> List[TestFailure]:
        """
        Parse test output to extract failure information.
        
        Args:
            output: Test runner output
            
        Returns:
            List of TestFailure objects
        """
        failures = []
        
        # Parse pytest-style output
        # Looking for patterns like:
        # FAILED tests/test_example.py::test_addition - AssertionError: ...
        failure_pattern = r'FAILED\s+([^\s]+)\s+-\s+(.+)'
        
        for match in re.finditer(failure_pattern, output):
            test_path = match.group(1)
            error_msg = match.group(2)
            
            # Extract file path and test name
            if '::' in test_path:
                file_path, test_name = test_path.split('::', 1)
            else:
                file_path, test_name = test_path, "unknown"
            
            # Try to extract traceback (simplified)
            traceback = self._extract_traceback(output, test_path)
            
            failures.append(TestFailure(
                test_name=test_name,
                error_message=error_msg,
                traceback=traceback,
                file_path=file_path
            ))
        
        return failures
    
    def _extract_traceback(self, output: str, test_path: str) -> str:
        """
        Extract traceback for a specific test from output.
        
        Parses test runner output to find and extract the traceback section
        for a specific test failure. Captures lines between the test failure
        marker and the next test result.
        
        Args:
            output: Full test runner output string
            test_path: Path identifier for the specific test (e.g., 'tests/test_foo.py::test_bar')
            
        Returns:
            Extracted traceback as a string, or empty string if not found
        """
        lines = output.split('\n')
        traceback_lines = []
        capturing = False
        
        for line in lines:
            if test_path in line and 'FAILED' in line:
                capturing = True
            elif capturing:
                if line.strip().startswith('FAILED') or line.strip().startswith('PASSED'):
                    break
                traceback_lines.append(line)
        
        return '\n'.join(traceback_lines)


class FailureAnalyzer:
    """Analyzes test failures to understand the root cause."""
    
    def analyze_failure(self, failure: TestFailure) -> Dict[str, Any]:
        """
        Analyze a test failure to determine the type and likely cause.
        
        Args:
            failure: TestFailure object
            
        Returns:
            Dictionary with analysis results
        """
        analysis = {
            'failure_type': self._classify_failure(failure.error_message),
            'likely_causes': self._identify_causes(failure),
            'context': self._extract_context(failure)
        }
        return analysis
    
    def _classify_failure(self, error_message: str) -> str:
        """Classify the type of failure based on error message."""
        if 'AssertionError' in error_message:
            return 'assertion'
        elif 'AttributeError' in error_message:
            return 'attribute'
        elif 'TypeError' in error_message:
            return 'type'
        elif 'ValueError' in error_message:
            return 'value'
        elif 'NameError' in error_message:
            return 'name'
        elif 'ImportError' in error_message or 'ModuleNotFoundError' in error_message:
            return 'import'
        else:
            return 'unknown'
    
    def _identify_causes(self, failure: TestFailure) -> List[str]:
        """Identify likely causes of the failure."""
        causes = []
        error_msg = failure.error_message.lower()
        
        if 'assert' in error_msg:
            causes.append('Incorrect expected value in assertion')
        if 'not found' in error_msg or 'does not exist' in error_msg:
            causes.append('Missing resource or method')
        if 'type' in error_msg:
            causes.append('Type mismatch')
        if 'none' in error_msg:
            causes.append('Unexpected None value')
        
        return causes if causes else ['Unknown cause']
    
    def _extract_context(self, failure: TestFailure) -> Dict[str, str]:
        """Extract contextual information from the failure."""
        return {
            'test_name': failure.test_name,
            'file': failure.file_path,
            'error': failure.error_message
        }


class FixGenerator:
    """Generates fixes for test failures using AI-powered analysis."""
    
    def generate_fix(self, failure: TestFailure, analysis: Dict) -> FixSuggestion:
        """
        Generate a fix suggestion for a test failure.
        
        Args:
            failure: TestFailure object
            analysis: Analysis results from FailureAnalyzer
            
        Returns:
            FixSuggestion object
        """
        # Read the test file
        try:
            with open(failure.file_path, 'r') as f:
                test_code = f.read()
        except FileNotFoundError:
            return FixSuggestion(
                file_path=failure.file_path,
                original_code="",
                fixed_code="",
                explanation=f"Test file not found: {failure.file_path}"
            )
        
        # Generate fix based on failure type
        failure_type = analysis.get('failure_type', 'unknown')
        fixed_code = self._apply_fix_strategy(test_code, failure, failure_type)
        
        explanation = self._generate_explanation(failure, analysis, failure_type)
        
        return FixSuggestion(
            file_path=failure.file_path,
            original_code=test_code,
            fixed_code=fixed_code,
            explanation=explanation
        )
    
    def _apply_fix_strategy(self, code: str, failure: TestFailure, failure_type: str) -> str:
        """
        Apply appropriate fix strategy based on failure type.
        
        Args:
            code: Original test code
            failure: TestFailure object with error details
            failure_type: Type of failure (assertion, import, attribute, etc.)
            
        Returns:
            Fixed code with suggested changes
        """
        
        if failure_type == 'assertion':
            return self._fix_assertion(code, failure)
        elif failure_type == 'import':
            return self._fix_import(code, failure)
        elif failure_type == 'attribute':
            return self._fix_attribute(code, failure)
        else:
            # Generic fix: add a comment suggesting manual review
            return self._add_review_comment(code, failure)
    
    def _fix_assertion(self, code: str, failure: TestFailure) -> str:
        """
        Attempt to fix assertion errors.
        
        Adds review comments to assertions that may need updating.
        
        Args:
            code: Original test code
            failure: TestFailure object
            
        Returns:
            Code with review comments added
        """
        # Example: If assertion compares expected vs actual, try to extract the actual value
        # This is a simplified example - real implementation would be more sophisticated
        
        # Look for assertion statements in the test
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if 'assert' in line.lower() and failure.test_name.replace('test_', '') in code[max(0, i-10):i+10]:
                # Add a comment suggesting review
                lines[i] = f"{line}  # FixBot: Review this assertion - may need updating"
        
        return '\n'.join(lines)
    
    def _fix_import(self, code: str, failure: TestFailure) -> str:
        """
        Attempt to fix import errors by adding missing imports.
        
        Args:
            code: Original test code
            failure: TestFailure object
            
        Returns:
            Code with missing import added, or original code if no fix found
        """
        # Check if import is missing
        missing_module = self._extract_missing_module(failure.error_message)
        if missing_module and not f"import {missing_module}" in code:
            # Add import at the top
            lines = code.split('\n')
            # Find where to insert (after existing imports)
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    insert_pos = i + 1
            lines.insert(insert_pos, f"import {missing_module}")
            return '\n'.join(lines)
        return code
    
    def _fix_attribute(self, code: str, failure: TestFailure) -> str:
        """
        Attempt to fix attribute errors by adding review comments.
        
        Args:
            code: Original test code
            failure: TestFailure object
            
        Returns:
            Code with review comment
        """
        return self._add_review_comment(code, failure)
    
    def _add_review_comment(self, code: str, failure: TestFailure) -> str:
        """
        Add a review comment to the code for manual inspection.
        
        Args:
            code: Original test code
            failure: TestFailure object
            
        Returns:
            Code with review comment prepended
        """
        comment = f"\n# FixBot: Test '{failure.test_name}' failed - {failure.error_message}\n"
        return comment + code
    
    def _extract_missing_module(self, error_message: str) -> Optional[str]:
        """
        Extract missing module name from error message.
        
        Args:
            error_message: Error message from test failure
            
        Returns:
            Module name if found, None otherwise
        """
        match = re.search(r"No module named '([^']+)'", error_message)
        if match:
            return match.group(1)
        return None
    
    def _generate_explanation(self, failure: TestFailure, analysis: Dict, failure_type: str) -> str:
        """
        Generate human-readable explanation of the fix.
        
        Args:
            failure: TestFailure object
            analysis: Analysis results from FailureAnalyzer
            failure_type: Classified failure type
            
        Returns:
            Human-readable explanation string
        """
        explanation = f"Analysis of test failure '{failure.test_name}':\n"
        explanation += f"- Failure type: {failure_type}\n"
        explanation += f"- Error: {failure.error_message}\n"
        explanation += f"- Likely causes: {', '.join(analysis.get('likely_causes', ['Unknown']))}\n"
        explanation += "\nSuggested fix has been applied. Please review and adjust as needed."
        return explanation


class CodePatcher:
    """Applies fixes to code files."""
    
    # Maximum number of diff lines to display
    MAX_DIFF_LINES = 10
    
    def apply_fix(self, suggestion: FixSuggestion, dry_run: bool = True) -> bool:
        """
        Apply a fix suggestion to the code.
        
        Args:
            suggestion: FixSuggestion object
            dry_run: If True, only show what would be changed without applying
            
        Returns:
            True if successful, False otherwise
        """
        if dry_run:
            print(f"\n{'='*60}")
            print(f"DRY RUN - Would apply fix to: {suggestion.file_path}")
            print(f"{'='*60}")
            print(suggestion.explanation)
            print(f"\n{'-'*60}")
            print("Suggested changes:")
            print(f"{'-'*60}")
            self._show_diff(suggestion.original_code, suggestion.fixed_code)
            return True
        
        try:
            # Create backup
            backup_path = f"{suggestion.file_path}.fixbot.bak"
            with open(suggestion.file_path, 'r') as f:
                original = f.read()
            with open(backup_path, 'w') as f:
                f.write(original)
            
            # Apply fix
            with open(suggestion.file_path, 'w') as f:
                f.write(suggestion.fixed_code)
            
            print(f"✓ Applied fix to {suggestion.file_path}")
            print(f"  Backup created: {backup_path}")
            return True
        except Exception as e:
            print(f"✗ Error applying fix: {str(e)}")
            return False
    
    def _show_diff(self, original: str, fixed: str):
        """
        Show a simple diff between original and fixed code.
        
        Args:
            original: Original code content
            fixed: Fixed code content
        """
        orig_lines = original.split('\n')
        fixed_lines = fixed.split('\n')
        
        # Simple line-by-line comparison
        max_lines = max(len(orig_lines), len(fixed_lines))
        
        for i in range(min(self.MAX_DIFF_LINES, max_lines)):  # Show first N lines of diff
            if i < len(orig_lines):
                print(f"  - {orig_lines[i]}")
            if i < len(fixed_lines) and (i >= len(orig_lines) or orig_lines[i] != fixed_lines[i]):
                print(f"  + {fixed_lines[i]}")


class FixBot:
    """Main FixBot agent that orchestrates the auto-fix process."""
    
    def __init__(self, test_command: str = "pytest"):
        self.test_runner = TestRunner(test_command)
        self.analyzer = FailureAnalyzer()
        self.fix_generator = FixGenerator()
        self.patcher = CodePatcher()
    
    def auto_fix(self, test_path: str = ".", dry_run: bool = True, max_attempts: int = 3) -> bool:
        """
        Automatically detect and fix failing tests.
        
        Args:
            test_path: Path to test directory or file
            dry_run: If True, show fixes without applying them
            max_attempts: Maximum number of fix attempts
            
        Returns:
            True if all tests pass, False otherwise
        """
        print("🤖 FixBot - AI Test Auto-Fix Agent")
        print("="*60)
        
        for attempt in range(1, max_attempts + 1):
            print(f"\n📊 Attempt {attempt}/{max_attempts}")
            print("-"*60)
            
            # Run tests
            print("🧪 Running tests...")
            success, output = self.test_runner.run_tests(test_path)
            
            if success:
                print("✅ All tests passed!")
                return True
            
            # Parse failures
            print("🔍 Analyzing failures...")
            failures = self.test_runner.parse_failures(output)
            
            if not failures:
                print("⚠️  Tests failed but couldn't parse failures")
                print("Test output:")
                print(output)
                return False
            
            print(f"Found {len(failures)} failing test(s)")
            
            # Analyze and fix each failure
            for i, failure in enumerate(failures, 1):
                print(f"\n🔧 Processing failure {i}/{len(failures)}: {failure.test_name}")
                
                # Analyze
                analysis = self.analyzer.analyze_failure(failure)
                
                # Generate fix
                suggestion = self.fix_generator.generate_fix(failure, analysis)
                
                # Apply fix
                self.patcher.apply_fix(suggestion, dry_run=dry_run)
            
            if dry_run:
                print("\n" + "="*60)
                print("DRY RUN MODE - No changes were applied")
                print("Run with --apply to apply fixes")
                print("="*60)
                return False
        
        print(f"\n⚠️  Could not fix all tests after {max_attempts} attempts")
        return False


def main():
    """CLI entry point for FixBot."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="FixBot - AI Test Auto-Fix Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fixbot.py                    # Dry run on all tests
  fixbot.py --apply            # Apply fixes to all tests
  fixbot.py tests/test_foo.py  # Fix specific test file
  fixbot.py --test-cmd pytest  # Use pytest (default)
        """
    )
    
    parser.add_argument(
        'test_path',
        nargs='?',
        default='.',
        help='Path to test directory or file (default: current directory)'
    )
    
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Apply fixes (default: dry run mode)'
    )
    
    parser.add_argument(
        '--test-cmd',
        default='pytest',
        help='Test command to use (default: pytest)'
    )
    
    parser.add_argument(
        '--max-attempts',
        type=int,
        default=3,
        help='Maximum number of fix attempts (default: 3)'
    )
    
    args = parser.parse_args()
    
    # Create and run FixBot
    bot = FixBot(test_command=args.test_cmd)
    success = bot.auto_fix(
        test_path=args.test_path,
        dry_run=not args.apply,
        max_attempts=args.max_attempts
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
