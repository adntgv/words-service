"""allow nullable

Revision ID: be6b3dc39b91
Revises: dc0c61b08f4a
Create Date: 2023-10-11 18:45:26.783669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be6b3dc39b91'
down_revision: Union[str, None] = 'dc0c61b08f4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
 
def upgrade() -> None:
    # Allow nullable for the 'definition_text' column in the 'definitions' table
    op.alter_column('definitions', 'definition_text', nullable=True)

    # Allow nullable for the 'example_text' column in the 'definitions' table
    op.alter_column('definitions', 'example_text', nullable=True)

    # Allow nullable for the 'translated_text' column in the 'translations' table
    op.alter_column('translations', 'translated_text', nullable=True)

    # Allow nullable for the 'language' column in the 'translations' table
    op.alter_column('translations', 'language', nullable=True)

    # Allow nullable for the 'synonym_text' column in the 'synonyms' table
    op.alter_column('synonyms', 'synonym_text', nullable=True)


def downgrade() -> None:
    # Revert nullable for the 'definition_text' column in the 'definitions' table
    op.alter_column('definitions', 'definition_text', nullable=False)

    # Revert nullable for the 'example_text' column in the 'definitions' table
    op.alter_column('definitions', 'example_text', nullable=False)

    # Revert nullable for the 'translated_text' column in the 'translations' table
    op.alter_column('translations', 'translated_text', nullable=False)

    # Revert nullable for the 'language' column in the 'translations' table
    op.alter_column('translations', 'language', nullable=False)

    # Revert nullable for the 'synonym_text' column in the 'synonyms' table
    op.alter_column('synonyms', 'synonym_text', nullable=False)
