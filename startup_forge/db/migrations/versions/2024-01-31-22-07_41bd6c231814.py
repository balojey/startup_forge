"""empty message

Revision ID: 41bd6c231814
Revises: c4527ab0d79e
Create Date: 2024-01-31 22:07:10.780372

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "41bd6c231814"
down_revision = "c4527ab0d79e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "connection",
        sa.Column("request_from", sa.Uuid(), nullable=False),
        sa.Column("request_to", sa.Uuid(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["request_from"], ["user.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["request_to"], ["user.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("request_from", "request_to"),
    )
    op.create_table(
        "connection_request",
        sa.Column("request_from", sa.Uuid(), nullable=False),
        sa.Column("request_to", sa.Uuid(), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "ACCEPTED",
                "REJECTED",
                "CANCELED",
                name="connectionrequeststatus",
            ),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["request_from"], ["user.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["request_to"], ["user.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("request_from", "request_to"),
    )
    op.create_table(
        "education",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("institution_name", sa.String(length=150), nullable=False),
        sa.Column("course_of_study", sa.String(length=150), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("state", sa.String(length=150), nullable=False),
        sa.Column("country", sa.String(length=150), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "language",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column(
            "name",
            sa.Enum("ENGLISH", "SPANISH", "ARABIC", name="languagename"),
            nullable=False,
        ),
        sa.Column(
            "level",
            sa.Enum("BASIC", "CONVERSATIONAL", "FLUENT", name="languagelevel"),
            nullable=False,
        ),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "post",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("text", sa.Text(), nullable=True),
        sa.Column("files_urls", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "review",
        sa.Column("mentee_id", sa.Uuid(), nullable=False),
        sa.Column("mentor_id", sa.Uuid(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["mentee_id"], ["user.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["mentor_id"], ["user.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "social_link",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column(
            "platform",
            sa.Enum(
                "TWITTER",
                "LINKEDIN",
                "FACEBOOK",
                "INSTAGRAM",
                "WHATSAPP",
                name="platform",
            ),
            nullable=False,
        ),
        sa.Column("link", sa.String(length=150), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "time_slot",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column(
            "day",
            sa.Enum(
                "MONDAY",
                "TUESDAY",
                "WEDNESDAY",
                "THURSDAY",
                "FRIDAY",
                "SATURDAY",
                "SUNDAY",
                name="day",
            ),
            nullable=False,
        ),
        sa.Column("start_time", sa.Time(timezone=True), nullable=False),
        sa.Column("end_time", sa.Time(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("day", "start_time", "end_time"),
    )
    op.create_table(
        "booking",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("time_slot_id", sa.Uuid(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["time_slot_id"], ["time_slot.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "time_slot_id", "date"),
    )
    op.create_table(
        "comment",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("post_id", sa.Uuid(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["post_id"], ["post.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "like",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("post_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["post_id"], ["post.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("user_id", "post_id"),
    )
    op.create_table(
        "repost",
        sa.Column("post_id", sa.Uuid(), nullable=False),
        sa.Column("repost_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["post_id"], ["post.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["repost_id"], ["post.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("post_id", "repost_id"),
    )
    op.create_table(
        "booking_activity",
        sa.Column(
            "mentor_activity",
            sa.Enum(
                "PENDING",
                "APPROVED",
                "RESCHEDULED",
                "REJECTED",
                "CANCELED",
                "COMPLETED",
                name="bookingstatus",
            ),
            nullable=False,
        ),
        sa.Column(
            "mentee_activity",
            sa.Enum(
                "PENDING",
                "APPROVED",
                "RESCHEDULED",
                "REJECTED",
                "CANCELED",
                "COMPLETED",
                name="bookingstatus",
            ),
            nullable=True,
        ),
        sa.Column("booking_id", sa.Uuid(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["booking_id"], ["booking.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "comment_reply",
        sa.Column("comment_id", sa.Uuid(), nullable=False),
        sa.Column("reply_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["comment_id"], ["comment.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["reply_id"], ["comment.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("comment_id", "reply_id"),
    )
    op.add_column(
        "profile",
        sa.Column("years_of_experience", sa.String(length=150), nullable=True),
    )
    op.add_column("profile", sa.Column("bio", sa.Text(), nullable=True))
    op.add_column(
        "profile", sa.Column("expertises", sa.ARRAY(sa.String()), nullable=True)
    )
    op.add_column("profile", sa.Column("skills", sa.ARRAY(sa.String()), nullable=True))
    op.add_column(
        "profile",
        sa.Column("profile_picture_url", sa.String(length=100), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("profile", "profile_picture_url")
    op.drop_column("profile", "skills")
    op.drop_column("profile", "expertises")
    op.drop_column("profile", "bio")
    op.drop_column("profile", "years_of_experience")
    op.drop_table("comment_reply")
    op.drop_table("booking_activity")
    op.drop_table("repost")
    op.drop_table("like")
    op.drop_table("comment")
    op.drop_table("booking")
    op.drop_table("time_slot")
    op.drop_table("social_link")
    op.drop_table("review")
    op.drop_table("post")
    op.drop_table("language")
    op.drop_table("education")
    op.drop_table("connection_request")
    op.drop_table("connection")
    # ### end Alembic commands ###