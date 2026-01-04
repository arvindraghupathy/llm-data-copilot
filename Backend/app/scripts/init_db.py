from app.infra.db.session import engine, Base
from app.infra.db.models import user, dataset, dataset_rows, dataset_documents # noqa

Base.metadata.create_all(bind=engine)
