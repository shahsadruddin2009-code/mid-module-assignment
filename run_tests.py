#!/usr/bin/env python3
"""
Test runner script for the Online Bookstore Flask application.

This script provides different ways to run the test suite:
- All tests
- Individual test files
- Specific test classes or methods
- With coverage reporting (if coverage.py is installed)

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --models          # Run only model tests
    python run_tests.py --routes          # Run only route tests
    python run_tests.py --integration     # Run only integration tests
    python run_tests.py --coverage        # Run all tests with coverage
    python run_tests.py --verbose         # Run with verbose output
"""

import sys
import unittest
import os
from argparse import ArgumentParser


def run_tests(test_pattern="test_*.py", verbosity=1, with_coverage=False):
    """Run tests with optional coverage reporting."""
    
    if with_coverage:
        try:
            import coverage
            cov = coverage.Coverage()
            cov.start()
        except ImportError:
            print("Coverage.py not installed. Install with: pip install coverage")
            with_coverage = False
    
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern=test_pattern)
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    if with_coverage:
        cov.stop()
        cov.save()
        
        print("\n" + "="*50)
        print("COVERAGE REPORT")
        print("="*50)
        cov.report(show_missing=True)
        
        # Generate HTML report
        try:
            cov.html_report(directory='htmlcov')
            print(f"\nHTML coverage report generated in: htmlcov/index.html")
        except Exception as e:
            print(f"Could not generate HTML report: {e}")
    
    return result.wasSuccessful()


def main():
    parser = ArgumentParser(description="Run tests for the Online Bookstore Flask app")
    
    # Test selection options
    parser.add_argument('--models', action='store_true', 
                       help='Run only model tests')
    parser.add_argument('--routes', action='store_true', 
                       help='Run only route tests')
    parser.add_argument('--integration', action='store_true', 
                       help='Run only integration tests')
    
    # Output options
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    parser.add_argument('--coverage', '-c', action='store_true',
                       help='Run with coverage reporting')
    
    # Specific test options
    parser.add_argument('--file', '-f', type=str,
                       help='Run specific test file (e.g., test_app_model.py)')
    parser.add_argument('--class', '-cl', type=str, dest='test_class',
                       help='Run specific test class (e.g., TestBookModel)')
    parser.add_argument('--method', '-m', type=str,
                       help='Run specific test method')
    
    args = parser.parse_args()
    
    # Set verbosity
    verbosity = 2 if args.verbose else 1
    
    # Determine test pattern
    if args.models:
        test_pattern = "test_app_model.py"
        print("Running Model Tests...")
    elif args.routes:
        test_pattern = "test_app_routes.py"
        print("Running Route Tests...")
    elif args.integration:
        test_pattern = "test_integration.py"
        print("Running Integration Tests...")
    elif args.file:
        test_pattern = args.file
        print(f"Running tests from {args.file}...")
    else:
        test_pattern = "test_*.py"
        print("Running All Tests...")
    
    # Handle specific class or method
    if args.test_class or args.method:
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        if args.method and args.test_class:
            # Run specific method in specific class
            module_name = args.file.replace('.py', '') if args.file else 'test_app_model'
            module = __import__(module_name)
            test_class = getattr(module, args.test_class)
            suite.addTest(test_class(args.method))
        elif args.test_class:
            # Run all methods in specific class
            if args.file:
                module_name = args.file.replace('.py', '')
                module = __import__(module_name)
                test_class = getattr(module, args.test_class)
                suite.addTests(loader.loadTestsFromTestCase(test_class))
        
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)
        return result.wasSuccessful()
    
    # Run the tests
    success = run_tests(test_pattern, verbosity, args.coverage)
    
    if success:
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())