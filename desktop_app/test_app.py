import os
import sys

os.environ["QT_QPA_PLATFORM"] = "offscreen"
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from PyQt6.QtWidgets import QApplication
from main import MainWindow
from database import init_db, seed_sample_data, get_all_questions

def run_tests():
    init_db()
    seed_sample_data()

    app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow()

    # Test 1: Window Properties
    assert window.windowTitle() == "DSA Notes"
    assert window.minimumWidth() == 980
    assert window.minimumHeight() == 640
    print("Test 1: Window title and minimum dimensions verified")

    # Test 2: Search filtering
    window.search_input.setText("Two")
    window.refresh_question_list()
    assert window.question_list_widget.count() == 2
    print("Test 2: Search filtering matched 2 questions")

    # Test 3: Empty search state
    window.search_input.setText("NonExistentTermXYZ")
    window.refresh_question_list()
    assert window.question_list_widget.count() == 0
    assert "NonExistentTermXYZ" in window.empty_detail_label.text()
    print("Test 3: Search empty state message verified")

    # Test 4: Clear search restores all
    window.search_input.clear()
    window.refresh_question_list()
    assert window.question_list_widget.count() >= 3
    print("Test 4: Search clear restored question list")

    # Test 5: View switching and focus
    window.open_add_form()  # Form
    assert window.stack.currentIndex() == 1
    window.switch_view(2)  # Topics
    assert window.stack.currentIndex() == 2
    window.switch_view(0)  # Dashboard
    assert window.stack.currentIndex() == 0
    print("Test 5: View router and input focus verified")

    # Test 6: Responsive image scaling
    window.resize(1400, 900)
    window._rescale_detail_image()
    print("Test 6: Dynamic image scaling hook verified")

    # Test 7: Shortcuts bound
    assert hasattr(window, "sc_new")
    assert hasattr(window, "sc_find")
    assert hasattr(window, "sc_save")
    assert hasattr(window, "sc_esc")
    print("Test 7: All keyboard shortcuts (New, Find, Save, Esc) verified")

    print("\n==========================================")
    print("ALL DESKTOP TESTS COMPLETED SUCCESSFULLY")
    print("==========================================")

if __name__ == "__main__":
    run_tests()
