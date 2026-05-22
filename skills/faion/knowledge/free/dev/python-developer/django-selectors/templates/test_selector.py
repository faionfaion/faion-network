# purpose: pytest skeleton locking query count for a selector
# consumes: factory_boy factories for the model and its relations
# produces: regression test failing on N+1 reintroduction
# depends-on: pytest-django, factory_boy
# token-budget-impact: ~120 tokens

import pytest


@pytest.mark.django_db
def test_<entity>_list_query_count(django_assert_num_queries, <factory>, <user_factory>):
    user = <user_factory>()
    for _ in range(10):
        <factory>(user=user)

    with django_assert_num_queries(3):  # adjust to actual measured baseline
        from apps.<app>.selectors import <entity>_list_for_user
        result = list(<entity>_list_for_user(user=user))
        for item in result:
            # touch every relation a caller will access
            list(item.<related_set>.all())

    assert len(result) == 10
