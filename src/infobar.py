"""
Anki Add-on "Card Info Bar for Browser"

Copyright (c):
- 2019 ijgnd
- 2017 Luminous Spice ("Infobar: another toolbar for Anki 2.1 beta")
       https://github.com/luminousspice/anki-addons/
       https://ankiweb.net/shared/info/1955978390
- hssm
- Ankitects Pty Ltd and contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from aqt import mw
from aqt.qt import *
from PyQt5 import QtWidgets, QtCore
from aqt.forms.browser import Ui_Dialog
from aqt.browser import Browser
from anki.sched import Scheduler
from anki.utils import ids2str, intTime, fmtTimeSpan
from anki.hooks import addHook, wrap

from .card_properties import cardstats


def gc(arg,fail=False):
    return mw.addonManager.getConfig(__name__).get(arg,fail)


def addInfoBar(self):
    a = ["added","fr","lr","due","ivl","ease","revs","laps","avTime",
            "cardType","noteType","Deck", "nid", "cid"] 
    for i in a:
        setattr(self,"il_" + i,QtWidgets.QLabel(self))
        setattr(self,"i_" + i,QtWidgets.QLabel(self))

    g = [
        #      0                1           2  3  4  5      6            7   8  9 10 11
        [self.il_added,    'Added:     ',   0, 0, 1, 1, self.i_added,    "", 0, 1, 1, 1],
        [self.il_fr,       'FirstRev:  ',   1, 0, 1, 1, self.i_fr,       "", 1, 1, 1, 1],
        [self.il_lr,       'LatestRev: ',   2, 0, 1, 1, self.i_lr,       "", 2, 1, 1, 1],
        [self.il_due,      'Due:  ',        0, 2, 1, 1, self.i_due,      "", 0, 3, 1, 1],
        [self.il_ivl,      'Ivl:  ',        1, 2, 1, 1, self.i_ivl,      "", 1, 3, 1, 1],
        [self.il_ease,     'Ease: ',        2, 2, 1, 1, self.i_ease,     "", 2, 3, 1, 1],
        [self.il_revs,     'Rvs/Lps: ',     0, 4, 1, 1, self.i_revs,     "", 0, 5, 1, 1],
        [self.il_nid,      'Note ID: ',     1, 4, 1, 1, self.i_nid ,     "", 1, 5, 1, 1],
        [self.il_cid,      'Card ID: ',     2, 4, 1, 1, self.i_cid,      "", 2, 5, 1, 1],
        [self.il_cardType, 'Card Type: ',   0, 6, 1, 1, self.i_cardType, "", 0, 7, 1, 1],
        [self.il_noteType, 'Note Type: ',   1, 6, 1, 1, self.i_noteType, "", 1, 7, 1, 2],
        [self.il_Deck,     'Deck:      ',   2, 6, 1, 1, self.i_Deck,     "", 2, 7, 1, 2],
        [self.il_avTime,   'AvgTime: ',     0, 8, 1, 1, self.i_avTime,   "", 0, 9, 1, 1],
    ]

    for l in g:
        t = "<b>" + l[1] + "</b>"  # increaes height noticeable
        l[0].setText(t) 
        #l[0].setStyleSheet('background-color: rgb(100, 10, 1);')
        l[6].setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.form.infogrid.addWidget(l[0], l[2], l[3], l[4], l[5])
        self.form.infogrid.addWidget(l[6], l[8], l[9], l[10], l[11])
    
    self.form.infogrid.setColumnStretch(0,1)
    self.form.infogrid.setColumnStretch(1,2)
    self.form.infogrid.setColumnStretch(2,1)
    self.form.infogrid.setColumnStretch(3,2)
    self.form.infogrid.setColumnStretch(4,1)
    self.form.infogrid.setColumnStretch(5,2)
    self.form.infogrid.setColumnStretch(6,1)
    self.form.infogrid.setColumnStretch(7,4)
    self.form.infogrid.setColumnStretch(8,1)
    self.form.infogrid.setColumnStretch(9,2)


def update(self):
    if self.card:
        p = self.cardstats(self.card)
        self.i_added.setText(p.Added) 
        self.i_fr.setText(p.FirstReview) 
        self.i_lr.setText(p.LatestReview)
        self.i_due.setText(p.Due)
        self.i_ivl.setText(p.Interval)
        self.i_ease.setText(p.Ease)
        self.i_revs.setText(p.Reviews + "/ " + p.Lapses)
        self.i_avTime.setText(p.AverageTime)
        self.i_cardType.setText(p.CardType)
        self.i_noteType.setText(p.NoteType)
        self.i_Deck.setText(p.Deck)
        self.i_nid.setText(p.NoteID)
        self.i_cid.setText(p.CardID)
            

def setupUi(self, Dialog):
    self.verticalLayout_2.removeWidget(self.tableView)
    self.infogrid = QtWidgets.QGridLayout()
    self.infowidget = QtWidgets.QWidget()
    self.infowidget.setLayout(self.infogrid)
    if not gc("enable by default"):
        self.infowidget.setVisible(False)
    self.verticalLayout_2.addWidget(self.infowidget)    
    self.verticalLayout_2.addWidget(self.tableView)


Ui_Dialog.setupUi = wrap(Ui_Dialog.setupUi, setupUi)
addHook("browser.setupMenus", addInfoBar)
addHook("browser.rowChanged", update)
Browser.cardstats = cardstats



def toggle_infobox(self):
    if not self.form.infowidget.isVisible():
        self.form.infowidget.setVisible(True)
    else:
        self.form.infowidget.setVisible(False)
Browser.toggle_infobox = toggle_infobox


def onSetupMenus(self):
    try:
        m = self.menuView
    except:
        self.menuView = QMenu(_("&View"))
        action = self.menuBar().insertMenu(
            self.mw.form.menuTools.menuAction(), self.menuView)
        m = self.menuView

    # a = m.addAction('toggle infobox')
    # a.triggered.connect(self.toggle_infobox)
    a = m.addAction('show infobox')
    a.setCheckable(True)
    a.setChecked(gc("enable by default"))
    a.toggled.connect(self.toggle_infobox) 
    cut = gc("show_infobox")
    if cut:
        a.setShortcut(QKeySequence(cut))
addHook("browser.setupMenus", onSetupMenus)


