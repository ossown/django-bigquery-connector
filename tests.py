import time
import traceback

from hamcrest import assert_that, equal_to, is_, none, not_none

from django.test import SimpleTestCase



class TestBigqueryBackend(SimpleTestCase):

    def test_accounts_query(self):
        success = False
        while not success:
            try:
                from accounts.models import Brand
                print("Querying Brand.objects.all()...")
                results = list(Brand.objects.all())
                print(f"Success! {len(results)} results:")
                for obj in results:
                    print(obj)
                success = True
            except Exception as e:
                print("Error occurred:")
                traceback.print_exc()
                print("Retrying in 5 seconds...")
                time.sleep(5)