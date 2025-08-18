from database.MySQLModel import MySQLModel

class ReferralOperatorsModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.referral_operators'
        super().__init__(db, table)
      