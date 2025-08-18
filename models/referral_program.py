from database.MySQLModel import MySQLModel

class ReferralProgramModel(MySQLModel):
    def __init__(self, db) -> any:
        table = 'ven_app_api.referral_program'
        super().__init__(db, table)
      