from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from urllib.parse import urlparse

class SanBrowser(QMainWindow):
    def __init__(self):
        super(SanBrowser, self).__init__()
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        self.browser = QWebEngineView()
        self.browser.load(QUrl('http://duckduckgo.com'))
        self.tabs.addTab(self.browser, 'Home')

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

        self.url_bar.returnPressed.connect(self.search)

        refresh_btn = QAction('Refresh', self)
        refresh_btn.triggered.connect(self.browser.reload)
        navbar.addAction(refresh_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.home)
        navbar.addAction(home_btn)

        self.tabs.currentChanged.connect(self.change_tab)

        addtab_btn = QAction('New Tab', self)
        addtab_btn.triggered.connect(self.add_new_tab)
        navbar.addAction(addtab_btn)

    def close_current_tab(self, index):
        self.tabs.removeTab(index)

    def change_tab(self, index):
        if index >= 0:
            self.browser = self.tabs.currentWidget()

    def add_new_tab(self, qurl=None):
        if qurl is None:
            qurl = QUrl('http://duckduckgo.com')
        browser = QWebEngineView()
        browser.setUrl(QUrl("https://duckduckgo.com"))
        i = self.tabs.addTab(browser, QUrl("https://duckduckgo.com").host())
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(self.update_url)
        browser.loadFinished.connect(lambda _, i=i: self.tabs.setTabIcon(i, browser.icon()))

    def home(self):
        self.browser.setUrl(QUrl('http://duckduckgo.com'))

    def search(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))
        if url == '':
            self.browser.setUrl(QUrl('http://duckduckgo.com'))
        elif 'http' not in url:
            self.browser.setUrl(QUrl('http://' + url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())
        index = self.tabs.currentIndex()
        parsed_url = urlparse(q.toString())
        self.tabs.setTabText(index, parsed_url.netloc)


execution = QApplication([])
execution.setApplicationName('San Browser')
window = SanBrowser()
window.show()
execution.exec_()