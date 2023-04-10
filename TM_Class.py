class BinaryAdditionTM:
    def __init__(self, tape):
        self.tape = tape
        self.head = 0
        self.state = 'q0'

    def transition(self):
        if self.state == 'q0':
            if self.tape[self.head] == '0':
                self.tape[self.head] = '1'
                self.head += 1
                self.state = 'q1'
            elif self.tape[self.head] == '1':
                self.tape[self.head] = '0'
                self.head += 1
                self.state = 'q0'
            else:
                self.state = 'halt'
        elif self.state == 'q1':
            if self.tape[self.head] == '0':
                self.tape[self.head] = '0'
                self.head -= 1
                self.state = 'q2'
            elif self.tape[self.head] == '1':
                self.tape[self.head] = '1'
                self.head += 1
            else:
                self.state = 'halt'
        elif self.state == 'q2':
            if self.tape[self.head] == '0':
                self.tape[self.head] = '1'
                self.head -= 1
            elif self.tape[self.head] == '1':
                self.tape[self.head] = '0'
                self.head -= 1
                self.state = 'q1'
            else:
                self.state = 'halt'
        elif self.state == 'q3':
            self.state = 'halt'

        if self.state == 'halt':
            # Compute the sum of the binary numbers on the tape
            tape_str = ''.join(self.tape)
            num1, num2 = tape_str.split('#')
            result = bin(int(num1, 2) + int(num2, 2))[2:]
            # Print the result
            print('Result:', result)
        else:
            # Print the current state and tape contents
            print('State:', self.state)
            print('Tape:', ''.join(self.tape))

tape = list('111#110')
tm = BinaryAdditionTM(tape)
while tm.state != 'halt':
    tm.transition()
