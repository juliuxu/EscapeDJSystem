DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Julian Jark', 'julianj@ifi.uio.no'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db.sqlite3',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# The bootstrap stylesheet to use, included are these: cosmo cyborg orginal slate spacelab
BOOTSTRAP_STYLE = "orginal"

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'PUT_IN_YOUR_SECRET_KEY_HERE!'
