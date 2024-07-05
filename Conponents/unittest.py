import unittest
from unittest.mock import patch, MagicMock
from FA5 import FiniteAutomata
from NFA import NFA
from DFA import DFA
import gui

class TestFiniteAutomaton(unittest.TestCase):

    @patch('builtins.input', side_effect=['3', 'a b', 'q0', 'q2', 'q0 a q1', 'q1 b q2', 'q2 a q0'])
    def test_create_fa(self, mock_input):
        fa = FiniteAutomata()
        fa.get_user_input()

        self.assertEqual(fa.states, {'q0', 'q1', 'q2'})
        self.assertEqual(fa.alphabet, {'a', 'b'})
        self.assertEqual(fa.initial_state, 'q0')
        self.assertEqual(fa.final_states, {'q2'})
        self.assertEqual(fa.transitions, {
            'q0': {'a': {'q1'}},
            'q1': {'b': {'q2'}},
            'q2': {'a': {'q0'}}
        })

class TestFiniteAutomatonGUI(unittest.TestCase):

    def setUp(self):
        self.root = MagicMock()
        self.app = gui.FiniteAutomatonGUI(self.root)

    def test_create_fa(self):
        self.app.num_states_entry.get = MagicMock(return_value='3')
        self.app.alphabet_entry.get = MagicMock(return_value='a b')
        self.app.initial_state_entry.get = MagicMock(return_value='q0')
        self.app.final_states_entry.get = MagicMock(return_value='q2')
        self.app.transitions_text.get = MagicMock(return_value='q0 a q1\nq1 b q2\nq2 a q0')

        self.app.create_fa()

        fa = self.app.fa
        self.assertIsInstance(fa, FiniteAutomata)
        self.assertEqual(fa.states, {'q0', 'q1', 'q2'})
        self.assertEqual(fa.alphabet, {'a', 'b'})
        self.assertEqual(fa.initial_state, 'q0')
        self.assertEqual(fa.final_states, {'q2'})
        self.assertEqual(fa.transitions, {
            'q0': {'a': {'q1'}},
            'q1': {'b': {'q2'}},
            'q2': {'a': {'q0'}}
        })

if __name__ == '__main__':
    unittest.main()
