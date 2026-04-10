from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class User(SQLModel, table=True):
    id: Optional[int] =  Field(default=None, primary_key=True)
    username:str = Field(index=True, unique=True)
    email:str = Field(index=True, unique=True)
    password:str

    ## Task 3.1: Relationship to link User to Many Todos
    todos: list['Todo'] = Relationship(back_populates="user")

    def set_password(self, plaintext_password):
        self.password = password_hash.hash(plaintext_password)

    def __str__(self) -> str:
        return f"(User id={self.id}, username={self.username} ,email={self.email})"


class TodoCategory(SQLModel, table=True):
    # Task 5.1: The Many-to-Many bridge table
    todo_id: int | None = Field(default=None, primary_key=True, foreign_key='todo.id')
    category_id: int | None = Field(default=None, primary_key=True, foreign_key='category.id')


class Todo(SQLModel, table=True):
    ## Task 2.1: Todo properties
    id: Optional[int] =  Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id') 
    text: str = Field(max_length=255)
    done: bool = Field(default=False)

    ## Task 3.2: Relationship mapping back to the single User
    user: User = Relationship(back_populates="todos")

    ## Task 5.2: Relationship mapping to Many Categories
    categories: list['Category'] = Relationship(back_populates="todos", link_model=TodoCategory)

    ## Task 3.4: Toggle method
    def toggle(self):
        self.done = not self.done
    
    
class Category(SQLModel, table=True):
    # Task 5.1: Category model mapping back to Many Todos
    id: Optional[int] =  Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id') 
    text: str = Field(max_length=255)

    todos: list['Todo'] = Relationship(back_populates="categories", link_model=TodoCategory)