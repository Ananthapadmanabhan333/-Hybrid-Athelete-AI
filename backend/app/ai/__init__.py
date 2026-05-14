# app/ai/__init__.py
# Makes this a proper Python package.
# The mistral_service singleton is imported lazily to avoid
# loading the model until initialize() is explicitly called.
