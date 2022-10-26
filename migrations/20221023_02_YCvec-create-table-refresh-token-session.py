"""
create TABLE refresh_token_session
"""

from yoyo import step

__depends__ = {'20221023_01_iQStB-create-table-access-token-session'}

steps = [
    step(
        """
            create table refresh_token_sessions(
                token text,
                user_id uuid not null
                    constraint fk_access_token_user
                        references users(id)
                        on DELETE cascade
            );
        """,
        """
            drop table if exists refresh_token_sessions;
        """
    )
]
