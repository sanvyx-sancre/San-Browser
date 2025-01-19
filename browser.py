from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

class SanBrowser(QMainWindow):
    def __init__(self):
        super(SanBrowser, self).__init__()
        self.browser = QWebEngineView()
        self.browser.load(QUrl('http://duckduckgo.com'))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        search_btn = QAction('Search', self)
        search_btn.triggered.connect(self.search)
        navbar.addAction(search_btn)

        self.url_bar = QLineEdit()
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

    def search(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))
        if url == '':
            self.browser.setUrl(QUrl('http://duckduckgo.com'))
        elif 'http' not in url:
            self.browser.setUrl(QUrl('http://' + url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())
    

execution = QApplication([])
execution.setApplicationName('San Browser')
window = SanBrowser()
window.show()
execution.exec_()
        



