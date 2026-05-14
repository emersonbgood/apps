import webview
import os

def main():
    # Get the path to your local HTML file
    file_path = 'file:///home/emersonberry/apps/website/browser.html'
    
    # Create the window loading your local "browser" interface
    window = webview.create_window('Website', file_path)
    
    webview.start()

if __name__ == '__main__':
    main()

