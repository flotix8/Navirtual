import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.browser = QWebEngineView()
        self.search_engine_url = 'https://www.google.com/search?q={}'
        self.setCentralWidget(self.browser)

        navbar = QToolBar()
        self.addToolBar(navbar)

        # Créer la barre de titre avec les onglets
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        # Ajouter un bouton pour ajouter un nouvel onglet
        add_tab_button = QPushButton("Nouvel onglet")
        add_tab_button.clicked.connect(self.add_new_tab)
        self.tab_widget.setCornerWidget(add_tab_button)

        # Ajouter un onglet initial
        self.add_new_tab()

        self.show()


        # Ajouter un bouton avec une icône personnalisée
        back_button = QPushButton('', self)
        back_button.setFixedSize(25, 25)
        back_button.setIconSize(back_button.size())
        back_icon = QIcon()
        back_icon.addPixmap(QPixmap('left_arrow.png').scaledToWidth(25, Qt.SmoothTransformation))
        back_button.setIcon(back_icon)
        back_button.setToolTip('Back')
        back_button.setObjectName('backButton')
        back_button.clicked.connect(self.browser.back)
        navbar.addWidget(back_button)

        forward_button = QPushButton('', self)
        forward_button.setFixedSize(25, 25)
        forward_button.setIconSize(forward_button.size())
        forward_icon = QIcon()
        forward_icon.addPixmap(QPixmap('right_arrow.png').scaledToWidth(25, Qt.SmoothTransformation))
        forward_button.setIcon(forward_icon)
        forward_button.setToolTip('Forward')
        forward_button.setObjectName('forwardButton')
        forward_button.clicked.connect(self.browser.forward)
        navbar.addWidget(forward_button)

        reload_button = QPushButton('', self)
        reload_button.setFixedSize(25, 25)
        reload_button.setIconSize(forward_button.size())
        reload_icon = QIcon()
        reload_icon.addPixmap(QPixmap('spinning_arrow.png').scaledToWidth(25, Qt.SmoothTransformation))
        reload_button.setIcon(reload_icon)
        reload_button.setToolTip('Reload')
        reload_button.setObjectName('reloadButton')
        reload_button.clicked.connect(self.browser.reload)
        navbar.addWidget(reload_button)

        home_button = QPushButton('', self)
        home_button.setFixedSize(25, 25)
        home_button.setIconSize(forward_button.size())
        home_icon = QIcon()
        home_icon.addPixmap(QPixmap('home.png').scaledToWidth(25, Qt.SmoothTransformation))
        home_button.setIcon(home_icon)
        home_button.setToolTip('Home')
        home_button.setObjectName('homeButton')
        home_button.clicked.connect(self.navigate_home)
        navbar.addWidget(home_button)

        # Ajouter une liste déroulante pour choisir le moteur de recherche
        self.search_engine_combo = QComboBox(self)
        self.search_engine_combo.addItems(['Google', 'Bing', 'Yahoo', 'Duckduckgo', 'Ecosia', 'Qwant', 'Lilo'])
        self.search_engine_combo.setObjectName('search_engine')
        self.search_engine_combo.setStyleSheet("width: 45px;")
        self.search_engine_combo.setCurrentIndex(0)
        self.search_engine_combo.activated[str].connect(self.change_search_engine)
        navbar.addWidget(self.search_engine_combo)

        self.setCentralWidget(self.browser)
        self.show()

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_search)
        self.url_bar.mousePressEvent = self.select_all
        navbar.addWidget(self.url_bar)
        self.browser.urlChanged.connect(self.update_url_bar)

        menu_button = QPushButton('', self)
        menu_button.setFixedSize(25, 25)
        menu_button.setIconSize(forward_button.size())
        menu_icon = QIcon()
        menu_icon.addPixmap(QPixmap('menu.png').scaledToWidth(25, Qt.SmoothTransformation))
        menu_button.setIcon(menu_icon)
        menu_button.setToolTip('Menu')
        menu_button.setObjectName('menuButton')
        menu_button.clicked.connect(self.show_menu_dialog)
        navbar.addWidget(menu_button)

        style_sheet = """
            QWidget {
                background-color: #1a1a1a;
                border-radius: 5px;
                color: #d9d9d9;
                height: 21px;
            }

            QLineEdit {
                border-radius: 5px;
                background-color: #1a1a1a;
                color: #d9d9d9;
                height: 35px;
                font-size: 14px;
                ont-family: system-ui;
            }
            QLineEdit:hover {
                background-color: #4d4d4d;
            }
            
            QPushButton:hover {
                background-color: #4d4d4d; 
            }
            QComboBox#search_engine:hover {
                background-color: #4d4d4d;
            }
         """
        self.setStyleSheet(style_sheet)

    def show_menu_dialog(self):
        # Créer un widget de liste pour représenter le menu
        menu_widget = QListWidget()
        menu_widget.addItems(['Option 1', 'Option 2', 'Option 3'])

        # Créer un QDockWidget pour afficher le menu
        menu_dock = QDockWidget("Menu", self)
        menu_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        menu_dock.setWidget(menu_widget)

        # Style
        menu_dock.setFixedWidth(350)
        menu_widget.setStyleSheet("background-color: #1a1a1a;")

        self.addDockWidget(Qt.RightDockWidgetArea, menu_dock)

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def change_search_engine(self, engine_name):
        if engine_name == 'Google':
            self.browser.setUrl(QUrl("https://www.google.com/"))
            self.search_engine_url = 'https://www.google.com/search?q={}'
        elif engine_name == 'Bing':
            self.browser.setUrl(QUrl("https://www.bing.com/"))
            self.search_engine_url = 'https://www.bing.com/search?q={}'
        elif engine_name == 'Yahoo':
            self.browser.setUrl(QUrl("https://search.yahoo.com/"))
            self.search_engine_url = 'https://search.yahoo.com/search?p={}'
        elif engine_name == 'Duckduckgo':
            self.browser.setUrl(QUrl("https://duckduckgo.com/"))
            self.search_engine_url = 'https://duckduckgo.com/?q={}'
        elif engine_name == 'Ecosia':
            self.browser.setUrl(QUrl("https://www.ecosia.org/"))
            self.search_engine_url = 'https://www.ecosia.org/search?method=index&q={}'
        elif engine_name == 'Qwant':
            self.browser.setUrl(QUrl("https://www.qwant.com/"))
            self.search_engine_url = 'https://www.qwant.com/?q={}'
        elif engine_name == 'Lilo':
            self.browser.setUrl(QUrl("https://www.lilo.org/"))
            self.search_engine_url = 'https://search.lilo.org/?q={}'
        else:
            self.browser.setUrl(QUrl("https://www.google.com/"))
            self.search_engine_url = 'https://www.google.com/search?q={}'

    def select_all(self, event):
        if isinstance(event, QMouseEvent) and event.button() == Qt.LeftButton:
            self.url_bar.selectAll()

    def navigate_to_search(self):
        # Naviguer vers la recherche en utilisant l'URL du moteur de recherche courant et la requête de recherche
        search_query = self.url_bar.text()
        url = self.search_engine_url.format(search_query)
        self.browser.load(QUrl(url))

    def add_new_tab(self):
        # Créer un nouvel onglet et l'ajouter à la barre de titre
        new_tab = QWidget()
        self.tab_widget.addTab(new_tab, "Nouvel onglet")

        # Ajouter une disposition pour les éléments dans l'onglet
        layout = QVBoxLayout()
        new_tab.setLayout(layout)

    def close_tab(self, index):
        # Fermer l'onglet spécifié par l'index
        self.tab_widget.removeTab(index)

    def load_url(self, url):
        # Charger l'URL spécifiée dans le navigateur
        print("Chargement de l'URL:", url)

app = QApplication(sys.argv)
window = MainWindow()
window.setWindowTitle('navigateur')
window.showMaximized()
sys.exit(app.exec_())

