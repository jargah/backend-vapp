from database.MySQLModel import MySQLModel

class ReferralMovementsModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.referral_movements'
        super().__init__(db, table)
      