import unittest
from pyknon.musiclib import MusiclibError, Note, NoteSeq, Rest


def seq_from_numbers(*args):
    return NoteSeq([Note(value=x) if x >= 0 else Rest() for x in args])


def seq_from_alist(*args):
    """((val, dur))
    """
    return NoteSeq([Note(val, dur) for val, dur in args])


class TestRest(unittest.TestCase):
    def test_stretch_dur(self):
        n1 = Rest(dur=0.25)
        n2 = n1.stretch_dur(2)
        n3 = n1.stretch_dur(0.5)
        self.assertEqual(n2.dur, 0.5)
        self.assertEqual(n3.dur, 0.125)

    def test_repr(self):
        representation = Rest(0.5).__repr__()
        self.assertEqual(representation, "<Rest: 0.5>")



class TestNote(unittest.TestCase):
    def test_init(self):
        n1 = Note("C")
        n2 = Note(value=6, octave=6, dur=0.125, volume=120)
        n3 = Note()
        n4 = Note(2)
        self.assertEqual(n1, Note(0))
        self.assertEqual(n2, Note(6, 6, 0.125, 120))
        self.assertEqual(n2, Note("F#8''", volume=120))
        self.assertEqual(n3, n1)
        self.assertEqual(n4, Note("D"))

    def test_repr(self):
        representation = Note(value=3, octave=5).__repr__()
        self.assertEqual(representation, "<Note: 3.5>")

    def test_note_equal(self):
        self.assertFalse(Note(3) == Note(15))
        self.assertTrue(Note(3) == Note(3))

    def test_note_sub(self):
        self.assertEqual(Note(4) - Note(3), 1)
        self.assertEqual(Note(3) - Note(4), -1)
        self.assertEqual(Note(25) - Note(1), 24)

    def test_transposition(self):
        c = Note(value=0)
        self.assertEqual(c.transposition(2), Note(value=2))
        self.assertEqual(c.transposition(0), Note(value=0))
        self.assertEqual(c.transposition(11), Note(value=11))

    def test_transposition_octave(self):
        e = Note(value=4, dur=0.25, octave=7)
        self.assertNotEqual(e.transposition(2), Note(value=6))
        self.assertEqual(e.transposition(2), Note(value=6, dur=0.25, octave=7))
        self.assertEqual(e.transposition(10), Note(value=2, dur=0.25, octave=8))

    def test_inversion(self):
        self.assertEqual(Note(3, 5).inversion(0), Note(9, 4))

    def test_note_list(self):
        note = Note(value=4, dur=0.25, octave=3, volume=120)
        result = (4, 3, 0.25, 120)
        self.assertEqual(note.note_list(), result)

    def test_stretch_dur(self):
        n1 = Note(value=4, dur=0.25, octave=3)
        n2 = n1.stretch_dur(2)
        n3 = n1.stretch_dur(0.5)
        self.assertEqual(n2.dur, 0.5)
        self.assertEqual(n3.dur, 0.125)



class TestNoteSeqOperations(unittest.TestCase):
    def test_sum(self):
        seq1 = NoteSeq("C D E")
        seq2 = NoteSeq("F G A")
        seq3 = NoteSeq("C D E F G A")
        self.assertEqual(seq1 + seq2, seq3)

    def test_multiplication(self):
        seq1 = NoteSeq("C4 D8 E8")
        seq2 = NoteSeq("C4 D8 E8 C4 D8 E8 C4 D8 E8")
        self.assertEqual(seq1 * 3, seq2)

    def test_iteration(self):
        seq1 = NoteSeq("C D E F G A B")
        numbers = [x.value for x in seq1]
        self.assertEqual(numbers, [0, 2, 4, 5, 7, 9, 11])

    def test_delitem(self):
        seq1 = NoteSeq("C D E")
        del seq1[0]
        seq2 = NoteSeq("D E")
        self.assertEqual(seq1, seq2)

    def test_len(self):
        seq = NoteSeq("C D E F")
        self.assertEqual(len(seq), 4)

    def test_append(self):
        seq1 = NoteSeq("C# D#")
        seq1.append(Note("F#"))
        seq2 = NoteSeq("C# D# F#")
        self.assertEqual(seq1, seq2)

    def test_insert(self):
        seq1 = NoteSeq("Ab Bb Eb")
        seq1.insert(2, Note("C#"))
        seq2 = NoteSeq("Ab Bb C# Eb")
        self.assertEqual(seq1, seq2)

    def test_getitem(self):
        seq1 = NoteSeq("C D E")
        seq2 = NoteSeq("D E")
        self.assertEqual(seq1[0], Note("C"))
        self.assertEqual(seq1[1:], seq2)



class TestNoteSeq(unittest.TestCase):
    def test_init(self):
        notes = [Note(0, 5), Note(2, 5)]
        seq1 = NoteSeq(notes)
        seq2 = NoteSeq("C#2' D#4''")
        seq3 = NoteSeq([Note(1, 5, 0.5), Note(3, 6, 0.25)])
        self.assertEqual(seq1, NoteSeq(notes))
        self.assertEqual(seq2, seq3)
        self.assertNotEqual(seq1, NoteSeq(notes + [Note(3, 5)]))
        self.assertRaises(MusiclibError, NoteSeq, [Note(1, 5, 0.5), Rest(2), 1])
        self.assertRaises(MusiclibError, NoteSeq, 1)

    def test_init_string(self):
        seq1 = NoteSeq([Note(0, 4, 0.125), Note(2, 4, 0.125)])
        seq2 = NoteSeq([Note(0, 6, 0.125), Rest(0.25)])
        seq3 = NoteSeq([Note(0, 5, 0.25), Note(2, 5, 0.25)])
        self.assertEqual(NoteSeq("C8, D"), seq1)
        self.assertEqual(NoteSeq("c8, d"), seq1)
        self.assertEqual(NoteSeq("c8'' r4"), seq2)
        self.assertEqual(NoteSeq("C8'' R4"), seq2)
        self.assertEqual(NoteSeq("C D"), seq3)

    def test_init_with_rest(self):
        seq1 = NoteSeq("C4 R4 D4")
        seq2 = NoteSeq("C8 R D")
        seq3 = NoteSeq([Note(0, dur=0.25), Rest(0.25), Note(2, dur=0.25)])
        self.assertEqual(seq1[0].dur, 0.25)
        self.assertEqual(seq1[1].dur, 0.25)
        self.assertEqual(seq1[2].dur, 0.25)
        self.assertEqual(seq2[0].dur, 0.125)
        self.assertEqual(seq2[1].dur, 0.125)
        self.assertEqual(seq2[2].dur, 0.125)
        self.assertEqual(seq3[0].dur, 0.25)
        self.assertEqual(seq3[1].dur, 0.25)
        self.assertEqual(seq3[2].dur, 0.25)
        
    def test_transposition(self):
        seq = seq_from_numbers(0, 4, 7)
        self.assertEqual(seq.transposition(3), seq_from_numbers(3, 7, 10))
        self.assertEqual(seq.transposition(5), seq_from_numbers(5, 9, 12))

    def test_transposition_with_rest(self):
        seq1 = seq_from_numbers(0, -1, 4, 7)
        seq2 = seq_from_numbers(3, -1, 7, 10)
        self.assertEqual(seq1.transposition(3), seq2)

    def test_transposition_startswith(self):
        seq1 = seq_from_numbers(4, 7, 1)
        seq2 = NoteSeq([Note(2, 5), Note(5, 5), Note(11, 4)])
        seq3 = NoteSeq([Note(2, 4), Note(5, 4), Note(11, 3)])
        self.assertEqual(seq1.transposition_startswith(Note(2, 5)), seq2)
        self.assertEqual(seq1.transposition_startswith(Note(2, 4)), seq3)

    def test_transposition_startswith_integer(self):
        seq1 = NoteSeq("C D E")
        seq2 = NoteSeq("D E F#")
        self.assertEqual(seq1.transposition_startswith(2), seq2)

    def test_transposition_startswith_rest(self):
        seq1 = seq_from_numbers(4, 7, -1, 1)
        seq2 = NoteSeq([Note(2, 5), Note(5, 5), Rest(), Note(11, 4)])
        self.assertEqual(seq1.transposition_startswith(Note(2, 5)), seq2)

    def test_inversion(self):
        seq1 = seq_from_numbers(0, 4, 7)
        seq2 = NoteSeq([Note(0, 5), Note(8, 4), Note(5, 4)])
        self.assertEqual(seq1.inversion(0), seq2)

    def test_inversion_octave(self):
        seq1 = seq_from_alist((7, 5), (8, 5), (11, 4))
        seq2 = seq_from_alist((7, 5), (6, 5), (3, 6))
        self.assertEqual(seq1.inversion(7), seq2)

    def test_inversion_rest(self):
        seq1 = seq_from_numbers(0, 4, -1, 7)
        seq2 = NoteSeq([Note(0, 5), Note(8, 4), Rest(), Note(5, 4)])
        self.assertEqual(seq1.inversion(0), seq2)

    def test_inversion_startswith(self):
        seq1 = seq_from_numbers(0, 4, 7)
        seq2 = NoteSeq([Note(1, 5), Note(9, 4), Note(6, 4)])
        self.assertEqual(seq1.inversion_startswith(Note(1, 5)), seq2)

    def test_inversion_startswith_integer(self):
        seq1 = NoteSeq("C E G")
        seq2 = NoteSeq("C Ab, F,")
        self.assertEqual(seq1.inversion_startswith(0), seq2)


    def test_inversion_startswith_octave(self):
        seq1 = seq_from_alist((7, 5), (8, 5), (11, 4))
        seq2 = seq_from_alist((4, 5), (3, 5), (0, 6))
        self.assertEqual(seq1.inversion_startswith(Note(4, 5)), seq2)

    def test_rotate(self):
        seq1 = seq_from_numbers(0, 4, 7)
        seq2 = seq_from_numbers(4, 7, 0)
        seq3 = seq_from_numbers(7, 0, 4)
        self.assertEqual(seq1.rotate(0), seq1)
        self.assertEqual(seq1.rotate(1), seq2)
        self.assertEqual(seq1.rotate(2), seq3)
        self.assertEqual(seq1.rotate(3), seq1)

    def test_note_list(self):
        seq = NoteSeq([Note(0, 3, 0.25, 120), Note(4, 3, 0.25, 120),
                       Note(7, 3, 0.25, 120), Note(0, 3, 0.25, 120)])
        nlist = [(0, 3, 0.25, 120), (4, 3, 0.25, 120),
                 (7, 3, 0.25, 120), (0, 3, 0.25, 120)]

        self.assertEqual(seq.note_list(), nlist)

    def test_note_list_rest(self):
        seq = NoteSeq([Note(0, 3, 0.25, 120), Note(4, 3, 0.25, 120),
                       Rest(0.25), Note(0, 3, 0.25, 120)])
        nlist = [(0, 3, 0.25, 120), (4, 3, 0.25, 120),
                 (-1, 0, 0.25, 0), (0, 3, 0.25, 120)]

        self.assertEqual(seq.note_list(), nlist)

    def test_stretch_dur(self):
        seq1 = NoteSeq("C4 D8 E8")
        seq2 = NoteSeq("C8 D16 E16")
        seq3 = NoteSeq("C2 D4 E4")
        self.assertEqual(seq1.stretch_dur(.5), seq2)
        self.assertEqual(seq1.stretch_dur(2), seq3)

    def test_retrograde(self):
        seq1 = NoteSeq("C4 D8 E8")
        seq2 = NoteSeq("E8 D8 C4")
        self.assertEqual(seq1.retrograde(), seq2)

    def test_intervals(self):
        seq = NoteSeq("C D E F#")
        self.assertEqual(seq.intervals(), [2, 2, 2])

    def test_stretch_inverval(self):
        seq1 = NoteSeq("C D E")
        seq2 = NoteSeq("C E G#")
        seq3 = NoteSeq("A Bb F#")
        seq4 = NoteSeq("A C#'' C''")
        self.assertEqual(seq1.stretch_inverval(2), seq2)
        self.assertEqual(seq3.stretch_inverval(3), seq4)
