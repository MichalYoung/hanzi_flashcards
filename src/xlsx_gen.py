"""Generate flashcards in Excel format"""

"""Early experiments: Try hard-coding a few cells."""

"""Note: "leaf" is the term for a front/back pair of pages.
If we count leaves and pages from zero, then we get
leaf    pages
0       0, 1
1       2, 3
2       4, 5

i.e., a card that is front and back of leaf n is on pages 2n, 2n+1.


"""

import xlsxwriter
import pleco_reader
import xlsx_config


def ceil_div(a: int, b: int) -> int:
    """Division with rounding up, i.e., a//b when a % mod b == 0, otherwise a//b + 1"""
    return -(a//-b) # Works because Python rounds down rather than toward zero


def make_sheet(path: str, n_cells: int) -> tuple[xlsxwriter.Workbook, xlsxwriter.worksheet]:
    """Returns a workbook with one worksheet with properly dimensioned cells
    """
    workbook = xlsxwriter.Workbook('../out/sample.xlsx')
    worksheet = workbook.add_worksheet()

    # Set up cell templates
    worksheet.set_column(0, xlsx_config.COLS - 1, xlsx_config.COL_WIDTH)
    spreads = ceil_div(n_cells, xlsx_config.CARDS_PER_PAGE)
    for side in range(2 * spreads):
        for side_row in range(xlsx_config.ROWS_PER_PAGE):
            row = side * xlsx_config.ROWS_PER_PAGE + side_row
            worksheet.set_row(row, xlsx_config.ROW_HEIGHT)
    # This should be simpler --- number of rows is ceil(cards / columns)

    return workbook, worksheet


def main():
    subject = open("../data/duolingo.txt", "r", encoding="utf-8")
    reader = pleco_reader.Reader(subject)
    workbook, worksheet = make_sheet('../out/sample.xlsx', reader.count)
    front_format = workbook.add_format(xlsx_config.XLSX_FRONT_FORMAT)
    front_format.set_align('vcenter')  # Should not be necessary
    front_format.set_border(5)   # continuous weight 3
    back_format = workbook.add_format(xlsx_config.XLSX_BACK_FORMAT)
    back_format.set_align('top')  # Should not be necessary
    back_format.set_border(5)


    for entry_num, entry in enumerate(reader.entries):
        characters, pinyin, defn = entry
        # First row of the spread in which the card will be placed
        front_spread = (entry_num // xlsx_config.CARDS_PER_PAGE)
        base_row = front_spread * xlsx_config.ROWS_PER_SPREAD
        # Where within each page of the spread?
        card_within_page = entry_num % xlsx_config.CARDS_PER_PAGE
        row_within_page = card_within_page // xlsx_config.COLS
        # The actual rows
        row_front = base_row + row_within_page
        row_back = row_front + xlsx_config.ROWS_PER_PAGE
        # Columns
        col_front = entry_num % xlsx_config.COLS
        col_back = (xlsx_config.COLS - 1) - col_front

        worksheet.write(row_front, col_front, characters ,front_format)
        worksheet.write(row_back, col_back, pinyin + "\n\n" + defn, back_format)
    # Add a format to use wrap the cell text.
    workbook.close()

if __name__ == '__main__':
    main()