from db.models.blog import Blog
from schema.blog import CreateBlog
from schema.blog import UpdateBlog
from sqlalchemy.orm import Session


def create_new_blog(blog: CreateBlog, db: Session, author_id: int):
    if not author_id:
        return {"error": "author must login first to post"}

    blog = Blog(**blog.dict(), author_id=author_id)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


def retreive_blog(id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    return blog


def list_blogs(db: Session):
    blogs = db.query(Blog).filter(Blog.is_active == True).all()
    return blogs


def update_blog(id: int, blog: UpdateBlog, author_id: int, db: Session):
    blog_in_db = db.query(Blog).filter(Blog.id == id).first()
    if not blog_in_db:
        return {"error": f"Blog with id {id} does not exist"}
    if not blog_in_db.author_id == author_id:
        return {
            "error": f"Only author {blog_in_db.author_id} able to delete it,  author {id} cannot modify the blog"
        }

    blog_in_db.title = blog.title
    blog_in_db.content = blog.content
    blog_in_db.slug = blog.slug
    db.add(blog_in_db)
    db.commit()
    return blog_in_db


def delete_blog(id: int, author_id: int, db: Session):
    blog_in_db = db.query(Blog).filter(Blog.id == id)
    record_author_id = blog_in_db.first().author_id
    if not blog_in_db.first():
        return {"error": f"Could not find blog with id {id}"}
    if not record_author_id == author_id:
        return {
            "error": f"Only author {record_author_id} able to delete it,  author {id} cannot delete a blog"
        }
    blog_in_db.delete()
    db.commit()
    return {"msg": f"deleted blog with id {id}"}
