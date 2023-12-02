# overlay-pdf
# Python script. Feed it a .pdf invoice document and brand it with a "PAID: [date stamp]" and a "thank you". Used for converting invoices into receipts when a customer pays.

(Running Ubuntu 22.04). I place the the main `.py` script at `~/.local/bin/overlay_pdf/overlay_pdf.py`. My stack of invoices live in `~/Documents/Pending invoices/`. (this path is hard coded in the script which you can adjust as necessary.

Without arguments, the script will look for the most-recently modified pdf file at the path above, brand it with a "PAID" + current date stamp angled green text, as per the screencap below, and save to `~/Documents/Pending invoices/Sent Receipts` with an 'R' appended to the filename. Adjust paths/naming behaviour as needed.

Optional parameters are `input`, `output`, and `date`, which will override default behaviour and specifiy input filepath, output filepath, and date, respectively.

You can also add the contents of the `.bashrc` file to your own .bashrc file afterwhich you can simply run `makereceipt` to run the script, with or without paramters.

e.g. `makereceipt --date=02.12.23`

![Screenshot](screenshot.png)
