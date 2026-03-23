import json
from itertools import islice

print("Plant database search. Type 'exit' to quit.")

try:
    while True:
        # Convert to lower for search.
        plant_search = input("\nEnter the name of the plant to search:").strip().lower()

        # Check exit.
        if plant_search == 'exit':
            print("Exiting...")
            break

        # Skip empty.
        if not plant_search:
            continue

        # Set the search state variable.
        matches = []

        # Open the db in read mode.
        with open('merged_plants_optimized.jsonl', 'r') as db:
            # Load the data into memory.
            for entity in db:
                data = json.loads(entity)
                common_name = data.get("common_name_primary")

                if common_name and plant_search in common_name.lower():
                    # Grab the scientific name
                    scientific_name = data.get("scientific_name_primary", "Missing")
                    # Convert back to a string with an indent for legibility.
                    # print(json.dumps(data, indent=2))
                    # Update the search state variable
                    matches.append({
                        "common_name": common_name,
                        "scientific_name": scientific_name
                    })
        # Print the total number of matches
        print(f"\nFound {len(matches)} matche(s) for '{plant_search}':")
        
        for match in matches:
            print(f"- {match['common_name']} ({match['scientific_name']})")
        
        if not matches:
            print(f"No results found for '{plant_search}'.")
                
except KeyboardInterrupt:
    print("\nSearch cancelled. Exiting...")