from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 

    @validates("name")
    def validates_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name")
        
        name_list = [author.name for author in self.query.all()]

        if name in name_list:
            raise ValueError("Authors cannot have similar names")
        
        return name
        
    @validates("phone_number")
    def validates_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit() :
            raise ValueError("Phone Number MUST be ten digits") 
        
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("content")
    def validates_content(self, key, words):
        if len(words) < 250 :
            raise ValueError("Post Content must be at least 250 characters long")
        
        return words
    
    @validates("summary")
    def validates_summary(self, key, words):
        if len(words) > 250 :
            raise ValueError("Post Summary must be a maximum of 250 characters long")
        
        return words
    
    @validates("category")
    def validates_category(self, key, category):
        if category.lower() != "fiction" and category.lower() !="non-fiction":
            raise ValueError(""" Post Category MUST either be "Fiction" or "Non-Fiction" """)
        
        return category
        
    @validates("title")
    def validates_title(self, key, title):
        if ("Won't Believe" not in title 
             and "Secret" not in title  
             and "Top" not in title  
             and "Guess" not in title ):
            raise ValueError(""" Post Title is not sufficiently clickbaity. It should contain either of these: \n                             
                                - "Won't Believe"
                                - "Secret"
                                - "Top"
                                - "Guess"
                            """)
        
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'