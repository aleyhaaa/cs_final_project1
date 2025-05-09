import sys
from PyQt6 import QtWidgets
from ui_vote import Ui_Form
from database import (
    setup_db, get_candidates, has_voted,
    record_vote, register_voter, count_votes,
    add_candidate
)

# NEW: helper to delete a candidate
import sqlite3
def delete_candidate(candidate_id):
    conn = sqlite3.connect("votes.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
    cur.execute("DELETE FROM votes WHERE candidate_id = ?", (candidate_id,))
    conn.commit()
    conn.close()

class VotingApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.candidate_buttons = [
            self.ui.radioButton,
            self.ui.radioButton_2,
            self.ui.radioButton_3,
            self.ui.radioButton_4
        ]

        self.load_candidates()

        self.ui.DoneButton.clicked.connect(self.submit_vote)
        self.ui.ResultsButton.clicked.connect(self.show_results)
        self.ui.CandidateButton.clicked.connect(self.add_new_candidate)
        self.ui.DeleteButton.clicked.connect(self.delete_candidate_prompt)  # 💣

    def load_candidates(self):
        """
        Load candidate names into radio buttons based on database.
        """
        self.candidates = get_candidates()
        for i, button in enumerate(self.candidate_buttons):
            if i < len(self.candidates):
                button.setText(self.candidates[i][1])
                button.setVisible(True)
            else:
                button.setVisible(False)

    def submit_vote(self):
        voter_id = self.ui.IDtextbox.toPlainText().strip()
        if not voter_id:
            self.show_message("Error", "Please enter a voter ID.")
            return
        if has_voted(voter_id):
            self.show_message("Error", "This voter has already voted.")
            return

        selected_id = None
        for i, button in enumerate(self.candidate_buttons):
            if button.isVisible() and button.isChecked():
                selected_id = self.candidates[i][0]
                break

        if selected_id is None:
            self.show_message("Error", "Please select a candidate.")
            return

        record_vote(selected_id, voter_id)
        register_voter(voter_id)
        self.show_message("Success", "Your vote has been recorded!")
        self.clear_form()

    def show_results(self):
        results = count_votes()
        if not results:
            self.show_message("Results", "No votes have been cast yet.")
            return

        result_text = "\n".join([f"{name}: {votes} votes" for name, votes in results])
        winner = results[0][0]
        result_text += f"\n\n🏆 Winner: {winner}"
        self.show_message("Voting Results", result_text)

    def add_new_candidate(self):
        if len(get_candidates()) >= 4:
            self.show_message("Error", "You can only have up to 4 candidates.")
            return

        name, ok = QtWidgets.QInputDialog.getText(self, "Add Candidate", "Enter candidate name:")
        if ok and name.strip():
            add_candidate(name.strip())
            self.load_candidates()
            self.show_message("Success", f"{name.strip()} added as a candidate!")
        elif ok:
            self.show_message("Error", "Candidate name cannot be empty.")

    def delete_candidate_prompt(self):
        """
        Show a dialog to select and delete a candidate.
        """
        self.candidates = get_candidates()
        if not self.candidates:
            self.show_message("Error", "There are no candidates to delete.")
            return

        names = [name for _, name in self.candidates]
        item, ok = QtWidgets.QInputDialog.getItem(self, "Delete Candidate", "Choose candidate to delete:", names, 0, False)
        if ok and item:
            for cid, name in self.candidates:
                if name == item:
                    delete_candidate(cid)
                    self.load_candidates()
                    self.show_message("Deleted", f"Candidate '{name}' has been deleted.")
                    break

    def clear_form(self):
        self.ui.IDtextbox.clear()
        for button in self.candidate_buttons:
            button.setAutoExclusive(False)
            button.setChecked(False)
            button.setAutoExclusive(True)

    def show_message(self, title, text):
        QtWidgets.QMessageBox.information(self, title, text)

if __name__ == "__main__":
    setup_db()
    app = QtWidgets.QApplication(sys.argv)
    window = VotingApp()
    window.show()
    sys.exit(app.exec())
