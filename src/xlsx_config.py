"""Configuration constants for generating Excel spreadsheets.
These constants are inter-dependent:  Number of rows and columns
must be compatible with cell dimensions, so that the sheets
paginate correctly.
"""

COLS = 2
ROWS_PER_PAGE = 5
CARDS_PER_PAGE = COLS * ROWS_PER_PAGE  # Counts fronts only
# A spread is a pair of pages, front and back
# A spread has the same number of CARDS as a page,
# but twice as many rows
ROWS_PER_SPREAD = 2 * ROWS_PER_PAGE

# Experimentally derived to fit 5 x 2 per page.
# You'll have to play with these if you change layout.
# I don't even know what the unit is.
ROW_HEIGHT = 140
COL_WIDTH = 40


XLSX_FRONT_FORMAT = {
    'font_size': 40,
    'valign': 'top',
    'align': 'center',
    'text_wrap': True,
    }

XLSX_BACK_FORMAT = {
    'font_size': 14,
    'valign': 'vcenter',
    'align': 'center',
    'text_wrap': True,
}
