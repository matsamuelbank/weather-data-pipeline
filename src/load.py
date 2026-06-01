import pandas as pd
from sqlalchemy.engine import Engine


def load_to_postgres(dataframe: pd.DataFrame, engine: Engine, table_name: str) -> int:
    """Insert a dataframe into PostgreSQL and return the number of loaded rows."""
    if dataframe.empty:
        return 0

    # Pour ce premier projet, to_sql suffit largement pour valider la logique ETL.
    dataframe.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
    )
    return len(dataframe.index)
