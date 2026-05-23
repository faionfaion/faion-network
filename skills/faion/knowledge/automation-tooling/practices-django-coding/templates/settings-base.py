# purpose: Base settings imported by dev/prod variants
# consumes: input artefacts described in AGENTS.md ## Prerequisites
# produces: artefact conforming to content/02-output-contract.xml for practices-django-coding
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1200 tokens when loaded as context

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
INSTALLED_APPS = ['django.contrib.admin']
