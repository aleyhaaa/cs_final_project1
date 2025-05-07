from database import (
    setup_db, get_candidates, add_candidate,
    has_voted, register_voter, record_vote, count_votes
)

def vote_menu():
    """
    Displays the main vote menu and returns the user's option.
    """
    print('---------------')
    print('VOTE MENU')
    print('---------------')
    print('a: Add Candidate')
    print('v: Vote')
    print('r: Results')
    print('x: Exit')
    option = input('Option: ').strip().lower()
    return option

def add_candidate_flow():
    """
    Handles adding a new candidate to the database (max 4 candidates).
    """
    candidates = get_candidates()
    if len(candidates) >= 4:
        print("Cannot add more than 4 candidates.")
        return
    name = input("Enter candidate name: ").strip()
    if name:
        add_candidate(name)
        print(f"{name} added.")
    else:
        print("Candidate name cannot be empty.")

def candidate_menu():
    """
    Displays the list of candidates and prompts the user to select one by ID.
    Returns the selected candidate's ID.
    """
    candidates = get_candidates()
    if not candidates:
        print("No candidates available. Add some first!")
        return None

    print('---------------')
    print('CANDIDATE MENU')
    print('---------------')
    for cid, name in candidates:
        print(f"{cid}: {name}")

    while True:
        try:
            can_option = int(input("Choose a candidate by number: "))
            if any(cid == can_option for cid, _ in candidates):
                return can_option
            else:
                print("Invalid candidate ID.")
        except ValueError:
            print("Please enter a valid number.")

def vote_flow():
    """
    Prompts user for voter ID, checks if they already voted,
    and records their vote if valid.
    """
    voter_id = input("Enter your voter ID: ").strip()
    if has_voted(voter_id):
        print("You have already voted.")
        return

    candidate_id = candidate_menu()
    if candidate_id:
        record_vote(candidate_id, voter_id)
        register_voter(voter_id)
        print("Vote recorded!")

def show_results():
    """
    Retrieves and displays current voting results and the winner.
    """
    results = count_votes()
    print('---------------')
    print("Voting Results:")
    for name, total in results:
        print(f"{name}: {total} votes")
    if results:
        winner = results[0][0]
        print(f"🏆 Winner: {winner}")
    print('---------------')

def main():
    """
    Main application loop to handle voting system operations.
    """
    setup_db()
    while True:
        option = vote_menu()
        if option == 'a':
            add_candidate_flow()
        elif option == 'v':
            vote_flow()
        elif option == 'r':
            show_results()
        elif option == 'x':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
