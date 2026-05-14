import sys
import os
import mimetypes
from configparser import ConfigParser
from PySide6.QtWidgets import (QApplication, QTextEdit, QWidget, QSizePolicy, QVBoxLayout, QFileIconProvider, QPushButton)
from PySide6.QtCore import Qt, QSize, QUrl, QEvent, QMimeDatabase
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QTextCursor, QDesktopServices, QPixmap, QIcon, QTextDocument, QTextCharFormat, QTextImageFormat
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class StickyNoteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Sticky Note")
        self.resize(220, 200)
        self.setAcceptDrops(True) 
        self.initUI()
        self.icon_provider = QFileIconProvider()
        self.mime_db = QMimeDatabase()
        self.pressed_anchor = None
        self.audio_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.audio_player.setAudioOutput(self.audio_output)
        
        icon_path = "/home/emersonberry/apps/stickynotes/stickynotes.png"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Warning: Icon file not found at {icon_path}")

    def initUI(self):
        app_layout = QVBoxLayout()
        app_layout.setContentsMargins(0, 0, 0, 0)
        app_layout.setSpacing(0)
        self.combined_area = QTextEdit(self)
        self.combined_area.setPlaceholderText("Type Words Here")
        self.combined_area.setStyleSheet("background-color: #FFFFa0; border: none; padding: 10px;")
        self.combined_area.setAcceptDrops(False)
        self.combined_area.setTextInteractionFlags(Qt.TextBrowserInteraction | Qt.TextEditorInteraction | Qt.LinksAccessibleByMouse)
        self.combined_area.viewport().installEventFilter(self)
        app_layout.addWidget(self.combined_area)
        self.setLayout(app_layout)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def eventFilter(self, source, event):
        if source is self.combined_area.viewport():
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self.pressed_anchor = self.combined_area.anchorAt(event.pos())
                return False
            if event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
                released_anchor = self.combined_area.anchorAt(event.pos())
                if self.pressed_anchor and self.pressed_anchor == released_anchor:
                    self.handleAnchorClick(self.pressed_anchor)
                    self.pressed_anchor = None
                return True
            self.pressed_anchor = None
            if event.type() == QEvent.MouseMove:
                if self.combined_area.anchorAt(event.pos()):
                    QApplication.setOverrideCursor(Qt.PointingHandCursor)
                else:
                    QApplication.restoreOverrideCursor()
            return super().eventFilter(source, event)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Accepts drag events if *any* file is an image or desktop file."""
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    mime_type, _ = mimetypes.guess_type(file_path)
                    is_image = mime_type and (mime_type.startswith('image/') or mime_type == 'image/svg+xml')
                    is_desktop = file_path.endswith('.desktop')

                    if is_image or is_desktop:
                        event.acceptProposedAction()
                        return

        event.ignore()

    def dropEvent(self, event: QDropEvent):
        """Processes dropped image and desktop files."""
        if event.mimeData().hasUrls():
            cursor = self.combined_area.textCursor()
            cursor.movePosition(QTextCursor.End)
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if os.path.exists(file_path):
                    mime_type, _ = mimetypes.guess_type(file_path)
                    is_image = mime_type and (mime_type.startswith('image/') or mime_type == 'image/svg+xml')
                    is_desktop = file_path.endswith('.desktop')

                    if is_image or is_desktop:
                        # Ensure a new line or block is inserted cleanly between items
                        # --- FIXED LINE HERE ---
                        if cursor.position() != 0 and not cursor.block().text().strip(): 
                        # -----------------------
                            cursor.insertBlock()
                        self.insertFileOrImage(file_path, cursor)
            event.acceptProposedAction()
        else:
            event.ignore()

    def insertFileOrImage(self, path, cursor):
        mime_type, _ = mimetypes.guess_type(path) if mimetypes.guess_type(path) else (None, None)

        if mime_type and (mime_type.startswith('image/') or mime_type == 'image/svg+xml'):
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(QSize(32, 32), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.insertInlineImage(scaled_pixmap, path, cursor)
            else:
                self.insertFileIcon(path, cursor)
        elif path.endswith('.desktop'):
            icon_path = self.get_desktop_icon_path(path)
            if icon_path:
                icon_pixmap = QIcon(icon_path).pixmap(QSize(32, 32))
                self.insertInlineImage(icon_pixmap, path, cursor)
            else:
                self.insertFileIcon(path, cursor)

    def insertFileIcon(self, path, cursor):
        icon = self.icon_provider.icon(QFileIconProvider.File)
        pixmap = icon.pixmap(QSize(32, 32))
        self.insertInlineImage(pixmap, path, cursor)

    def insertInlineImage(self, pixmap, path, cursor):
        document = self.combined_area.document()
        image_url = QUrl(f"resource://{os.path.basename(path)}")
        document.addResource(QTextDocument.ImageResource, image_url, pixmap)

        image_format = QTextImageFormat()
        image_format.setName(image_url.toString())
        image_format.setToolTip(f"Click to open:\n{os.path.basename(path)}")
        image_format.setAnchorHref(path)

        cursor.insertImage(image_format)
        
        text_to_insert = os.path.basename(path)
        cursor.insertText(f" {text_to_insert}\n")
    
    def get_desktop_icon_path(self, desktop_file_path):
        config = ConfigParser()
        config.read(desktop_file_path)
        if 'Desktop Entry' in config and 'Icon' in config['Desktop Entry']:
            icon_name = config['Desktop Entry']['Icon']
            for size in ['128x128', '64x64', '48x48', '32x32', '24x24', '16x16']:
                icon_path = os.path.join('/usr/share/icons/hicolor', size, 'apps', icon_name + '.png')
                if os.path.exists(icon_path):
                    return icon_path
            for size in ['128x128', '64x64', '48x48', '32x32', '24x24', '16x16']:
                icon_path = os.path.join('/usr/share/icons/gnome', size, 'apps', icon_name + '.png')
                if os.path.exists(icon_path):
                    return icon_path
            return icon_name
        return None

    def handleAnchorClick(self, anchor_url):
        url = QUrl(anchor_url)
        if url.scheme() == 'audio':
            self.play_audio(url.path()) 
        else:
            self.openFileFromAnchor(url)

    def openFileFromAnchor(self, url):
        QDesktopServices.openUrl(url)
        QApplication.restoreOverrideCursor()

    def play_audio(self, path):
        url = QUrl.fromLocalFile(path)
        if self.audio_player.source() == url and self.audio_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.audio_player.pause()
        else:
            self.audio_player.setSource(url)
            self.audio_player.play()

if __name__ == '__main__':
    from PySide6.QtWidgets import QSizePolicy
    from PySide6.QtGui import QTextDocument
    app = QApplication(sys.argv)
    note = StickyNoteApp()
    note.show()
    sys.exit(app.exec())
