from api.administrator.routes import administrator
from api.landing.routes import landing
from api.catalog.routes import catalog
from api.identity.routes import identity

router = list()
router.append(administrator)
router.append(landing)
router.append(catalog)
router.append(identity)