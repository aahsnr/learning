#!/usr/bin/env python3
# Read input file and process lines
items = []
with open("doom-packages.txt", "r") as f:
    for line in f.readlines():
        stripped_line = line.strip()
        if stripped_line:
            items.append(stripped_line)

# Remove duplicates while preserving order
unique_items = []
seen = set()
for item in items:
    if item not in seen:
        unique_items.append(item)
        seen.add(item)

# Sort alphabetically (case-insensitive)
unique_items.sort(key=lambda x: x.lower())

# Add checkbox formatting
checklist = []
for item in unique_items:
    checklist.append(f"- [ ] {item}")

# Write to output file
with open("doom-packages-checklist.txt", "w") as f:
    for entry in checklist:
        f.write(entry + "\n")
