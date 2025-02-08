# Makefile

# Command to run only the enriched-profile API test
test-enriched-profile:
	PYTHONPATH=src python -m unittest test.test_linkedin_scrapers.TestLinkedInScrapers.test_get_enriched_linkedin_profile

# Command to run all tests
test-all:
	PYTHONPATH=src python -m unittest discover test