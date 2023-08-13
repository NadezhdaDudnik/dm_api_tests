def test_search(grpc_search):
    response = grpc_search.search(
        query='test_nadin',
        size=10,
        skip=0,
        search_across=['FORUM_TOPIC']
    )
