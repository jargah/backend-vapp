from database.MySQLModel import MySQLModel

class ReferralBenefitModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.referral_benefit'
        super().__init__(db, table)
      