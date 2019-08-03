from fabric.api import task, local


def print_msg(msg, error=False):
    """Print message in console."""

    def green_msg(msg):
        """Make message green color in console."""
        return '\033[92m{0}\033[00m'.format(msg)

    def red_msg(msg):
        """Make message red color in console."""
        return '\033[91m{0}\033[00m'.format(msg)

    print_function = red_msg if error else green_msg
    print(print_function('\n{}\n'.format(msg)))


# MAIN COMMANDS
# ============================================================================

@task
def manage(command):
    """Run ``python3 manage.py`` command."""
    return local('python3 manage.py {}'.format(command))


@task
def run():
    """Run server."""
    return manage('runserver')


@task
def shell():
    """Run server."""
    return manage('shell_plus')


# GIT
# ============================================================================

@task
def push():
    """Push changes to all servers."""
    print_msg('1. Pushing to origin')
    local('git push origin master --tags')

    print_msg('2. Pushing to Heroku')
    local('git push heroku master')


# LOCALES
# ============================================================================

@task
def makemessages():
    """Make messages."""
    return manage('makemessages -l ru --no-location')


@task
def compilemessages():
    """Compile messages."""
    return manage('compilemessages')


# MIGRATIONS AND DATABASE
# ============================================================================

@task
def makemigrations():
    """Make migrations for database."""
    manage('makemigrations')


@task
def migrate():
    """Apply migrations to database."""
    print_msg('Applying migrations')
    manage('migrate')


@task
def createsuperuser(email='root@root.ru'):
    """Create superuser with default credentials."""
    print_msg('Creating superuser')
    return manage('createsuperuser --username root --email {}'.format(email))


@task
def resetdb():
    """Reset database to initial state."""
    print_msg('Remove "scr/media" folder')
    local('rm -rf media/')

    print_msg('Reset database')
    manage('reset_db -c --noinput')

    migrate()
    createsuperuser()


# STATIC CHECKS: ISORT AND PEP8
# ============================================================================

@task
def isort():
    """Fix imports formatting."""
    print_msg('Running imports fix')
    local('isort apps core config -y -rc')


@task
def pep8(path='apps core'):
    """Check PEP8 errors."""
    print_msg('Checking PEP8 errors')
    return local('flake8 --config=.flake8 {}'.format(path))


# REQUIREMENTS
# ============================================================================

@task
def requirements():
    """Install requirements."""
    print_msg('Installing requirements')
    local('pip install -r requirements.txt')


# HEROKU
# ============================================================================

@task
def logs():
    local('heroku logs --source app --tail')


@task
def scale(value=1):
    local(f'heroku ps:scale web={value}')


@task
def ps():
    local(f'heroku ps')


@task
def runweb():
    local(f'heroku local web -f Procfile.local')
