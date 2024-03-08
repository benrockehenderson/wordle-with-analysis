from helpers import ALL_STATUSES, INCORRECT, CORRECT, WRONG_POSITION, cartesian_product_general
import visualizer


def is_correct_char(answer: str, guess: str, i: int) -> bool:
    """Return whether the character status of guess[i] with respect to answer is CORRECT.

    Preconditions:
    - len(answer) == len(guess)
    - 0 <= i < len(answer)

    >>> is_correct_char('teach', 'adieu', 3)
    False
    >>> is_correct_char('teaching', 'reacting', 1)
    True
    """

    return guess[i] == answer[i]



def is_wrong_position_char(answer: str, guess: str, i: int) -> bool:
    """Return whether the character status of guess[i] with respect to answer is WRONG_POSITION.

    Preconditions:
    - len(answer) == len(guess)
    - 0 <= i < len(answer)

    >>> is_wrong_position_char('teach', 'adieu', 3)
    True
    >>> is_wrong_position_char('teaching', 'reacting', 1)
    False
    >>> # Cases with duplicate characters!
    >>> is_wrong_position_char('hello', 'hoops', 1)
    True
    >>> is_wrong_position_char('hello', 'hoops', 2)
    True
    >>> # Case that counts as 'incorrect' rather than 'wrong position' due to guess already being correct at the
    >>> # right position index
    >>> is_wrong_position_char('hello', 'keeps', 2)
    False
    """

    return guess[i] != answer[i] and any(
        {guess[i] == answer[j] and guess[j] != answer[j] and j != i and j < len(guess) for j in range(0, len(answer))})



def is_incorrect_char(answer: str, guess: str, i: int) -> bool:
    """Return whether the character status of guess[i] with respect to answer is INCORRECT.

    Preconditions:
    - len(answer) == len(guess)
    - 0 <= i < len(answer)

    >>> is_incorrect_char('teach', 'adieu', 1)
    True
    >>> is_incorrect_char('teaching', 'reacting', 1)
    False
    >>> is_incorrect_char('hello', 'keeps', 2)
    True

    HINT: you can use the previous two status functions to implement this one.
    """
    return not is_correct_char(answer, guess, i) and not is_wrong_position_char(answer, guess, i)



def get_character_status(answer: str, guess: str, i: int) -> str:
    """Return the character status of guess[i] with respect to answer.

    The return value is one of the three values {INCORRECT, WRONG_POSITION, CORRECT}.

    Preconditions:
    - len(answer) == len(guess)
    - 0 <= i < len(answer)

    >>> get_character_status('teach', 'adieu', 1) == INCORRECT
    True
    >>> get_character_status('teaching', 'reacting', 1) == CORRECT
    True
    """
    if is_correct_char(answer, guess, i):
        return CORRECT
    elif is_wrong_position_char(answer, guess, i):
        return WRONG_POSITION
    else:
        return INCORRECT



def get_guess_status(answer: str, guess: str) -> list[str]:
    """Return the guess status of the given guess with respect to answer.

    The return value is a list with the same length as guess, whose
    elements are all in the set {INCORRECT, WRONG_POSITION, CORRECT}.

    Preconditions:
    - answer != ''
    - len(answer) == len(guess)

    >>> example_status = get_guess_status('teach', 'adieu')
    >>> example_status == [WRONG_POSITION, INCORRECT, INCORRECT, WRONG_POSITION, INCORRECT]
    True
    """
    return [get_character_status(answer, guess, i) for i in range(0, len(answer))]


def get_guesses_statuses(answer: str, guesses: list[str]) -> list[list[str]]:
    """Return the guess statuses of each given guess with respect to answer.

    The return value is a list with the same length as guesses, where each status has
    elements that are all in the set {INCORRECT, WRONG_POSITION, CORRECT}.

    Preconditions:
    - answer != ''
    - all({len(answer) == len(guess) for guess in guesses})

    >>> example_statuses = get_guesses_statuses('teach', ['adieu'])
    >>> example_statuses == [[WRONG_POSITION, INCORRECT, INCORRECT, WRONG_POSITION, INCORRECT]]
    True
    """
    return [[get_character_status(answer, guess, i) for i in range(0, len(answer))] for guess in guesses]


def part3a_example(answer: str, guesses: list[str]) -> None:
    """Visualize the Wordle game for the given answer and guesses.

    >>> answer = 'hello'
    >>> guesses = ['reach', 'allow', 'keeps', 'hoops']
    >>> part3a_example(answer, guesses)
    """

    statuses = get_guesses_statuses(answer, guesses)
    visualizer.draw_wordle(answer, guesses, statuses)



@check_contracts
def is_potential_single(word: str, guess: str, status: list[str]) -> bool:
    """Return whether the given word is a potential answer for the given guess and status.

    Preconditions:
    - len(word) == len(guess) == len(status)
    - _is_valid_status(status)
    - word != ''

    >>> is_potential_single('later', 'tower', [WRONG_POSITION, INCORRECT, INCORRECT, CORRECT, CORRECT])
    True
    >>> is_potential_single('later', 'tower', [INCORRECT] * 5)
    False
    """
    return get_guess_status(word, guess) == status


@check_contracts
def is_potential_multiple(word: str, guesses: list[str], statuses: list[list[str]]) -> bool:
    """Return whether the given word is a potential answer for the given guesses and statuses.

    Preconditions:
    - len(guesses) == len(statuses)
    - all({len(word) == len(guess) for guess in guesses})
    - all({len(word) == len(status) for status in statuses})
    - all({_is_valid_status(status) for status in statuses})
    - word != ''

    >>> example_guesses = ['tower', 'lower', 'power', 'round']
    >>> example_statuses = [
    ...     [WRONG_POSITION, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [CORRECT, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [INCORRECT, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [WRONG_POSITION, INCORRECT, INCORRECT, INCORRECT, INCORRECT]
    ... ]
    >>> is_potential_multiple('later', example_guesses, example_statuses)
    True
    """

    return all([is_potential_single(word, guesses[i], statuses[i]) for i in range(0, len(guesses))])


@check_contracts
def find_potential_answers(word_set: set[str],
                           guesses: list[str], statuses: list[list[str]]) -> list[str]:
    """Return the list of words (from word_set) that are potential answers for the given guesses and statuses.

    The returned list is in alphabetical order

    Preconditions:
    - all words in word_set have the same non-zero length
    - all({guess in word_set for guess in guesses})
    - len(guesses) == len(statuses)
    - all({len(guesses[i]) == len(statuses[i]) for i in range(0, len(guesses))})
    - all({_is_valid_status(status) for status in statuses})

    >>> example_word_set = {'later', 'liter', 'tower', 'lower', 'power', 'round', 'tiger'}
    >>> example_guesses = ['tower', 'lower', 'power', 'round']
    >>> example_statuses = [
    ...     [WRONG_POSITION, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [CORRECT, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [INCORRECT, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [WRONG_POSITION, INCORRECT, INCORRECT, INCORRECT, INCORRECT]
    ... ]
    >>> find_potential_answers(example_word_set, example_guesses, example_statuses)
    ['later', 'liter']
    """

    return sorted([word for word in word_set if is_potential_multiple(word, guesses, statuses)])


@check_contracts
def part3b_example(word_set_file: str, guesses: list[str], statuses: list[list[str]]) -> None:
    """Visualize the Wordle game (with correct answers!) for the given guesses and statuses.

    Preconditions:
        - all words in the word_set_file have the same non-zero length
        - all guesses appear in the word_set_file
        - guesses and statuses satisfy all preconditions of find_potential_answers

    Note: This function is already completed for you. DO NOT MODIFY THIS FUNCTION.
    """
    with open(word_set_file) as f:
        # word_set is assigned to a set[str] containing the words in the file
        word_set = {str.strip(w) for w in f.readlines()}

    correct_answers = find_potential_answers(word_set, guesses, statuses)
    visualizer.draw_wordle_answers(correct_answers, guesses, statuses)



@check_contracts
def find_potential_guesses_single(word_set: set[str], answer: str, status: list[str]) -> list[str]:
    """Return the list of guesses from word_set that are consistent with the answer and status.

    The returned list is in alphabetical order.

    Preconditions:
    - answer != ''
    - answer in word_set
    - all words in word_set have the same non-zero length
    - len(answer) == len(status)
    - _is_valid_status(status)

    >>> example_word_set = {'later', 'liter', 'tower', 'lower', 'power', 'round', 'tiger'}
    >>> example_status = [WRONG_POSITION, INCORRECT, INCORRECT, CORRECT, CORRECT]
    >>> find_potential_guesses_single(example_word_set, 'later', example_status)
    ['tiger', 'tower']
    """
    return sorted([word for word in word_set if is_potential_single(answer, word, status)])


@check_contracts
def find_guesses_multiple(word_set: set[str],
                          answer: str, statuses: list[list[str]]) -> list[list[str]]:
    """Return the possible guess words from word_set that are consistent with the answer and statuses.

    The returned value is a list of lists, where each of the inner lists is a sequence of words that yields
    the given statuses with respect to the given answer.

    IMPORTANT: Call the sorted function on the list of lists before returning it. This will ensure
    that the inner lists are sorted alphabetically by their first words, breaking ties by comparing
    their second words, etc.

    Preconditions:
    - answer != ''
    - answer in word_set
    - all words in word_set have the same non-zero length
    - all({len(answer) == len(status) for status in statuses})
    - all({_is_valid_status(status) for status in statuses})

    >>> example_word_set = {'later', 'liter', 'tower', 'lower', 'power', 'round', 'tiger'}
    >>> example_statuses = [
    ...     [WRONG_POSITION, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [CORRECT, INCORRECT, INCORRECT, CORRECT, CORRECT]
    ... ]
    >>> find_guesses_multiple(example_word_set, 'later', example_statuses)
    [['tiger', 'lower'], ['tower', 'lower']]

    Note that ['tiger', 'lower'] comes before ['tower', 'lower'] because 'tiger' comes before
    'tower' alphabetically.
    """
    results = [find_potential_guesses_single(word_set, answer, status) for status in statuses]
    return cartesian_product_general(results)


@check_contracts
def visualize_part3c(word_set_file: str, answer: str, statuses: list[list[str]]) -> None:
    """Visualize the Wordle game (with reverse-engineered guesses!) for the given answer and statuses.

    

    1. First, read in the words in word_set_file. You can reuse the same code from
       part3b_example for this step.
    2. Then, compute the possible guesses for the given answer and statuses.
    3. Then, call visualizer.draw_wordle_guesses to display the result!

    Preconditions:
        - answer appears in the word_set_file
        - all words in the word_set_file have the same non-zero length
        - answer and statuses satisfy the preconditions of find_guesses_multiple
    """

    with open(word_set_file) as f:
        # word_set is assigned to a set[str] containing the words in the file
        word_set = {str.strip(w) for w in f.readlines()}
        possible_guesses = find_guesses_multiple(word_set, answer, statuses)
        a2_visualizer.draw_wordle_guesses(answer, possible_guesses, statuses)


@check_contracts
def information_score(answer: str, guess: str) -> float:
    """Return the information score of guess with respect to answer.

    See assignment handout for the formula for information score.

    Preconditions:
    - len(answer) == len(guess)
    - answer != ''
    >>> information_score('later', 'tiger')
    2.5
    """
    status = get_guess_status(answer, guess)
    return list.count(status, CORRECT) + 0.5 * list.count(status, WRONG_POSITION)


def information_score_multiple(potential_answers: set[str], p_answer: str) -> float:
    """ Helper function for find_answers_and_scores:
    Return the average info score for p_answer in potential_answers

    >>> information_score_multiple({'reach', 'tiger', 'tower'}, 'tiger')
    3.0
    """
    total = sum([information_score(potential_answer, p_answer) for potential_answer in potential_answers])
    length = len(potential_answers)
    return total / length


@check_contracts
def find_answers_and_scores(word_set: set[str],
                            guesses: list[str], statuses: list[list[str]]) -> dict[str, float]:
    """Return a mapping from possible correct answers to their average information score (see handout for details).

    Preconditions:
    - all words in word_set have the same non-zero length
    - all({guess in word_set for guess in guesses})
    - len(guesses) == len(statuses)
    - all({len(guesses[i]) == len(statuses[i]) for i in range(0, len(guesses))})
    - all({_is_valid_status(status) for status in statuses})
    - There is at least one possible correct answer

    >>> example_word_set = {'later', 'liter', 'tower', 'lower', 'power', 'round', 'tiger'}
    >>> example_guesses = ['tower', 'lower', 'power', 'round']
    >>> example_statuses = [
    ...     [WRONG_POSITION, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [CORRECT, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [INCORRECT, INCORRECT, INCORRECT, CORRECT, CORRECT],
    ...     [WRONG_POSITION, INCORRECT, INCORRECT, INCORRECT, INCORRECT]
    ... ]
    >>> find_answers_and_scores(example_word_set, example_guesses, example_statuses)
    {'later': 4.5, 'liter': 4.5}
    """
    potential_answers = find_potential_answers(word_set, guesses, statuses)
    return {potential_answer: information_score_multiple(potential_answers, potential_answer) for potential_answer in
            potential_answers}



@check_contracts
def _is_valid_status(status: list[str]) -> bool:
    """Return whether s is a valid status.

    A valid status is a list that contains only the three statuses in ALL_STATUSES.
    This function is used in some of the precondition expressions in this file.
    """
    return all({char_status in ALL_STATUSES for char_status in status})



