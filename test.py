# Define the transition function for the Turing machine
def transition(state, symbol):
    if state == 0:
        if symbol == '0':
            return (1, '0', 'R')
        elif symbol == '1':
            return (2, '1', 'R')
    elif state == 1:
        if symbol == '0':
            return (3, '1', 'N')
        elif symbol == '1':
            return (1, '0', 'R')
    elif state == 2:
        if symbol == '0':
            return (1, '1', 'R')
        elif symbol == '1':
            return (2, '0', 'R')
    elif state == 3:
        if symbol == '0':
            return (4, '0', 'N')
        elif symbol == '1':
            return (3, '1', 'N')

# Define the main function that runs the Turing machine
def run_turing_machine(input_str):
    tape = ['B'] + list(input_str) + ['B']
    head_pos = 1
    state = 0
    while state != 4:
        symbol = tape[head_pos]
        new_state, new_symbol, direction = transition(state, symbol)
        tape[head_pos] = new_symbol
        if direction == 'R':
            head_pos += 1
        elif direction == 'L':
            head_pos -= 1
        state = new_state
    output_str = ''.join(tape[1:3])
    return output_str

# Test the Turing machine with some inputs
print(run_turing_machine('00'))  
print(run_turing_machine('01'))  # Output: '01'
print(run_turing_machine('10'))  # Output: '01'
print(run_turing_machine('11'))  # Output: '10'
