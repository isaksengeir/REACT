from PyQt5.QtWidgets import QListWidget


class DragDropListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setDragDropMode(self.InternalMove)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            super(DragDropListWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(DragDropListWidget, self).dragMoveEvent(event)
        event.accept()
        #if event.mimeData().hasUrls():
        #    event.setDropAction(Qt.CopyAction)
        #    event.accept()
        #else:
        #    print("Ignoring dragMovementEvent")
        #    event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            files_accept = ["out", "pdb", "com", "xyz", "inp"]
            links_ = []
            for url in event.mimeData().urls():
                # https://doc.qt.io/qt-5/qurl.html
                if str(url.toLocalFile()).split("/")[-1].split(".")[-1] in files_accept:
                    links_.append(str(url.toLocalFile()))

            #TODO should we add the entire path to project table? If not, this must communicate back path to dict() somehow
            self.addItems(links_)

        else:
            super(DragDropListWidget, self).dropEvent(event)
            event.accept()

