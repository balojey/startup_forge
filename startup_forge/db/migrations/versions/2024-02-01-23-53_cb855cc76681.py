"""empty message

Revision ID: cb855cc76681
Revises: 0612f85d74c0
Create Date: 2024-02-01 23:53:08.511425

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "cb855cc76681"
down_revision = "0612f85d74c0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("comment_reply")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "comment_reply",
        sa.Column("comment_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("reply_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["comment_id"],
            ["comment.id"],
            name="comment_reply_comment_id_fkey",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["reply_id"],
            ["comment.id"],
            name="comment_reply_reply_id_fkey",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("comment_id", "reply_id", name="comment_reply_pkey"),
    )
    # ### end Alembic commands ###