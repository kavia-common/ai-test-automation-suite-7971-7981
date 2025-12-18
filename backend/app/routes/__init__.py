"""
Routes package initializer.

This module intentionally does not import blueprints to avoid circular imports.
Each route module (health, tests, executions, reports, ai) defines its own
Blueprint instance and is imported explicitly in app.__init__ to register
endpoints with the API.
"""
