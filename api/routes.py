from api.administrator.routes import administrator

from api.account.routes import router_account
from api.core.routes import router_core

router = list()
router.append(administrator)
router.append(router_account)
router.append(router_core)