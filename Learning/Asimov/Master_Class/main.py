import sys
from streamlit.web import cli

sys.argv = ["streamlit", "run", "app.py"]
sys.exit(cli.main())
