"""
Lab 1 - Improved Program
Aleyha Alelawi
"""

#this program will tally votes of different canidates

def vote_menu():
        print('---------------')
        print('VOTE MENU')
        print('---------------')
        print('v: Vote')
        print('x: Exit')
        option = input('Option: ').strip().lower()
        
        if option in ['v', 'x']:
            return option
        else:
            invalid = input('Invalid (v/x): ').strip().lower()


def candidate_menu():
    candidate = {1: 'John', 2: 'Jane'}
    print('---------------')
    print('CANDIDATE MENU')
    print('---------------')
    
    for number, name in candidate.items():
        print(f'{number}: {name}')
    
    can_option = input('Candidate: ')
        
    while True:
        if can_option.isdigit():
            can_option = int(can_option)
            if can_option in candidate:
                print(f'Voted {candidate[can_option]}')
                return candidate[can_option]
        can_option = input('Invalid (1/2): ').strip()


def main():
    vote_count = {'John': 0, 'Jane': 0}
    
    while True:
        option = vote_menu()
        
        if option == 'v':
            candidate = candidate_menu()
            vote_count[candidate] += 1
        elif option == 'x':
            print('---------------')
            print(f"John - {vote_count['John']}, Jane - {vote_count['Jane']}, Total - {sum(vote_count.values())}")
            print('---------------')
            break
main()

            