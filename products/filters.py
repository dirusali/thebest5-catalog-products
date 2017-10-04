from django.db.models import F
from rest_framework.filters import SearchFilter
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

class FullTextSearchFilter(SearchFilter):
    """ 
    Class that implements the filter_queryset method to use PostgreSQL Full text search
    See https://docs.djangoproject.com/en/1.11/ref/contrib/postgres/search/
    """
    
    def filter_queryset(self, request, queryset, view):
        #search_fields = getattr(view, 'search_fields', None)
        params = request.query_params.get(self.search_param, '')
        search_terms = self.get_search_terms(request)

        if not search_terms:
            return queryset

        if len(search_terms) < 2:
            # if there are only one search term return the super implementation without full text search
            return super(FullTextSearchFilter, self).filter_queryset(request, queryset, view)

        # Old implementation
        # if not search_fields or not search_terms:
        #     return queryset
        # Old implementation
        # extra_weight = ['B','C','D']
        # vector = SearchVector(search_fields[0], weight='A')
        # for i,search_field in enumerate(search_fields[1:]):
        #     vector += SearchVector(search_field, weight=extra_weight[i])
        #
        # query = SearchQuery(params)
        # queryset = queryset.model.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.8).order_by('-rank')[:20]

        query = SearchQuery(params)
        queryset = queryset.model.objects.annotate(rank=SearchRank(F('search_vector'), query)).filter(rank__gte=0.8).order_by('-rank')[:20]
        return queryset

