import pytest
from dm_api_search_async import SearchEntityType, SearchRequest


def test_search(grpc_search):
    grpc_search.search(
        query='nadya_course',
        size=10,
        skip=0,
        search_across=['FORUM_TOPIC']
    )


@pytest.mark.asyncio
async def test_search_async(grpc_search_async):
    response = await grpc_search_async.search(
        search_request=SearchRequest(
            query='test_nadin',
            size=10,
            skip=0,
            search_across=[SearchEntityType.FORUM_TOPIC]
        )
    )
    print(response)
