from dagster import asset

@asset
def test():
    return 0


