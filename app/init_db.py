from app.database.postgres_connection import user_session_maker
from app.models.user_model import User
from app.models.group_model import Group
from app.models.groups_and_users import UserGroup
def initialize_db():
    session = user_session_maker()
    try:
        # הוספת משתמשים לדוגמה
        new_user1 = User(username='chezkyk', password='12345', address='bbb')
        new_user2 = User(username='user2', password='password2', address='address2')
        session.add(new_user1)
        session.add(new_user2)

        # הוספת קבוצות לדוגמה
        new_group1 = Group(group_name='Group1', address='Address1')
        new_group2 = Group(group_name='Group2', address='Address2')
        new_group3 = Group(group_name='Group3', address='Address3')
        new_group4 = Group(group_name='Group4', address='Address4')
        session.add(new_group1)
        session.add(new_group2)
        session.add(new_group3)
        session.add(new_group4)

        # הכנסה לדוגמה של קשרים בין משתמשים לקבוצות
        session.add(UserGroup(user=new_user1, group=new_group1))
        session.add(UserGroup(user=new_user2, group=new_group2))
        session.add(UserGroup(user=new_user1, group=new_group3))
        session.add(UserGroup(user=new_user2, group=new_group4))

        # מחויב לכל השינויים
        session.commit()

        print("Data inserted successfully.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()
