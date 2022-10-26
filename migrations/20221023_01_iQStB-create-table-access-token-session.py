"""
create TABLE access_token_session
"""

from yoyo import step

__depends__ = {'20221022_01_7iV19-create-users'}

steps = [
    step(
        """
            create table if not exists access_token_sessions(
                token text,
                user_id uuid not null
                    constraint fk_access_token_user
                        references users(id)
                        on DELETE cascade
            );
        """,
        """
            drop table if exists access_token_sessions;
        """
    )
]
