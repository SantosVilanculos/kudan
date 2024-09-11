from PySide6.QtCore import QFile, QTextStream, QUrl
from PySide6.QtGui import QDesktopServices, QTextDocument
from PySide6.QtWidgets import QTextBrowser

from env import contents_directory_path


class License(QTextBrowser):
    def __init__(self) -> None:
        super().__init__()

        self.setOpenLinks(False)
        self.setOpenExternalLinks(False)
        self.anchorClicked.connect(self.anchor_clicked)

        PATH = contents_directory_path()

        q_text_document = QTextDocument()
        q_file = QFile(str(PATH.joinpath("LICENSE")))
        if q_file.open(QFile.ReadOnly | QFile.Text):
            q_text_stream = QTextStream(q_file)
            q_text_document.setPlainText(q_text_stream.readAll())
            q_file.close()
        else:
            q_text_document.setHtml(
                '<p>The MIT License: <a href="https:/opensource.org/license/mit/">https://opensource.org/license/mit</a></p>'
            )
        self.setDocument(q_text_document)

    def anchor_clicked(self, q_url: QUrl):
        QDesktopServices.openUrl(q_url)
