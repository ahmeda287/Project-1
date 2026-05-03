import csv
from PyQt6.QtWidgets import QMainWindow
from gui import Ui_MainWindow


class Logic(QMainWindow, Ui_MainWindow):
    """
    A class representing the logic of a GUI voting application.
    Inherits from QMainWindow and the generated Ui_MainWindow class.
    Imports csv to use csv stuff
    """

    RESULTS_FILE: str = 'results.csv'
    VOTER_ID_FILE: str = 'voter_ids.csv'

    def __init__(self) -> None:
        """
        Method to initialize the Logic window, set default instance variables,
        load voter IDs from file, and connect all GUI buttons to their correct methods.
        """
        super().__init__()
        self.setupUi(self)

        self.__votes: dict[str, int] = {
            'Isabella': 0,
            'Genji': 0,
            'Hannah': 0,
            'Jane': 0,
            'Jack': 0,
            'John': 0
        }
        self.__voter_ids: dict[str, int] = {}

        self.__load_voter_ids()

        self.submit_vote.clicked.connect(self.__submit_vote)
        self.finish_voting.clicked.connect(self.__finish_voting)

    def __load_voter_ids(self) -> None:
        """
        Method to load voter IDs and their voted status from the voter_ids_csv file.
        Sets an error message if the file is not found or cannot be read.
        """
        try:
            with open(Logic.VOTER_ID_FILE, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    self.__voter_ids[row[0].strip()] = int(row[1].strip())
        except FileNotFoundError:
            self.__set_error(f'voter_ids.csv not found.')
        except:
            self.__set_error('Could not load voter IDs.')

    def __get_selected_candidate(self) -> str:
        """
        Method to determine which candidate radio button is currently selected.
        :return: The name of the selected candidate, or an empty string if none is selected.
        """
        if self.option_isabbela.isChecked():
            return 'Isabella'
        elif self.option_genji.isChecked():
            return 'Genji'
        elif self.option_hannah.isChecked():
            return 'Hannah'
        elif self.option_jane.isChecked():
            return 'Jane'
        elif self.option_jack.isChecked():
            return 'Jack'
        elif self.option_john.isChecked():
            return 'John'
        return ''

    def __submit_vote(self) -> None:
        """
        Method to validate and submit a vote for the selected candidate.
        Validates that the voter ID is a non-empty 4-digit number, exists in the voter ID file,
        and has not already voted. Sets an error message for any failed validation.
        When successful it increments the candidate's vote count and marks the voter ID as used which is 1 and 0 for unused.
        """
        voter_id: str = self.voter_id.text().strip()

        if voter_id == '':
            self.__set_error('Please enter a voter ID.')
            return

        if not voter_id.isdigit() or len(voter_id) != 4:
            self.__set_error('Voter ID must be a 4-digit number.')
            return

        if self.__voter_ids.get(voter_id, '') == '':
            self.__set_error('Voter ID not found.')
            return

        if self.__voter_ids[voter_id] == 1:
            self.__set_error('This voter ID has already voted.')
            return

        candidate: str = self.__get_selected_candidate()
        if candidate == '':
            self.__set_error('Please select a candidate.')
            return

        self.__votes[candidate] += 1
        self.__voter_ids[voter_id] = 1
        self.voter_id.clear()
        self.option_isabbela.setChecked(False)
        self.option_genji.setChecked(False)
        self.option_hannah.setChecked(False)
        self.option_jane.setChecked(False)
        self.option_jack.setChecked(False)
        self.option_john.setChecked(False)

        self.__set_success(f'Vote cast for {candidate} successfully.')

    def __update_voter_ids_csv(self) -> None:
        """
        Method to write the current voter ID voted statuses back to the voter_ids_csv file.
        Sets an error message if the file cannot be written.
        """
        try:
            with open(Logic.VOTER_ID_FILE, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['Voter ID', 'Voted status'])
                for key in self.__voter_ids:
                    writer.writerow([key, self.__voter_ids[key]])
        except:
            self.__set_error('Could not update voter file.')

    def __finish_voting(self) -> None:
        """
        Method to end the voting session by saving results and disabling voting buttons.
        """
        self.__save_results()
        self.__disable_voting()

    def __save_results(self) -> None:
        """
        Method to save the final vote totals to the results.csv file and display the results.
        Updates the voter_ids.csv file with correct voter_id vote statues before writing results.
        Sets an error message if the results file cannot be written.
        """
        self.__update_voter_ids_csv()

        total_votes: int = 0
        for candidate in self.__votes:
            total_votes += self.__votes[candidate]

        try:
            with open(Logic.RESULTS_FILE, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['Results'])
                writer.writerow(['Total Votes', total_votes])
                for candidate in self.__votes:
                    writer.writerow([candidate, self.__votes[candidate]])
            self.__display_results()
        except Exception:
            self.__set_error('Could not save results.')

    def __display_results(self) -> None:
        """
        Method to determine and display the winner of the election.
        Handles tie and zero-vote edge cases.
        Displays the winner and a confirmation that results were saved to results.csv.
        """
        winner: str = ''
        vote_count: int = 0
        for candidate in self.__votes:
            if self.__votes[candidate] > vote_count:
                winner = candidate
                vote_count = self.__votes[candidate]

        tie_check: int = 0
        for candidate in self.__votes:
            if self.__votes[candidate] == vote_count:
                tie_check += 1
        if tie_check > 1:
            winner = 'Tie between 2 or more candidates'
        if vote_count == 0:
            winner = 'No votes cast all vote counts 0'

        result_text: str = f'Winner is {winner}\nSuccesfuly saved candidate vote counts \nto results.csv file'
        self.__set_success(result_text.strip())

    def __disable_voting(self) -> None:
        """
        Method to disable all voting buttons after the voting session has ended.
        """
        self.voter_id.setEnabled(False)
        self.submit_vote.setEnabled(False)
        self.finish_voting.setEnabled(False)

    def __set_error(self, message: str) -> None:
        """
        Method to display an error message in red in the status label.
        :param message: The error message string to display.
        """
        self.error_text.setStyleSheet('color: red;')
        self.error_text.setText(message)

    def __set_success(self, message: str) -> None:
        """
        Method to display a successful/info message in black in the status label.
        :param message: The success message string to display.
        """
        self.error_text.setStyleSheet('color: black;')
        self.error_text.setText(message)
