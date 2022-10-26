"""
create users
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
            create table if not exists users(
                id uuid primary key default gen_random_uuid(),
                created_at timestamp default current_timestamp,
                username varchar(50) not null,
                hashed_password text not null,
                email varchar(50) not null,
                phone varchar(50),
                firstname varchar(50),
                lastname varchar(50),
                unique (username)
            );
        """,
        """
            drop table if exists users;
        """
    )
]
