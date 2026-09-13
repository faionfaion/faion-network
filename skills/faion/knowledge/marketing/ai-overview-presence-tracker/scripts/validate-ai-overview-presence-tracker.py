#!/usr/bin/env python3
"""validate-ai-overview-presence-tracker.py

Validate the artefact produced by the ai-overview-presence-tracker methodology against the JSON Schema
(draft-07) embedded in content/02-output-contract.xml, plus the cross-field rules from
content/01-core-rules.xml the schema cannot express. Stdlib-only, self-contained.

Inputs:
    --file PATH    artefact JSON to validate
    --self-test    run the contract's own valid + invalid examples
    --help         this message

Exit codes:
    0  artefact valid
    1  artefact invalid (violation list printed to stderr)
    2  usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#',
 '$id': 'https://faion.net/schemas/ai-overview-presence-tracker.json',
 'title': 'AI Overview presence report',
 'type': 'object',
 'required': ['query_set_version',
              'tracked_domain',
              'included_subdomains',
              'window_start',
              'window_end',
              'weeks_observed',
              'scrape_config',
              'queries',
              'rows',
              'metrics',
              'findings',
              'retrofit_list'],
 'additionalProperties': False,
 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'url': {'type': 'string', 'pattern': '^https://[^\\s/]+/'},
                 'host': {'type': 'string', 'pattern': '^[a-z0-9.-]+\\.[a-z]{2,}$'},
                 'rate': {'type': 'number', 'minimum': 0, 'maximum': 1}},
 'properties': {'__faion_header__': {'type': ['object', 'string']},
                'query_set_version': {'type': 'string', 'pattern': '^v[0-9]+$'},
                'tracked_domain': {'$ref': '#/definitions/host'},
                'included_subdomains': {'type': 'array', 'items': {'$ref': '#/definitions/host'}},
                'window_start': {'$ref': '#/definitions/date'},
                'window_end': {'$ref': '#/definitions/date'},
                'weeks_observed': {'type': 'integer', 'minimum': 1, 'maximum': 8},
                'scrape_config': {'type': 'object',
                                  'required': ['adapter',
                                               'country',
                                               'language',
                                               'device',
                                               'logged_out',
                                               'aio_available_checked'],
                                  'additionalProperties': False,
                                  'properties': {'adapter': {'type': 'string', 'minLength': 3},
                                                 'country': {'type': 'string',
                                                             'pattern': '^[A-Z]{2}$'},
                                                 'language': {'type': 'string',
                                                              'pattern': '^[a-z]{2}$'},
                                                 'device': {'type': 'string',
                                                            'enum': ['mobile', 'desktop']},
                                                 'logged_out': {'const': True},
                                                 'aio_available_checked': {'const': True}}},
                'queries': {'type': 'array',
                            'minItems': 20,
                            'items': {'type': 'object',
                                      'required': ['query', 'target_url'],
                                      'additionalProperties': False,
                                      'properties': {'query': {'type': 'string', 'minLength': 3},
                                                     'target_url': {'$ref': '#/definitions/url'}}}},
                'rows': {'type': 'array',
                         'minItems': 1,
                         'items': {'type': 'object',
                                   'required': ['query',
                                                'week',
                                                'observed_at',
                                                'status',
                                                'aio_present',
                                                'citations',
                                                'our_domain_cited',
                                                'selected_snippet',
                                                'panel_position'],
                                   'additionalProperties': False,
                                   'properties': {'query': {'type': 'string', 'minLength': 3},
                                                  'week': {'type': 'integer',
                                                           'minimum': 1,
                                                           'maximum': 8},
                                                  'observed_at': {'anyOf': [{'$ref': '#/definitions/date'},
                                                                            {'type': 'null'}]},
                                                  'status': {'type': 'string',
                                                             'enum': ['observed', 'missing']},
                                                  'aio_present': {'type': ['boolean', 'null']},
                                                  'citations': {'type': 'array',
                                                                'items': {'$ref': '#/definitions/url'}},
                                                  'our_domain_cited': {'type': ['boolean', 'null']},
                                                  'selected_snippet': {'type': ['string', 'null']},
                                                  'panel_position': {'type': ['integer', 'null'],
                                                                     'minimum': 1}},
                                   'allOf': [{'if': {'properties': {'status': {'const': 'missing'}}},
                                              'then': {'properties': {'observed_at': {'type': 'null'},
                                                                      'aio_present': {'type': 'null'},
                                                                      'citations': {'maxItems': 0},
                                                                      'our_domain_cited': {'type': 'null'},
                                                                      'selected_snippet': {'type': 'null'},
                                                                      'panel_position': {'type': 'null'}}},
                                              'else': {'properties': {'observed_at': {'type': 'string'},
                                                                      'aio_present': {'type': 'boolean'},
                                                                      'our_domain_cited': {'type': 'boolean'}}}},
                                             {'if': {'properties': {'status': {'const': 'observed'},
                                                                    'aio_present': {'const': True}}},
                                              'then': {'properties': {'citations': {'minItems': 1},
                                                                      'panel_position': {'type': 'integer'},
                                                                      'selected_snippet': {'type': 'string'}}}},
                                             {'if': {'properties': {'status': {'const': 'observed'},
                                                                    'aio_present': {'const': False}}},
                                              'then': {'properties': {'citations': {'maxItems': 0},
                                                                      'our_domain_cited': {'const': False},
                                                                      'panel_position': {'type': 'null'},
                                                                      'selected_snippet': {'type': 'null'}}}}]}},
                'metrics': {'type': 'array',
                            'minItems': 3,
                            'allOf': [{'contains': {'properties': {'name': {'const': 'aio_presence_rate'},
                                                                   'scope': {'const': 'window'}}}},
                                      {'contains': {'properties': {'name': {'const': 'our_citation_rate'},
                                                                   'scope': {'const': 'window'}}}},
                                      {'contains': {'properties': {'name': {'const': 'median_panel_position'},
                                                                   'scope': {'const': 'window'}}}}],
                            'items': {'type': 'object',
                                      'required': ['name',
                                                   'scope',
                                                   'week',
                                                   'value',
                                                   'unit',
                                                   'numerator',
                                                   'denominator'],
                                      'additionalProperties': False,
                                      'properties': {'name': {'type': 'string',
                                                              'enum': ['aio_presence_rate',
                                                                       'our_citation_rate',
                                                                       'median_panel_position']},
                                                     'scope': {'type': 'string',
                                                               'enum': ['week', 'window']},
                                                     'week': {'type': ['integer', 'null'],
                                                              'minimum': 1,
                                                              'maximum': 8},
                                                     'value': {'type': 'number', 'minimum': 0},
                                                     'unit': {'type': 'string',
                                                              'enum': ['ratio', 'count']},
                                                     'numerator': {'type': ['number', 'null'],
                                                                   'minimum': 0},
                                                     'denominator': {'type': 'integer',
                                                                     'minimum': 0}},
                                      'allOf': [{'if': {'properties': {'name': {'const': 'median_panel_position'}}},
                                                 'then': {'properties': {'unit': {'const': 'count'}}},
                                                 'else': {'properties': {'unit': {'const': 'ratio'},
                                                                         'value': {'$ref': '#/definitions/rate'}}}},
                                                {'if': {'properties': {'scope': {'const': 'window'}}},
                                                 'then': {'properties': {'week': {'type': 'null'}}},
                                                 'else': {'properties': {'week': {'type': 'integer'}}}}]}},
                'findings': {'type': 'array',
                             'minItems': 1,
                             'items': {'type': 'object',
                                       'required': ['metric',
                                                    'text',
                                                    'co_occurrence_only',
                                                    'causal'],
                                       'additionalProperties': False,
                                       'properties': {'metric': {'type': 'string',
                                                                 'enum': ['aio_presence_rate',
                                                                          'our_citation_rate',
                                                                          'median_panel_position']},
                                                      'text': {'type': 'string',
                                                               'minLength': 20,
                                                               'not': {'pattern': '(?i)(cost '
                                                                                  'us|because '
                                                                                  'of|due to|led '
                                                                                  'to|caused|thanks '
                                                                                  'to|resulted '
                                                                                  'in)'}},
                                                      'co_occurrence_only': {'const': True},
                                                      'causal': {'const': False}}}},
                'retrofit_list': {'type': 'array',
                                  'items': {'type': 'object',
                                            'required': ['query',
                                                         'target_url',
                                                         'weeks_present',
                                                         'uncited_last_4_weeks',
                                                         'impressions',
                                                         'cited_domains'],
                                            'additionalProperties': False,
                                            'properties': {'query': {'type': 'string',
                                                                     'minLength': 3},
                                                           'target_url': {'$ref': '#/definitions/url'},
                                                           'weeks_present': {'type': 'integer',
                                                                             'minimum': 5,
                                                                             'maximum': 8},
                                                           'uncited_last_4_weeks': {'const': True},
                                                           'impressions': {'type': 'integer',
                                                                           'minimum': 0},
                                                           'cited_domains': {'type': 'array',
                                                                             'minItems': 1,
                                                                             'items': {'$ref': '#/definitions/host'}}}}}}}

OK = {'query_set_version': 'v1',
 'tracked_domain': 'example-crm.com',
 'included_subdomains': [],
 'window_start': '2026-03-02',
 'window_end': '2026-04-26',
 'weeks_observed': 8,
 'scrape_config': {'adapter': 'SE Ranking AIO tracker',
                   'country': 'US',
                   'language': 'en',
                   'device': 'mobile',
                   'logged_out': True,
                   'aio_available_checked': True},
 'queries': [{'query': 'best crm for small business',
              'target_url': 'https://example-crm.com/guides/best-crm-for-small-business'},
             {'query': 'crm for real estate agents',
              'target_url': 'https://example-crm.com/guides/crm-for-real-estate-agents'},
             {'query': 'how to migrate from spreadsheets to crm',
              'target_url': 'https://example-crm.com/guides/how-to-migrate-from-spreadsheets-to-crm'},
             {'query': 'crm with email sequences',
              'target_url': 'https://example-crm.com/guides/crm-with-email-sequences'},
             {'query': 'pipeline management software',
              'target_url': 'https://example-crm.com/guides/pipeline-management-software'},
             {'query': 'free crm vs paid crm',
              'target_url': 'https://example-crm.com/guides/free-crm-vs-paid-crm'},
             {'query': 'crm for consultants',
              'target_url': 'https://example-crm.com/guides/crm-for-consultants'},
             {'query': 'crm integration with gmail',
              'target_url': 'https://example-crm.com/guides/crm-integration-with-gmail'},
             {'query': 'lead scoring software',
              'target_url': 'https://example-crm.com/guides/lead-scoring-software'},
             {'query': 'sales pipeline stages explained',
              'target_url': 'https://example-crm.com/guides/sales-pipeline-stages-explained'},
             {'query': 'crm for nonprofits',
              'target_url': 'https://example-crm.com/guides/crm-for-nonprofits'},
             {'query': 'how to track sales follow ups',
              'target_url': 'https://example-crm.com/guides/how-to-track-sales-follow-ups'},
             {'query': 'crm for freelancers',
              'target_url': 'https://example-crm.com/guides/crm-for-freelancers'},
             {'query': 'contact management software',
              'target_url': 'https://example-crm.com/guides/contact-management-software'},
             {'query': 'deal tracking spreadsheet alternative',
              'target_url': 'https://example-crm.com/guides/deal-tracking-spreadsheet-alternative'},
             {'query': 'crm onboarding checklist',
              'target_url': 'https://example-crm.com/guides/crm-onboarding-checklist'},
             {'query': 'crm data cleanup',
              'target_url': 'https://example-crm.com/guides/crm-data-cleanup'},
             {'query': 'sales forecasting for small teams',
              'target_url': 'https://example-crm.com/guides/sales-forecasting-for-small-teams'},
             {'query': 'crm for agencies',
              'target_url': 'https://example-crm.com/guides/crm-for-agencies'},
             {'query': 'crm reporting dashboard',
              'target_url': 'https://example-crm.com/guides/crm-reporting-dashboard'}],
 'rows': [{'query': 'best crm for small business',
           'week': 1,
           'observed_at': '2026-03-02',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://hubspot.com/crm-comparison', 'https://g2.com/categories/crm'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1},
          {'query': 'best crm for small business',
           'week': 2,
           'observed_at': '2026-03-09',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://hubspot.com/crm-comparison', 'https://g2.com/categories/crm'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1},
          {'query': 'best crm for small business',
           'week': 3,
           'observed_at': '2026-03-16',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://hubspot.com/crm-comparison', 'https://g2.com/categories/crm'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1},
          {'query': 'best crm for small business',
           'week': 4,
           'observed_at': '2026-03-23',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://hubspot.com/crm-comparison', 'https://g2.com/categories/crm'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1},
          {'query': 'best crm for small business',
           'week': 5,
           'observed_at': '2026-03-31',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://hubspot.com/crm-comparison', 'https://g2.com/categories/crm'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1},
          {'query': 'best crm for small business',
           'week': 6,
           'observed_at': '2026-04-06',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://hubspot.com/crm-comparison', 'https://g2.com/categories/crm'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1},
          {'query': 'best crm for small business',
           'week': 7,
           'observed_at': '2026-04-13',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://hubspot.com/crm-comparison', 'https://g2.com/categories/crm'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1},
          {'query': 'best crm for small business',
           'week': 8,
           'observed_at': '2026-04-20',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://hubspot.com/crm-comparison', 'https://g2.com/categories/crm'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1},
          {'query': 'crm for real estate agents',
           'week': 1,
           'observed_at': '2026-03-02',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://example-crm.com/guides/crm-for-real-estate-agents',
                         'https://zoho.com/crm/guide'],
           'our_domain_cited': True,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 2},
          {'query': 'crm for real estate agents',
           'week': 2,
           'observed_at': '2026-03-09',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://example-crm.com/guides/crm-for-real-estate-agents',
                         'https://zoho.com/crm/guide'],
           'our_domain_cited': True,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 2},
          {'query': 'crm for real estate agents',
           'week': 3,
           'observed_at': '2026-03-16',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://example-crm.com/guides/crm-for-real-estate-agents',
                         'https://zoho.com/crm/guide'],
           'our_domain_cited': True,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 2},
          {'query': 'crm for real estate agents',
           'week': 4,
           'observed_at': '2026-03-23',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://example-crm.com/guides/crm-for-real-estate-agents',
                         'https://zoho.com/crm/guide'],
           'our_domain_cited': True,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 2},
          {'query': 'crm for real estate agents',
           'week': 5,
           'observed_at': '2026-03-31',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://example-crm.com/guides/crm-for-real-estate-agents',
                         'https://zoho.com/crm/guide'],
           'our_domain_cited': True,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 2},
          {'query': 'crm for real estate agents',
           'week': 6,
           'observed_at': '2026-04-06',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://example-crm.com/guides/crm-for-real-estate-agents',
                         'https://zoho.com/crm/guide'],
           'our_domain_cited': True,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 2},
          {'query': 'crm for real estate agents',
           'week': 7,
           'observed_at': '2026-04-13',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://example-crm.com/guides/crm-for-real-estate-agents',
                         'https://zoho.com/crm/guide'],
           'our_domain_cited': True,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 2},
          {'query': 'crm for real estate agents',
           'week': 8,
           'observed_at': '2026-04-20',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://example-crm.com/guides/crm-for-real-estate-agents',
                         'https://zoho.com/crm/guide'],
           'our_domain_cited': True,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 2},
          {'query': 'how to migrate from spreadsheets to crm',
           'week': 1,
           'observed_at': '2026-03-02',
           'status': 'observed',
           'aio_present': False,
           'citations': [],
           'our_domain_cited': False,
           'selected_snippet': None,
           'panel_position': None},
          {'query': 'how to migrate from spreadsheets to crm',
           'week': 2,
           'observed_at': '2026-03-09',
           'status': 'observed',
           'aio_present': False,
           'citations': [],
           'our_domain_cited': False,
           'selected_snippet': None,
           'panel_position': None},
          {'query': 'how to migrate from spreadsheets to crm',
           'week': 3,
           'observed_at': '2026-03-16',
           'status': 'observed',
           'aio_present': False,
           'citations': [],
           'our_domain_cited': False,
           'selected_snippet': None,
           'panel_position': None},
          {'query': 'how to migrate from spreadsheets to crm',
           'week': 4,
           'observed_at': '2026-03-23',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://hubspot.com/crm-comparison'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1},
          {'query': 'how to migrate from spreadsheets to crm',
           'week': 5,
           'observed_at': '2026-03-31',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://hubspot.com/crm-comparison'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1},
          {'query': 'how to migrate from spreadsheets to crm',
           'week': 6,
           'observed_at': '2026-04-06',
           'status': 'observed',
           'aio_present': False,
           'citations': [],
           'our_domain_cited': False,
           'selected_snippet': None,
           'panel_position': None},
          {'query': 'how to migrate from spreadsheets to crm',
           'week': 7,
           'observed_at': '2026-04-13',
           'status': 'observed',
           'aio_present': False,
           'citations': [],
           'our_domain_cited': False,
           'selected_snippet': None,
           'panel_position': None},
          {'query': 'how to migrate from spreadsheets to crm',
           'week': 8,
           'observed_at': '2026-04-20',
           'status': 'observed',
           'aio_present': False,
           'citations': [],
           'our_domain_cited': False,
           'selected_snippet': None,
           'panel_position': None},
          {'query': 'crm with email sequences',
           'week': 1,
           'observed_at': '2026-03-02',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://pipedrive.com/blog/crm', 'https://g2.com/categories/crm'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1},
          {'query': 'crm with email sequences',
           'week': 2,
           'observed_at': '2026-03-09',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://pipedrive.com/blog/crm', 'https://g2.com/categories/crm'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1},
          {'query': 'crm with email sequences',
           'week': 3,
           'observed_at': '2026-03-16',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://pipedrive.com/blog/crm', 'https://g2.com/categories/crm'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1},
          {'query': 'crm with email sequences',
           'week': 4,
           'observed_at': None,
           'status': 'missing',
           'aio_present': None,
           'citations': [],
           'our_domain_cited': None,
           'selected_snippet': None,
           'panel_position': None},
          {'query': 'crm with email sequences',
           'week': 5,
           'observed_at': '2026-03-31',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://pipedrive.com/blog/crm', 'https://g2.com/categories/crm'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1},
          {'query': 'crm with email sequences',
           'week': 6,
           'observed_at': '2026-04-06',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://pipedrive.com/blog/crm', 'https://g2.com/categories/crm'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1},
          {'query': 'crm with email sequences',
           'week': 7,
           'observed_at': '2026-04-13',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://pipedrive.com/blog/crm', 'https://g2.com/categories/crm'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1},
          {'query': 'crm with email sequences',
           'week': 8,
           'observed_at': '2026-04-20',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://pipedrive.com/blog/crm', 'https://g2.com/categories/crm'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM with pipeline stages and email sync...',
           'panel_position': 1}],
 'metrics': [{'name': 'aio_presence_rate',
              'scope': 'week',
              'week': 1,
              'value': 0.75,
              'unit': 'ratio',
              'numerator': 3,
              'denominator': 4},
             {'name': 'our_citation_rate',
              'scope': 'week',
              'week': 1,
              'value': 0.333,
              'unit': 'ratio',
              'numerator': 1,
              'denominator': 3},
             {'name': 'median_panel_position',
              'scope': 'week',
              'week': 1,
              'value': 1,
              'unit': 'count',
              'numerator': 1,
              'denominator': 3},
             {'name': 'aio_presence_rate',
              'scope': 'week',
              'week': 2,
              'value': 0.75,
              'unit': 'ratio',
              'numerator': 3,
              'denominator': 4},
             {'name': 'our_citation_rate',
              'scope': 'week',
              'week': 2,
              'value': 0.333,
              'unit': 'ratio',
              'numerator': 1,
              'denominator': 3},
             {'name': 'median_panel_position',
              'scope': 'week',
              'week': 2,
              'value': 1,
              'unit': 'count',
              'numerator': 1,
              'denominator': 3},
             {'name': 'aio_presence_rate',
              'scope': 'week',
              'week': 3,
              'value': 0.75,
              'unit': 'ratio',
              'numerator': 3,
              'denominator': 4},
             {'name': 'our_citation_rate',
              'scope': 'week',
              'week': 3,
              'value': 0.333,
              'unit': 'ratio',
              'numerator': 1,
              'denominator': 3},
             {'name': 'median_panel_position',
              'scope': 'week',
              'week': 3,
              'value': 1,
              'unit': 'count',
              'numerator': 1,
              'denominator': 3},
             {'name': 'aio_presence_rate',
              'scope': 'week',
              'week': 4,
              'value': 1.0,
              'unit': 'ratio',
              'numerator': 3,
              'denominator': 3},
             {'name': 'our_citation_rate',
              'scope': 'week',
              'week': 4,
              'value': 0.333,
              'unit': 'ratio',
              'numerator': 1,
              'denominator': 3},
             {'name': 'median_panel_position',
              'scope': 'week',
              'week': 4,
              'value': 1,
              'unit': 'count',
              'numerator': 1,
              'denominator': 3},
             {'name': 'aio_presence_rate',
              'scope': 'week',
              'week': 5,
              'value': 1.0,
              'unit': 'ratio',
              'numerator': 4,
              'denominator': 4},
             {'name': 'our_citation_rate',
              'scope': 'week',
              'week': 5,
              'value': 0.25,
              'unit': 'ratio',
              'numerator': 1,
              'denominator': 4},
             {'name': 'median_panel_position',
              'scope': 'week',
              'week': 5,
              'value': 1.0,
              'unit': 'count',
              'numerator': 1.0,
              'denominator': 4},
             {'name': 'aio_presence_rate',
              'scope': 'week',
              'week': 6,
              'value': 0.75,
              'unit': 'ratio',
              'numerator': 3,
              'denominator': 4},
             {'name': 'our_citation_rate',
              'scope': 'week',
              'week': 6,
              'value': 0.333,
              'unit': 'ratio',
              'numerator': 1,
              'denominator': 3},
             {'name': 'median_panel_position',
              'scope': 'week',
              'week': 6,
              'value': 1,
              'unit': 'count',
              'numerator': 1,
              'denominator': 3},
             {'name': 'aio_presence_rate',
              'scope': 'week',
              'week': 7,
              'value': 0.75,
              'unit': 'ratio',
              'numerator': 3,
              'denominator': 4},
             {'name': 'our_citation_rate',
              'scope': 'week',
              'week': 7,
              'value': 0.333,
              'unit': 'ratio',
              'numerator': 1,
              'denominator': 3},
             {'name': 'median_panel_position',
              'scope': 'week',
              'week': 7,
              'value': 1,
              'unit': 'count',
              'numerator': 1,
              'denominator': 3},
             {'name': 'aio_presence_rate',
              'scope': 'week',
              'week': 8,
              'value': 0.75,
              'unit': 'ratio',
              'numerator': 3,
              'denominator': 4},
             {'name': 'our_citation_rate',
              'scope': 'week',
              'week': 8,
              'value': 0.333,
              'unit': 'ratio',
              'numerator': 1,
              'denominator': 3},
             {'name': 'median_panel_position',
              'scope': 'week',
              'week': 8,
              'value': 1,
              'unit': 'count',
              'numerator': 1,
              'denominator': 3},
             {'name': 'aio_presence_rate',
              'scope': 'window',
              'week': None,
              'value': 0.806,
              'unit': 'ratio',
              'numerator': 25,
              'denominator': 31},
             {'name': 'our_citation_rate',
              'scope': 'window',
              'week': None,
              'value': 0.32,
              'unit': 'ratio',
              'numerator': 8,
              'denominator': 25},
             {'name': 'median_panel_position',
              'scope': 'window',
              'week': None,
              'value': 1,
              'unit': 'count',
              'numerator': 1,
              'denominator': 25}],
 'findings': [{'metric': 'our_citation_rate',
               'text': "our_citation_rate for the window 2026-03-02 to 2026-04-26 is 0.32: 'crm "
                       "for real estate agents' is cited every week; 'best crm for small business' "
                       'shows a panel in all 8 weeks and never cites us.',
               'co_occurrence_only': True,
               'causal': False},
              {'metric': 'aio_presence_rate',
               'text': "aio_presence_rate for 'how to migrate from spreadsheets to crm' is 0.25 "
                       'over 2026-03-02 to 2026-04-26; its Search Console impressions fell in the '
                       'same window, which co-occurs with the panel and is not attributed to it.',
               'co_occurrence_only': True,
               'causal': False}],
 'retrofit_list': [{'query': 'best crm for small business',
                    'target_url': 'https://example-crm.com/guides/best-crm-for-small-business',
                    'weeks_present': 8,
                    'uncited_last_4_weeks': True,
                    'impressions': 48200,
                    'cited_domains': ['hubspot.com', 'g2.com']},
                   {'query': 'crm with email sequences',
                    'target_url': 'https://example-crm.com/guides/crm-with-email-sequences',
                    'weeks_present': 7,
                    'uncited_last_4_weeks': True,
                    'impressions': 9100,
                    'cited_domains': ['pipedrive.com', 'g2.com']}]}

BAD = {'query_set_version': 'v1',
 'tracked_domain': 'example-crm.com',
 'included_subdomains': [],
 'window_start': '2026-03-02',
 'window_end': '2026-03-22',
 'weeks_observed': 3,
 'scrape_config': {'adapter': 'SE Ranking AIO tracker',
                   'country': 'US',
                   'language': 'en',
                   'device': 'tablet',
                   'logged_out': False,
                   'aio_available_checked': True},
 'queries': [{'query': 'best crm for small business',
              'target_url': 'https://example-crm.com/guides/best-crm-for-small-business'},
             {'query': 'crm for real estate agents',
              'target_url': 'https://example-crm.com/guides/crm-for-real-estate-agents'},
             {'query': 'how to migrate from spreadsheets to crm',
              'target_url': 'https://example-crm.com/guides/how-to-migrate-from-spreadsheets-to-crm'},
             {'query': 'crm with email sequences',
              'target_url': 'https://example-crm.com/guides/crm-with-email-sequences'},
             {'query': 'pipeline management software',
              'target_url': 'https://example-crm.com/guides/pipeline-management-software'},
             {'query': 'free crm vs paid crm',
              'target_url': 'https://example-crm.com/guides/free-crm-vs-paid-crm'},
             {'query': 'crm for consultants',
              'target_url': 'https://example-crm.com/guides/crm-for-consultants'},
             {'query': 'crm integration with gmail',
              'target_url': 'https://example-crm.com/guides/crm-integration-with-gmail'},
             {'query': 'lead scoring software',
              'target_url': 'https://example-crm.com/guides/lead-scoring-software'},
             {'query': 'sales pipeline stages explained',
              'target_url': 'https://example-crm.com/guides/sales-pipeline-stages-explained'},
             {'query': 'crm for nonprofits',
              'target_url': 'https://example-crm.com/guides/crm-for-nonprofits'},
             {'query': 'how to track sales follow ups',
              'target_url': 'https://example-crm.com/guides/how-to-track-sales-follow-ups'}],
 'rows': [{'query': 'best crm for small business',
           'week': 1,
           'observed_at': '2026-03-02',
           'status': 'observed',
           'aio_present': True,
           'citations': [],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM...',
           'panel_position': 1},
          {'query': 'best crm for small business',
           'week': 2,
           'observed_at': '2026-03-09',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://hubspot.com/crm-comparison'],
           'our_domain_cited': True,
           'selected_snippet': 'Example CRM is a popular choice...',
           'panel_position': 1},
          {'query': 'best crm for small business',
           'week': 3,
           'observed_at': '2026-03-20',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://hubspot.com/crm-comparison'],
           'our_domain_cited': False,
           'selected_snippet': 'Pick a CRM...',
           'panel_position': 1},
          {'query': 'how to migrate from spreadsheets to crm',
           'week': 1,
           'observed_at': '2026-03-02',
           'status': 'observed',
           'aio_present': False,
           'citations': [],
           'our_domain_cited': False,
           'selected_snippet': None,
           'panel_position': None},
          {'query': 'how to migrate from spreadsheets to crm',
           'week': 2,
           'observed_at': '2026-03-09',
           'status': 'observed',
           'aio_present': True,
           'citations': ['https://hubspot.com/crm-comparison'],
           'our_domain_cited': False,
           'selected_snippet': 'Migrating...',
           'panel_position': 2},
          {'query': 'how to migrate from spreadsheets to crm',
           'week': 3,
           'observed_at': '2026-03-16',
           'status': 'observed',
           'aio_present': False,
           'citations': [],
           'our_domain_cited': False,
           'selected_snippet': None,
           'panel_position': None}],
 'metrics': [{'name': 'aio_presence_rate',
              'scope': 'window',
              'week': None,
              'value': 0.667,
              'unit': 'ratio',
              'numerator': 4,
              'denominator': 6},
             {'name': 'our_citation_rate',
              'scope': 'window',
              'week': None,
              'value': 0.167,
              'unit': 'ratio',
              'numerator': 1,
              'denominator': 6},
             {'name': 'median_panel_position',
              'scope': 'window',
              'week': None,
              'value': 1,
              'unit': 'count',
              'numerator': 1,
              'denominator': 4}],
 'findings': [{'metric': 'our_citation_rate',
               'text': "Losing the citation on 'best crm for small business' cost us 12 percent of "
                       'clicks in week 3.',
               'co_occurrence_only': False,
               'causal': True}],
 'retrofit_list': [{'query': 'how to migrate from spreadsheets to crm',
                    'target_url': 'https://example-crm.com/guides/how-to-migrate-from-spreadsheets-to-crm',
                    'weeks_present': 1,
                    'uncited_last_4_weeks': True,
                    'impressions': 3100,
                    'cited_domains': ['hubspot.com']}]}


# --------------------------------------------------------------------------
# draft-07 subset: required, type, enum, const, pattern, minimum/maximum,
# exclusiveMinimum/Maximum, minLength/maxLength, minItems/maxItems,
# minProperties/maxProperties, uniqueItems, items, contains, properties,
# additionalProperties, allOf/anyOf/oneOf/not, if/then/else, local $ref
# (#/definitions/...). Enough for every constraint the contract declares.
# --------------------------------------------------------------------------

_TYPES = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
}


def _check(schema: dict, value, path: str, errs: list[str]) -> None:
    if schema is True or schema == {}:
        return
    if schema is False:
        errs.append(f"{path or '$'}: schema forbids any value")
        return
    if "$ref" in schema:
        node = SCHEMA
        for part in schema["$ref"].lstrip("#/").split("/"):
            node = node[part]
        merged = dict(node)
        merged.update({k: v for k, v in schema.items() if k != "$ref"})
        schema = merged
    t = schema.get("type")
    if t is not None:
        types = t if isinstance(t, list) else [t]
        if not any(_TYPES[x](value) for x in types):
            errs.append(f"{path or '$'}: expected type {'/'.join(types)}, got {type(value).__name__}")
            return
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{path or '$'}: {value!r} not in {schema['enum']!r}")
    if "const" in schema and value != schema["const"]:
        errs.append(f"{path or '$'}: must equal {schema['const']!r}, got {value!r}")
    if isinstance(value, str):
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errs.append(f"{path or '$'}: {value!r} does not match /{schema['pattern']}/")
        if "minLength" in schema and len(value) < schema["minLength"]:
            errs.append(f"{path or '$'}: shorter than minLength {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errs.append(f"{path or '$'}: longer than maxLength {schema['maxLength']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errs.append(f"{path or '$'}: {value} below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errs.append(f"{path or '$'}: {value} above maximum {schema['maximum']}")
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            errs.append(f"{path or '$'}: {value} not above exclusiveMinimum {schema['exclusiveMinimum']}")
        if "exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"]:
            errs.append(f"{path or '$'}: {value} not below exclusiveMaximum {schema['exclusiveMaximum']}")
        if "multipleOf" in schema and abs(round(value / schema["multipleOf"]) * schema["multipleOf"] - value) > 1e-9:
            errs.append(f"{path or '$'}: {value} is not a multiple of {schema['multipleOf']}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errs.append(f"{path or '$'}: fewer than minItems {schema['minItems']}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errs.append(f"{path or '$'}: more than maxItems {schema['maxItems']}")
        if schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            errs.append(f"{path or '$'}: items are not unique")
        if "items" in schema:
            if isinstance(schema["items"], list):
                for i, (sub, item) in enumerate(zip(schema["items"], value)):
                    _check(sub, item, f"{path}[{i}]", errs)
            else:
                for i, item in enumerate(value):
                    _check(schema["items"], item, f"{path}[{i}]", errs)
        if "contains" in schema:
            if not any(_ok(schema["contains"], item) for item in value):
                errs.append(f"{path or '$'}: no element satisfies `contains`")
    if isinstance(value, dict):
        for k in schema.get("required", []):
            if k not in value:
                errs.append(f"{path or '$'}: missing required field {k!r}")
        if "minProperties" in schema and len(value) < schema["minProperties"]:
            errs.append(f"{path or '$'}: fewer than minProperties {schema['minProperties']}")
        if "maxProperties" in schema and len(value) > schema["maxProperties"]:
            errs.append(f"{path or '$'}: more than maxProperties {schema['maxProperties']}")
        props = schema.get("properties", {})
        for k, sub in props.items():
            if k in value:
                _check(sub, value[k], f"{path}.{k}" if path else k, errs)
        ap = schema.get("additionalProperties", True)
        if ap is False:
            for k in value:
                if k not in props:
                    errs.append(f"{path or '$'}: additional property {k!r} not allowed")
        elif isinstance(ap, dict):
            for k in value:
                if k not in props:
                    _check(ap, value[k], f"{path}.{k}" if path else k, errs)
    for sub in schema.get("allOf", []):
        _check(sub, value, path, errs)
    if "anyOf" in schema and not any(_ok(s, value) for s in schema["anyOf"]):
        errs.append(f"{path or '$'}: matches none of anyOf")
    if "oneOf" in schema and sum(_ok(s, value) for s in schema["oneOf"]) != 1:
        errs.append(f"{path or '$'}: must match exactly one of oneOf")
    if "not" in schema and _ok(schema["not"], value):
        errs.append(f"{path or '$'}: matches forbidden `not` schema")
    if "if" in schema:
        branch = "then" if _ok(schema["if"], value) else "else"
        if branch in schema:
            _check(schema[branch], value, path, errs)


def _ok(schema, value) -> bool:
    tmp: list[str] = []
    _check(schema, value, "", tmp)
    return not tmp

import statistics
from datetime import date, timedelta
from urllib.parse import urlsplit


def _d(s):
    try:
        return date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def _host(u: str) -> str:
    h = urlsplit(u).hostname or ""
    return h[4:] if h.startswith("www.") else h


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    dom = obj.get("tracked_domain", "")
    ours = {dom, *obj.get("included_subdomains", [])}
    ws, we, n = _d(obj.get("window_start", "")), _d(obj.get("window_end", "")), obj.get("weeks_observed") or 0
    if ws and we and we != ws + timedelta(days=7 * n - 1):
        errs.append(f"window_end must be window_start + {7 * n - 1} days for {n} observed weeks (r-fixed-versioned-query-set)")
    qs = {q.get("query"): q for q in obj.get("queries") or [] if isinstance(q, dict)}
    for i, q in enumerate(obj.get("queries") or []):
        if _host(q.get("target_url", "")) not in ours:
            errs.append(f"queries[{i}]: target_url is not on {dom} (r-fixed-versioned-query-set)")
    rows = [r for r in obj.get("rows") or [] if isinstance(r, dict)]
    for i, r in enumerate(rows):
        if r.get("query") not in qs:
            errs.append(f"rows[{i}]: query {r.get('query')!r} is not in the query set (r-fixed-versioned-query-set)")
        if r.get("week", 0) > n:
            errs.append(f"rows[{i}]: week {r.get('week')} is beyond weeks_observed {n} (r-weekly-same-day-no-interpolation)")
        if r.get("status") == "observed":
            due = ws + timedelta(days=7 * (r.get("week", 1) - 1)) if ws else None
            at = _d(r.get("observed_at"))
            if due and at and abs((at - due).days) > 2:
                errs.append(f"rows[{i}]: observed_at {at} is more than 48 hours from the scheduled day {due} (r-weekly-same-day-no-interpolation)")
            cited = any(_host(c) in ours for c in r.get("citations") or [])
            if bool(r.get("our_domain_cited")) != cited:
                errs.append(f"rows[{i}]: our_domain_cited must be {cited} from the citation hosts, not from snippet text (r-our-domain-cited-exact-host-match)")
    def block(sub):
        obs = [r for r in sub if r.get("status") == "observed"]
        pres = [r for r in obs if r.get("aio_present")]
        return {"aio_presence_rate": (len(pres), len(obs)), "our_citation_rate": (sum(1 for r in pres if r.get("our_domain_cited")), len(pres)),
                "median_panel_position": (statistics.median([r["panel_position"] for r in pres]) if pres else None, len(pres))}
    want = {("window", None): block(rows)}
    for w in sorted({r.get("week") for r in rows}):
        want[("week", w)] = block([r for r in rows if r.get("week") == w])
    seen = set()
    for i, m in enumerate(obj.get("metrics") or []):
        key = (m.get("scope"), m.get("week"))
        seen.add((key, m.get("name")))
        if key not in want:
            errs.append(f"metrics[{i}]: no rows for {key} (r-report-metrics-presence-citation-position)")
            continue
        num, den = want[key].get(m.get("name"), (None, None))
        if m.get("name") == "median_panel_position":
            if num is not None and abs(m.get("value", -1) - num) > 1e-9 or m.get("denominator") != den:
                errs.append(f"metrics[{i}]: median_panel_position for {key} must be {num} over {den} present panels (r-report-metrics-presence-citation-position)")
        else:
            if m.get("numerator") != num or m.get("denominator") != den:
                errs.append(f"metrics[{i}]: {m.get('name')} for {key} must be {num} / {den} ({'present over observed' if m.get('name') == 'aio_presence_rate' else 'cited over present panels'}) (r-report-metrics-presence-citation-position)")
            elif den and abs(round(num / den, 3) - m.get("value", -1)) > 0.0005:
                errs.append(f"metrics[{i}]: value must be {round(num / den, 3)} (r-report-metrics-presence-citation-position)")
    for key in want:
        for name in ("aio_presence_rate", "our_citation_rate", "median_panel_position"):
            if (key, name) not in seen:
                errs.append(f"metrics: {name} missing for {key} (r-report-metrics-presence-citation-position)")
    rl = obj.get("retrofit_list") or []
    if n < 8 and rl:
        errs.append("retrofit_list must be empty until 8 weeks are observed (r-retrofit-priority-rule)")
    prev = None
    for i, e in enumerate(rl):
        qrows = [r for r in rows if r.get("query") == e.get("query")]
        if not qrows:
            errs.append(f"retrofit_list[{i}]: no rows for {e.get('query')!r} (r-retrofit-priority-rule)")
        else:
            present = sum(1 for r in qrows if r.get("aio_present"))
            if present != e.get("weeks_present") or present < 5:
                errs.append(f"retrofit_list[{i}]: weeks_present must be {present} from the rows and at least 5 (r-retrofit-priority-rule)")
            last4 = [r for r in qrows if r.get("week", 0) > n - 4 and r.get("status") == "observed"]
            if any(r.get("our_domain_cited") for r in last4):
                errs.append(f"retrofit_list[{i}]: {e.get('query')!r} was cited in one of the last 4 weeks (r-retrofit-priority-rule)")
            hosts = {_host(c) for r in qrows for c in r.get("citations") or []}
            for h in e.get("cited_domains") or []:
                if h not in hosts:
                    errs.append(f"retrofit_list[{i}]: cited domain {h!r} never appears in the rows' citations (r-retrofit-priority-rule)")
        if prev is not None and e.get("impressions", 0) > prev:
            errs.append(f"retrofit_list[{i}]: not ranked by impressions descending (r-retrofit-priority-rule)")
        prev = e.get("impressions", 0)
        q = qs.get(e.get("query"))
        if q and q.get("target_url") != e.get("target_url"):
            errs.append(f"retrofit_list[{i}]: target_url differs from the query set's (r-retrofit-priority-rule)")
    return errs


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    _check(SCHEMA, obj, "", errs)
    if not errs:
        errs.extend(extra(obj))
    return errs


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("self-test FAIL: OK fixture rejected: " + "; ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-ai-overview-presence-tracker.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
    ap.add_argument("--self-test", action="store_true", help="run the contract's own examples and exit")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
