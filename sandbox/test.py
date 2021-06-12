from models.initial import db, User, Tweet

db.drop_tables([User, Tweet])
db.connect(reuse_if_open=True)
db.create_tables([User, Tweet])

charlie = User.create(username='charlie')

Tweet.create(user=charlie, message='My first tweet')

print(User.get(User.username == 'charlie').username)