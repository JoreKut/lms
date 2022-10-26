from app.pkg.models.routes import Routes
from . import (
    auth,
    course,
    lecture,
    users,
)

__routes__ = Routes(
    routers=(
        auth.router,
        course.router,
        lecture.router,
        users.router,
    )
)
