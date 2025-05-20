#!/bin/bash

# Create folders
mkdir -p electro_mart_project/backend/app/static/{css,js,images} \
    electro_mart_project/backend/app/templates \
    electro_mart_project/backend/tests \
    electro_mart_project/backend/migrations \
    electro_mart_project/database_design/{normalization,diagrams} \
    electro_mart_project/report/screenshots

# Go into project directory
cd electro_mart_project || exit

# Create Python and other backend files
touch backend/app/{__init__.py,models.py,routes.py,auth.py,schemas.py}
touch backend/app/static/css/style.css
touch backend/app/static/js/main.js

# Create HTML templates
touch backend/app/templates/{index.html,products.html,product_detail.html,cart.html,checkout.html,login.html,register.html,order_history.html,base.html}

# Create test files
touch backend/tests/{__init__.py,test_models.py,test_routes.py,test_auth.py}

# Other backend files
touch backend/{run.py,config.py,requirements.txt,.env.example}
touch backend/migrations/README.md
echo "# Store migration scripts here" > backend/migrations/README.md

# Database design files
touch database_design/{schema.sql,populate_data.sql,sample_queries.sql}
touch database_design/normalization/{1nf.md,2nf.md,3nf.md,bcnf.md}
touch database_design/diagrams/{eer_diagram.png,logical_model.png}

# Report files
touch report/{ElectroMart_Project_Report.docx,cover_page_template.docx}

# Project root files
touch .gitignore README.md

# Write content to README and requirements.txt
cat <<EOF > README.md
# ElectroMart E-Commerce Project

This project is for the IDATG2204 course.

## Setup

Instructions to set up and run the project will go here.
EOF

cat <<EOF > backend/requirements.txt
Flask==3.0.3
psycopg2-binary  # For PostgreSQL
SQLAlchemy==2.0.30
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.7
python-dotenv==1.0.1
# Add other packages like Flask-WTF for forms, Flask-Login for auth if needed
EOF

# .gitignore content
cat <<EOF > .gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
.pytest_cache/
.hypothesis/
pytestdebug.log
coverage.xml

# Flask stuff:
instance/
.webassets-cache

# Environments
.env
.venv
venv/
ENV/
env.bak/
env/

# Others
.mypy_cache/
.dmypy.json
.pyre/
.pytype/
.ipynb_checkpoints
EOF

cd ..
echo " Project structure for ElectroMart created successfully under the 'electro_mart_project' folder!"

