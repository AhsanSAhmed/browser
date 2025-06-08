import sys
import os
import base64
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
    QLabel,
    QMessageBox,
    QDockWidget,
    QInputDialog,
    QTabWidget,
    QMenu,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QUrl, QSize, Qt, QPoint
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtWebEngineWidgets import QWebEngineProfile
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence



class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Get the absolute path of the script directory
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        #load custon font
        self.load_custom_font()
        
        #stack to store closed tabs
        self.closed_tabs = []  # Stack to store (url, title)
        
        #add shortcut for reopening closed tabs
        reopen_shortcut = QShortcut(QKeySequence("Ctrl+Shift+T"), self)
        reopen_shortcut.activated.connect(self.reopen_last_closed_tab)

        # Remove default window decorations (including title bar)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.set_web_engine_settings()

        # Set up the main window properties
        self.setWindowTitle("VEGVÍSIR")
        self.setGeometry(100, 100, 800, 600)

        # Custom Title Bar
        self.title_bar = QWidget(self)
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet(
            """
            background-color: #1c1c1c;
            color: #e0c097;
            font-family: "Mantinia";
            border-bottom: 2px solid #d4af37;
            """
        )

        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(5, 0, 5, 0)

        # Title label
        title_label = QLabel("VEGVÍSIR")
        title_label.setStyleSheet("color: #d4af37;")
        title_layout.addWidget(title_label)

        title_layout.addStretch()

        # Create custom minimize, maximize/restore, and close buttons
        minimize_btn = QPushButton("_")
        maximize_btn = QPushButton("☐")
        close_btn = QPushButton("❌")

        for btn in [minimize_btn, maximize_btn, close_btn]:
            btn.setFixedSize(35, 35)
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #3e2f1c;
                    color: #f5f5dc;
                    border: 2px solid #d4af37;
                    font-family: "Mantinia";
                }
                QPushButton:hover {
                    background-color: #111;
                }
                """
            )

        minimize_btn.clicked.connect(self.showMinimized)
        maximize_btn.clicked.connect(self.toggle_maximize)
        close_btn.clicked.connect(self.close)

        title_layout.addWidget(minimize_btn)
        title_layout.addWidget(maximize_btn)
        title_layout.addWidget(close_btn)
        

        # Drag functionality for the custom title bar
        self.old_position = None
        self.title_bar.mousePressEvent = self.mouse_press_event
        self.title_bar.mouseMoveEvent = self.mouse_move_event

        # Tab widget for multiple tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.update_url_bar)

        # Add "+" tab for adding new tabs
        self.add_new_tab_button()

        # Create developer tools window (QDockWidget)
        self.dev_tools_view = QWebEngineView()
        self.dev_dock = QDockWidget("Developer Tools", self)
        self.dev_dock.setWidget(self.dev_tools_view)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dev_dock)
        self.dev_dock.hide()

        # Create the navigation bar components
        self.url_bar = QLineEdit()
        self.url_bar.setFont(QFont("Mantinia", 10))
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        button_size = QSize(35, 35)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(self.script_dir, "images", "left-arrow.png")))
        back_btn.setFixedSize(button_size)
        back_btn.clicked.connect(self.browser_back)

        forward_btn = QPushButton()
        forward_btn.setIcon(QIcon(os.path.join(self.script_dir, "images", "right-arrow.png")))
        forward_btn.setFixedSize(button_size)
        forward_btn.clicked.connect(self.browser_forward)

        refresh_btn = QPushButton()
        refresh_btn.setIcon(QIcon(os.path.join(self.script_dir, "images", "refresh.png")))
        refresh_btn.setFixedSize(button_size)
        refresh_btn.clicked.connect(self.browser_refresh)

        home_btn = QPushButton()
        home_btn.setIcon(QIcon(os.path.join(self.script_dir, "images", "home.png")))
        home_btn.setFixedSize(button_size)
        home_btn.clicked.connect(self.navigate_home)

        bookmark_btn = QPushButton()
        bookmark_btn.setIcon(
            QIcon(os.path.join(self.script_dir, "images", "bookmark.png"))
        )
        bookmark_btn.setFixedSize(button_size)
        bookmark_btn.clicked.connect(self.add_bookmark)

        inspect_btn = QPushButton()
        inspect_btn.setIcon(
            QIcon(os.path.join(self.script_dir, "images", "binoculars.png"))
        )
        inspect_btn.setFixedSize(button_size)
        inspect_btn.clicked.connect(self.toggle_dev_tools)

        self.bookmark_bar_layout = QHBoxLayout()
        self.bookmark_bar_layout.setContentsMargins(5, 0, 5, 0)
        self.bookmark_bar_layout.setSpacing(5)

        bookmark_bar_widget = QWidget()
        bookmark_bar_widget.setLayout(self.bookmark_bar_layout)
        bookmark_bar_widget.setFixedHeight(35)  # Very thin bookmark bar

        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(5, 5, 5, 5)
        nav_layout.setSpacing(5)

        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(forward_btn)
        nav_layout.addWidget(refresh_btn)
        nav_layout.addWidget(home_btn)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(bookmark_btn)
        nav_layout.addWidget(inspect_btn)

        nav_widget = QWidget()
        nav_widget.setLayout(nav_layout)
        nav_widget.setFixedHeight(70)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.title_bar)

        main_layout.addWidget(nav_widget)
        main_layout.addWidget(bookmark_bar_widget)
        main_layout.addWidget(self.tab_widget)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        self.bookmarks = []

        self.setStyleSheet(
            """
        QWidget {
            font-family: "Mantinia";
            background-color: #1c1c1c; 
            color: #e0c097;  
        }

        QPushButton {
            background-color: #e0c097;
            border: 2px solid #d4af37;  
            color: #f5f5dc;
            border-radius: 5px;
            padding: 0px;  /* Adjust padding */
        }
        QPushButton:hover {
                    background-color: #5a422b;
                }

        QLineEdit {
            background-color: #2e2b26;
            border: 2px solid #d4af37;
            color: #e0c097;
            height: 35px;  /* Fixed height */
        }

         QTabWidget::pane { border: 2px solid #d4af37; }
            QTabWidget::tab-bar { left: 10px; }

            QTabBar::tab {
                background-color: #1e1a16;
                color: #e0c097;
                padding: 10px;
                margin-right: 5px;  /* Space between tabs */
                border-right: 1px solid #d4af37;
            }

            QTabBar::tab:selected { background-color: #2c241b; }
            QTabBar::tab:last { border-right: none; }  /* Remove right border from the last tab */

        """
        )

        # Open the initial tab with the home page
        self.add_new_tab(QUrl("https://www.google.com"), "Home")

    def set_web_engine_settings(self):
        profile = QWebEngineProfile.defaultProfile()
        profile.setRequestInterceptor(None)

        # Disable GPU acceleration
        profile.setPersistentStoragePath(os.path.join(self.script_dir, "webengine"))
        profile.setCachePath(os.path.join(self.script_dir, "webengine_cache"))
        profile.setPersistentStoragePath(
            os.path.join(self.script_dir, "webengine_persistent")
        )

        # Set other WebEngine settings
        QWebEngineSettings.globalSettings().setAttribute(
            QWebEngineSettings.AutoLoadImages, True
        )
        QWebEngineSettings.globalSettings().setAttribute(
            QWebEngineSettings.JavascriptEnabled, True
        )
        QWebEngineSettings.globalSettings().setAttribute(
            QWebEngineSettings.LocalStorageEnabled, True
        )
        QWebEngineSettings.globalSettings().setAttribute(
            QWebEngineSettings.WebRTCPublicInterfacesOnly, False
        )

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl("https://www.google.com")

        browser = QWebEngineView()
        browser.setUrl(qurl)

        # Set up developer tools for the browser
        browser.page().setDevToolsPage(self.dev_tools_view.page())

        # Update the tab label when the URL changes
        browser.titleChanged.connect(
            lambda title: self.tab_widget.setTabText(
                self.tab_widget.currentIndex(), title if title else "Untitled"
            )
        )

        browser.urlChanged.connect(lambda q: self.update_url_bar())
        browser.loadFinished.connect(lambda success: self.apply_fantasy_style(browser))

        index = self.tab_widget.insertTab(self.tab_widget.count() - 1, browser, label)
        self.tab_widget.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            widget = self.tab_widget.widget(index)
            if isinstance(widget, QWebEngineView):
                url = widget.url().toString()
                title = self.tab_widget.tabText(index)
                self.closed_tabs.append((url, title))
            self.tab_widget.removeTab(index)
        else:
            self.close()
            
    def reopen_last_closed_tab(self):
        if self.closed_tabs:
            url, title = self.closed_tabs.pop()
            self.add_new_tab(QUrl(url), title)


    def apply_fantasy_style(self, browser):
        font_path = os.path.join(self.script_dir, "fonts", "Mantinia.ttf")
        with open(font_path, "rb") as font_file:
            base64_font = base64.b64encode(font_file.read()).decode("utf-8")
    
        css = f"""
        @font-face {{
            font-family: 'Mantinia';
            src: url(data:font/ttf;base64,{base64_font}) format('truetype');
        }}
        * {{
            font-family: 'Mantinia', serif !important;
            font-size: 20px;
        }}
        """
    
        browser.page().runJavaScript(
            f"""
            (function() {{
                var style = document.createElement('style');
                style.type = 'text/css';
                style.innerHTML = `{css}`;
                document.head.appendChild(style);
            }})();
            """
        )

    def toggle_dev_tools(self):
        if self.dev_dock.isVisible():
            self.dev_dock.hide()
        else:
            self.dev_dock.show()

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.tab_widget.currentWidget().setUrl(QUrl(url))

    def navigate_home(self):
        self.tab_widget.currentWidget().setUrl(QUrl("https://www.google.com"))

    def update_url_bar(self):
        current_browser = self.tab_widget.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            self.url_bar.setText(current_browser.url().toString())

    def browser_back(self):
        current_browser = self.tab_widget.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.back()

    def browser_forward(self):
        current_browser = self.tab_widget.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.forward()

    def browser_refresh(self):
        current_browser = self.tab_widget.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.reload()

    def add_new_tab_button(self):
        new_tab_btn = QPushButton("+")
        new_tab_btn.setFixedSize(35, 35)
        # Adjust the button's position by adding a top margin
        new_tab_btn.setStyleSheet(
            "margin-top: 5px; margin-bottom: 9px;"
        )  # Negative top margin to move it up
        new_tab_btn.clicked.connect(lambda: self.add_new_tab())
        self.tab_widget.setCornerWidget(new_tab_btn, Qt.TopLeftCorner)

    def add_bookmark(self):
        current_browser = self.tab_widget.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            url = current_browser.url().toString()

            # Create a custom input dialog for bookmark title
            dialog = QInputDialog(self)
            dialog.setWindowFlags(
                Qt.FramelessWindowHint | Qt.Popup
            )  # Remove title bar, make it popup
            dialog.setInputMode(QInputDialog.TextInput)
            dialog.setLabelText("Enter bookmark title:")
            dialog.setCancelButtonText("Cancel")
            dialog.resize(350, 150)  # Optional: Resize the dialog if needed

            # Show the dialog and wait for the user input
            if dialog.exec_() == QInputDialog.Accepted:
                bookmark_title = dialog.textValue()
                if bookmark_title:  # If the user entered a title
                    bookmark_btn = QPushButton(bookmark_title)
                    bookmark_btn.setStyleSheet(
                        """
                        QPushButton {
                            background-color: #3e2f1c;
                            color: #f5f5dc;
                            border: 2px solid #d4af37;
                            font-family: "Mantinia";
                        }
                        QPushButton:hover {
                            background-color: #5a422b;
                        }
                        """
                    )
                    bookmark_btn.clicked.connect(
                        lambda checked=False, url=url, title=bookmark_title: self.add_new_tab(QUrl(url), title)
                    )


                    # Context menu for deleting bookmarks
                    bookmark_btn.setContextMenuPolicy(Qt.CustomContextMenu)
                    bookmark_btn.customContextMenuRequested.connect(
                        lambda pos, btn=bookmark_btn: self.show_bookmark_menu(pos, btn)
                    )

                    # Add the bookmark button to the bookmark bar
                    self.bookmark_bar_layout.addWidget(bookmark_btn)
                    self.bookmarks.append((bookmark_title, url, bookmark_btn))


    def show_bookmark_menu(self, pos, bookmark_btn):
        menu = QMenu(self)
        delete_action = menu.addAction("Delete Bookmark")

        action = menu.exec_(bookmark_btn.mapToGlobal(pos))

        if action == delete_action:
            # Remove the button from the layout
            bookmark_btn.setParent(None)
            bookmark_btn.deleteLater()

            # Remove the bookmark from the list
            self.bookmarks = [b for b in self.bookmarks if b[2] != bookmark_btn]

    def mouse_press_event(self, event):
        self.old_position = event.globalPos()

    def mouse_move_event(self, event):
        delta = QPoint(event.globalPos() - self.old_position)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_position = event.globalPos()

    def load_custom_font(self):
        font_path = os.path.join(self.script_dir, "fonts", "Mantinia.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print("Failed to load Mantinia font.")
        else:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            print(f"Mantinia font loaded: {family}")
            app_font = QFont(family)
            QApplication.setFont(app_font)  # Apply it globally




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("VEGVÍSIR Browser")
    window = Browser()
    window.show()
    sys.exit(app.exec_())