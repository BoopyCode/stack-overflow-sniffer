#!/usr/bin/env python3
# Stack Overflow Sniffer - Because your memory is as reliable as a JavaScript framework

import json
import os
import sys
from datetime import datetime
from pathlib import Path

DB_FILE = Path.home() / '.stack_sniffer.json'

def load_db():
    """Loads your forgotten wisdom from the digital abyss"""
    if DB_FILE.exists():
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return []

def save_db(db):
    """Saves your future self from present you's incompetence"""
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=2)

def add_solution(problem, solution, tags=None):
    """Records another solution you'll definitely remember this time"""
    db = load_db()
    entry = {
        'problem': problem,
        'solution': solution,
        'tags': tags or [],
        'date': datetime.now().isoformat(),
        'times_forgotten': 0  # Optimism is key
    }
    db.append(entry)
    save_db(db)
    print(f"✓ Added: '{problem[:50]}...' (You'll forget this in 3-6 months)")

def search_solutions(query):
    """Searches for answers you already have but can't find in your brain"""
    db = load_db()
    results = []
    query_lower = query.lower()
    
    for entry in db:
        if (query_lower in entry['problem'].lower() or 
            query_lower in entry['solution'].lower() or
            any(query_lower in tag.lower() for tag in entry['tags'])):
            
            # Increment the shame counter
            entry['times_forgotten'] += 1
            results.append(entry)
    
    if results:
        save_db(db)  # Save the updated counters
        print(f"\n🔍 Found {len(results)} solutions you've already solved (embarrassing):")
        for i, entry in enumerate(results, 1):
            print(f"\n{i}. Problem: {entry['problem'][:80]}...")
            print(f"   Solution: {entry['solution'][:80]}...")
            print(f"   Tags: {', '.join(entry['tags'])}")
            print(f"   Forgotten {entry['times_forgotten']} times (try writing it down?)")
    else:
        print(f"\n🤷 No matches. Either you're learning or your search terms suck.")

def main():
    """Main function - because every script needs one, apparently"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python stack_sniffer.py add \"problem\" \"solution\" [tag1 tag2...]")
        print("  python stack_sniffer.py search \"query\"")
        print("\nExample: python stack_sniffer.py add \"parse JSON\" \"import json\" python beginner")
        return
    
    command = sys.argv[1]
    
    if command == 'add' and len(sys.argv) >= 4:
        problem = sys.argv[2]
        solution = sys.argv[3]
        tags = sys.argv[4:] if len(sys.argv) > 4 else None
        add_solution(problem, solution, tags)
    elif command == 'search' and len(sys.argv) >= 3:
        query = sys.argv[2]
        search_solutions(query)
    else:
        print("Invalid command. Did you forget how to use your own tool? Classic.")

if __name__ == '__main__':
    main()
