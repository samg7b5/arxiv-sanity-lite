#!/usr/bin/env python3
"""
Interactive CLI for inspecting and editing user tags.
"""

from aslite import db

def list_users(tdb):
    print("Users in tags DB:")
    for i, user in enumerate(tdb.keys(), 1):
        print(f"{i}. {user}")

def view_user_tags(tdb, user):
    if user not in tdb:
        print(f"User '{user}' not found.")
        return
    tags = tdb[user]
    if not tags:
        print(f"No tags for user '{user}'.")
        return
    print(f"Tags for user '{user}':")
    for tag, papers in tags.items():
        print(f"  {tag} ({len(papers)} papers): {sorted(papers)}")

def add_tag(tdb, user, tag):
    tags = tdb.get(user, {})
    if tag in tags:
        print(f"Tag '{tag}' already exists for user '{user}'.")
    else:
        tags[tag] = set()
        tdb[user] = tags
        print(f"Added tag '{tag}' for user '{user}'.")

def add_paper_to_tag(tdb, user, tag, pid):
    tags = tdb.get(user, {})
    if tag not in tags:
        print(f"Tag '{tag}' does not exist for user '{user}'. Creating it.")
        tags[tag] = set()
    tags[tag].add(pid)
    tdb[user] = tags
    print(f"Added paper '{pid}' to tag '{tag}' for user '{user}'.")

def remove_paper_from_tag(tdb, user, tag, pid):
    tags = tdb.get(user, {})
    if tag not in tags or pid not in tags[tag]:
        print(f"Paper '{pid}' not found in tag '{tag}' for user '{user}'.")
        return
    tags[tag].remove(pid)
    tdb[user] = tags
    print(f"Removed paper '{pid}' from tag '{tag}' for user '{user}'.")

def main():
    tdb = db.get_tags_db(flag='c', autocommit=True)
    print("=== Interactive Tag Manager ===")
    
    while True:
        print("\nOptions:")
        print(" 1. List users")
        print(" 2. View a user’s tags")
        print(" 3. Add a new tag to a user")
        print(" 4. Add a paper to a tag")
        print(" 5. Remove a paper from a tag")
        print(" 6. Quit")

        choice = input("Enter option number: ").strip()
        
        if choice == '1':
            list_users(tdb)
        elif choice == '2':
            user = input("Enter username: ").strip()
            view_user_tags(tdb, user)
        elif choice == '3':
            user = input("Enter username: ").strip()
            tag = input("Enter new tag name: ").strip()
            add_tag(tdb, user, tag)
        elif choice == '4':
            user = input("Enter username: ").strip()
            tag = input("Enter tag name: ").strip()
            pid = input("Enter paper ID (e.g., 2505.11111): ").strip()
            add_paper_to_tag(tdb, user, tag, pid)
        elif choice == '5':
            user = input("Enter username: ").strip()
            tag = input("Enter tag name: ").strip()
            pid = input("Enter paper ID to remove: ").strip()
            remove_paper_from_tag(tdb, user, tag, pid)
        elif choice == '6':
            print("Exiting.")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()
