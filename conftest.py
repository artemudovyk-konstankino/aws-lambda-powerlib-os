from glob import glob

# Get all paths to fixtures files
fixtures_paths = glob('src/tests/**/fixtures/[!__]*.py', recursive=True)

pytest_plugins = [
    # Autodiscover all fixtures files and load them as PyTest plugins
    fixture_file.replace('/', '.').replace('.py', '')
    for fixture_file in fixtures_paths
]
