import sys
from app import Application

def main(argv):
    """Entry point for demo manager"""
    app = Application()
    return app.run(argv)

if __name__ == '__main__':
    SystemExit(main(sys.argv))
