from django.db.models import Case, F, IntegerField, Q, Value, When
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Candidate
from .serializers import CandidateSerializer


class CandidateViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing candidate information.

    Provides CRUD operations for candidates in the ATS system.
    """

    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="q",
                description="Search query string (space-separated words to search in candidate names)",
                required=False,
                type=str,
            )
        ],
        description="Search candidates by name with results sorted by relevancy. Relevancy is defined as the number of words in the search query that match in the candidate name.",
    )
    @action(detail=False, methods=["get"])
    def search(self, request):
        """
        Search candidates by name with relevancy-based sorting.

        Relevancy is defined by the number of words in the search query
        that are found in the candidate's name. Results are ordered
        by the number of matching words (highest first).
        """
        search_query: str = request.query_params.get("q", "")
        if not search_query:
            return Response(self.get_serializer(self.queryset, many=True).data)

        # split the search query into words
        search_words = search_query.lower().split()
        filter_q = Q()

        # Build relevance annotations
        annotations = {}
        for i, word in enumerate(search_words):
            # Add this word to the filter criteria (OR condition)
            filter_q |= Q(name__icontains=word)

            # Add an annotation that gives 1 point if this word is found
            annotations[f"word_{i}_match"] = Case(
                When(name__icontains=word, then=1),
                default=0,
                output_field=IntegerField(),
            )

        # Filter candidates that match at least one word
        candidates = Candidate.objects.filter(filter_q)

        # Annotate with individual word matches
        candidates = candidates.annotate(**annotations)

        # Calculate total match score (sum of all word matches)
        match_score_expression = None
        for i in range(len(search_words)):
            field_name = f"word_{i}_match"
            if match_score_expression is None:
                match_score_expression = F(field_name)
            else:
                match_score_expression += F(field_name)

        # If we have no search words, default to 0
        if match_score_expression is None:
            candidates = candidates.annotate(match_score=Value(0))
        else:
            candidates = candidates.annotate(match_score=match_score_expression)

        # Order by descending match score
        candidates = candidates.order_by("-match_score", "name")

        serializer = self.get_serializer(candidates, many=True)
        return Response(serializer.data)
