from fastapi import Query
from typing import Optional


class HotelsSearchArgs:

    """
    Searching args for endpoint 'hotels/find_hotels'
    """

    def __init__(
            self,
            location: str,
            stars: Optional[int] = Query(None, ge=1, le=5),
            limit: Optional[int] = Query(20, ge=1, le=100),
            offset: Optional[int] = Query(0, ge=0, )

    ):
        self.location = location
        self.stars = stars
        self.limit = limit
        self.offset = offset


class ServiceTypesArgs:

    """
    Args for creating new service type
    """

    def __init__(
            self,
            name: str
    ):
        self.name = name
