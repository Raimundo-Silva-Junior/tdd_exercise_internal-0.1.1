Caktus Django Coding Exercise
=============================

Using Django 2.2 or higher, and Python 3.6 or higher, create a Django project that meets the
requirements listed below and passes the tests contained herein.

A few additional recommendations:

- Review the tests in detail before implementing the business logic, as they include a few
  assumptions about how the views will be structured.
- Create a git repository for the project and use the first commit to import this initial project
  skeleton. Then, try to break up the changes into at least a few logically separate commits with
  commit messages **briefly** explaining what each commit does.
- A base HTML template is included for convenience, but you're free to replace this with another of
  your choosing.
- The finished product doesn't need to be deployed anywhere, and continuing to use sqlite3 as the
  database backend is fine. (If you prefer not to use sqlite3, please use Postgres instead.)
- Set aside no more than 3 hours for the exercise. The full project will almost certainly take
  longer than this. At or around the 3 hour mark, find a good stopping point and return what you
  have so far.

Good luck and have fun!


Project Requirements
--------------------


Data Models
~~~~~~~~~~~

The project to be built is a crossword drill exercise program. It presents clues to the user and
accepts guesses for answers, tracking how many clues have been offered and how many have been
answered successfully. To aid in building the project, a fixtures file is included that contains
realistic crossword puzzle data. The fixture contains three models with the following fields:

- Puzzle: published crossword puzzle
   * ``title``, optional, maximum 255 characters
   * ``date``, required (publication date)
   * ``byline``, required, maximum 255 characters
   * ``publisher``, required, maximum 12 characters
- Entry
   * ``entry_text``, required and unique, maximum 50 characters
- Clue
   * ``entry``, reference to an Entry
   * ``puzzle``, reference to a Puzzle
   * ``clue_text``, required, maximum 512 characters
   * ``theme``, boolean, default ``False`` (not used by the project but contained in the fixtures
     file)

Crossword puzzle entries are typically shown always in all-uppercase characters, the project code
should follow this convention but also allow for users to enter lowercase and have it be coerced
to upper case for checking matches.


Views
~~~~~

The project should have two views:

- **Drill view:** presents a random clue with information about the entry (length and puzzle
  where it appeared) to the user, and includes an input field where the user can provide a guess
  at the answer. Input of an incorrect guess should re-display the same clue with a note the answer
  is not correct. Input of a correct answer should redirect to the answer view for that clue.
  The drill view's rendered page should offer the user an "escape hatch" to see the answer even
  if they cannot correctly guess it.

- **Answer view:** when reached via a successful guess, this view congratulates the user on their
  success and offers up some additional data about the clue. If this is the only occurrence of the
  clue in the database then that is stated. If, however, the clue appears more than once in the
  database then the answer page for the clue presents a table of Entries associated with the clue
  and a count of how many times that Clue/Entry pair appear in the database.


Tests
-----

Tests are provided in the ``xword_data/tests`` subdirectory. The project code should allow these
tests to run successfully. Note the tests use factory-boy and beautifulsoup4 (specific versions can
be found in the requirements file).


Critique
--------

Feel free to provide feedback on any potential errors or poor practices in the test code or model
structures!
