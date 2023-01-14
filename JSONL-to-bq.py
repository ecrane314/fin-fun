# Read JSONL file and append write to BQ Table
# Upsert needed as duplicates? Unique on the date of the observation
# Need a new table per series? Yes. Run the joins as needed.