# Makefile

# Command to run only the enriched-profile API test
test-profile:
	PYTHONPATH=src python -m unittest test.test_linkedin_scrapers.TestLinkedInScrapers.test_cleaned_get_profile_data

# Command to run all tests
test-all:
	PYTHONPATH=src python -m unittest discover test



