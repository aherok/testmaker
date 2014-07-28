import os
import sys

# settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'testmaker.settings'

# path
test_dir = os.path.join(os.path.dirname(__file__), 'testmaker')
sys.path.insert(0, test_dir)

# other imports
from django.test.utils import get_runner
from django.conf import settings

# force sqlite DB for testing purposes
settings.DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3'}}


def runtests():
    if 'south' in settings.INSTALLED_APPS:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['tester'])
    sys.exit(bool(failures))

if __name__ == '__main__':
    runtests()
