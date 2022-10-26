from app.pkg.models.routes import Routes
from . import (
    auth,
    course,
    lecture,
    users,
    lecturers
)

__routes__ = Routes(
    routers=(
        lecturers.router,
        auth.router,
        course.router,
        lecture.router,
        users.router,
    )
)
