from database.MySQLModel import MySQLModel

class ReferralHistoryModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.referral_history'
        super().__init__(db, table)
      