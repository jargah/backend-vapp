from database.MySQLModel import MySQLModel

class ReferralRedemptionsModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.referral_redemptions'
        super().__init__(db, table)
      